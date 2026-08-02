# Churn Without a Cancel Button

Identifying silent churn in a non-contractual business, and
measuring which customers actually respond to intervention.

## The problem

Subscription businesses know when a customer leaves — they
cancel. Marketplaces and retailers don't. Customers simply
stop buying, and the only signal is silence.

This creates two problems with no obvious starting point.

**There is no churn label.** You cannot train a model to
predict something your data doesn't record. The label has
to be constructed, and a fixed rule like "90 days inactive"
fails immediately: a weekly shopper silent for a month is
at risk, while a quarterly shopper silent for a month is
behaving normally.

**You cannot verify that retention spending works.** Customers
who accept offers tend to be the ones who were already most
engaged. Comparing them to everyone else measures who signed
up, not what the offer did.

## What this project does

1. **Constructs a churn label** from behaviour, deriving the
   inactivity threshold from observed return rates and scaling
   it to each customer's own purchase rhythm.

2. **Segments customers** by shopping behaviour, so the same
   churn score can be acted on differently depending on who
   it belongs to.

3. **Measures intervention effect** using a randomised
   promotional campaign, separating the effect of the offer
   from the effect of who was already buying.

## Why it matters

Marketplace companies discuss retention constantly and credit
membership programs with driving it, but the quantified claims
are correlations — members spend more, members retain longer.
Members also self-select. This project shows what the answer
looks like when the treatment is randomised and the effect
can actually be isolated.