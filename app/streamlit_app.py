import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Retention Targeting", layout="wide", page_icon="◐")

st.markdown("""<style>
    [data-testid="stMetricValue"] {font-size: 1.7rem; font-weight: 600;}
    [data-testid="stMetricLabel"] {font-size: 0.8rem; opacity: 0.7;}
    [data-testid="stProgress"] > div > div {background-color: rgba(255,255,255,0.08);}
    [data-testid="stProgress"] > div > div > div > div {background-color: #C4614F;}
    h1 {font-weight: 600; letter-spacing: -0.02em;}
    .block-container {padding-top: 2.5rem;}
</style>""", unsafe_allow_html=True)

NAIVE = 0.0332

@st.cache_data
def load():
    return pd.read_parquet("app/app_data.parquet")

df = load()

st.title("Retention Targeting Tool")
st.caption("X5 RetailHero · 30,006 held-out customers · randomised SMS campaign")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Overview", "Who to contact", "Is it worth it?", "Customer lookup"])


def measure(d):
    t, c = d[d.treatment == 1]['target'], d[d.treatment == 0]['target']
    return 0.0 if len(t) == 0 or len(c) == 0 else t.mean() - c.mean()

def rank_and_take(col, pct):
    return df.nlargest(max(int(len(df) * pct), 1), col)


# ───────────────────────── Overview ─────────────────────────
with tab1:
    total_risk = (df.churn_risk * df.total_spend).sum()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Customers", f"{len(df):,}")
    c2.metric("Campaign effect", f"{NAIVE*100:.1f} pp",
              help="Extra buyers per 100 contacted, on average")
    c3.metric("Would buy anyway", f"{df[df.treatment==0]['target'].mean()*100:.0f}%")
    c4.metric("Revenue at risk", f"₽{total_risk/1e6:.1f}M")

    st.divider()
    st.subheader("Where the money is")

    seg = df.groupby('segment_name').agg(
        n=('client_id', 'count'),
        spend=('total_spend', 'mean'),
        risk=('churn_risk', 'mean')).reset_index()
    seg['at_risk'] = seg.n * seg.risk * seg.spend
    seg = seg.sort_values('at_risk', ascending=False)

    for col, (_, r) in zip(st.columns(len(seg)), seg.iterrows()):
        with col:
            st.markdown(f"**{r.segment_name}**")
            st.markdown(f"### ₽{r.at_risk/1e6:.1f}M")
            st.caption(f"{r.n:,} customers · {r.risk*100:.0f}% at risk")
            st.progress(float(r.risk))

    st.divider()
    st.warning(
        "**Lapsing light** shoppers are 72% likely to leave but hold only ₽2.6M. "
        "**High-value bulk** shoppers are 31% likely to leave and hold ₽26M — "
        "ten times more. Ranking by risk alone points at the wrong group.")


# ─────────────────────── Who to contact ───────────────────────
with tab2:
    st.subheader("Set a budget")
    n = st.slider("How many customers can you contact?",
                  500, len(df), 3000, step=500, label_visibility="collapsed")
    st.caption(f"Contacting **{n:,}** of {len(df):,} customers ({n/len(df)*100:.0f}%)")
    pct = n / len(df)

    st.divider()

    policies = {
        "Response × value": "value_score",
        "Response only": "uplift_score",
        "Churn risk": "churn_risk",
    }

    best_rev = 0
    for col, (label, key) in zip(st.columns(3), policies.items()):
        top = rank_and_take(key, pct)
        lift = measure(top)
        rev = lift * top.avg_spend.mean() * n
        with col:
            st.markdown(f"**{label}**" + ("  ⭐" if key == "value_score" else ""))
            st.metric("Extra revenue", f"₽{rev:,.0f}")
            st.caption(f"{lift*n:,.0f} extra purchases")

    st.caption("⭐ Recommended. Response-only finds more buyers, but they spend "
               "less — so it earns less overall.")

    st.divider()
    st.subheader("Your targeting list")

    chosen = st.radio("Rank by", list(policies.keys()),
                      horizontal=True, label_visibility="collapsed")
    out = rank_and_take(policies[chosen], pct)

    display = out[['client_id', 'segment_name', 'churn_risk',
                   'uplift_score', 'total_spend']].copy()
    display.columns = ['Customer', 'Segment', 'Risk', 'Response', 'Spend']
    display['Risk'] = (display['Risk'] * 100).round(0).astype(int).astype(str) + '%'
    display['Response'] = (display['Response'] * 100).round(1).astype(str) + 'pp'
    display['Spend'] = '₽' + display['Spend'].round(0).astype(int).map('{:,}'.format)

    st.dataframe(display.head(25), use_container_width=True, hide_index=True)
    st.download_button(f"Download all {len(out):,} customers",
                       out.to_csv(index=False), "targets.csv", "text/csv")


# ─────────────────────── Is it worth it? ───────────────────────
with tab3:
    st.subheader("Where does the campaign stop paying?")

    c1, c2 = st.columns(2)
    cost = c1.slider("Cost per message (₽)", 1, 50, 5)
    margin = c2.slider("Gross margin (%)", 5, 50, 22) / 100

    pts = []
    for p in np.arange(0.05, 1.01, 0.05):
        top = rank_and_take("value_score", p)
        k = len(top)
        gross = measure(top) * top.avg_spend.mean() * margin * k
        pts.append({"pct": p * 100, "net": gross - cost * k})
    curve = pd.DataFrame(pts)
    best = curve.loc[curve.net.idxmax()]

    if best.net > 0:
        st.success(f"**Contact the top {best.pct:.0f}%** — net profit "
                   f"₽{best.net:,.0f} on {int(len(df)*best.pct/100):,} messages")
    else:
        st.error(f"**Do not run the campaign.** At ₽{cost} per message, "
                 "no budget level is profitable.")

    fig = go.Figure(go.Scatter(
        x=curve.pct, y=curve.net, mode="lines",
        line=dict(color="#C4614F", width=3), fill='tozeroy',
        fillcolor="rgba(196,97,79,0.12)"))
    fig.add_hline(y=0, line_dash="dot", line_color="grey")
    fig.update_layout(
        xaxis_title="% of customers contacted", yaxis_title="Net profit (₽)",
        height=380, margin=dict(t=20, b=40),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

    st.info("Drag the cost slider. Below ₽5 the campaign should reach almost "
            "everyone. Above roughly ₽10 it should not run at all.")


# ─────────────────────── Customer lookup ───────────────────────
with tab4:
    cid = st.text_input("Customer ID", df.client_id.iloc[0])
    row = df[df.client_id == cid]

    if row.empty:
        st.warning("No customer with that ID.")
    else:
        r = row.iloc[0]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Segment", r.segment_name)
        c2.metric("Risk of leaving", f"{r.churn_risk*100:.0f}%")
        c3.metric("Total spend", f"₽{r.total_spend:,.0f}")
        c4.metric("Visits", f"{int(r.n_txn)}")

        st.divider()
        rank = int((df.value_score > r.value_score).sum() + 1)
        pctile = rank / len(df) * 100

        if pctile <= 10:
            st.success(f"**Contact.** Ranked {rank:,} of {len(df):,} "
                       f"by expected value — top {pctile:.0f}%.")
        else:
            st.info(f"**Below the cut-off.** Ranked {rank:,} of {len(df):,} "
                    f"— top {pctile:.0f}%.")

        st.caption(f"Last visit {int(r.recency)} days ago · "
                   f"typically shops every {r.avg_gap:.0f} days · "
                   f"uses {int(r.n_stores)} stores")