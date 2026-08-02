Churn Without a Cancel Button

Finding customers who quietly stop buying—and working out which ones are worth spending money on.

The Problem

Netflix knows when you leave. You click Cancel, and that moment gets recorded.

A shop does not. A food delivery app does not. Customers simply stop coming back one day. Nobody announces it. All you see is silence.

This creates two major problems.

1. There Is No Churn Label

You cannot teach a model to identify something your data never recorded. You first have to build the churn label yourself.

A simple rule does not work well.

Suppose you decide that 90 days without a purchase means the customer has churned:

A customer who shops every week and has been inactive for one month is clearly at risk, but the rule says they are fine.

A customer who normally shops every three months and has been inactive for one month is behaving normally, but the same rule may soon flag them.

One cutoff cannot fit every customer.

2. You Cannot Tell Whether Offers Actually Work

You send discounts to customers, and some of them continue buying. It looks like the discount worked.

However, customers who respond to offers are often the same customers who were already buying the most. They may have continued purchasing even without the offer.

In that case, you have not measured what the offer changed. You have only measured who was already loyal.

What This Project Does

1. Builds a Churn Label from Customer Behaviour

Instead of guessing a fixed inactivity cutoff, the project examines the data and asks:

How many customers return after 30 days of inactivity?

How many return after 60 days?

How many return after 90 days?

At some point, almost nobody returns. That point becomes the baseline churn cutoff.

The project then adjusts the cutoff for each customer based on how often they normally purchase.

2. Groups Customers into Behavioural Segments

Customers behave differently:

Some shop weekly and buy in bulk.

Some repeatedly purchase the same product.

Some mainly buy when a discount is available.

Some purchase only occasionally.

Knowing that a customer may leave is not enough. You also need to understand what type of customer they are before deciding what action to take.

3. Measures What an Offer Actually Changes

The project uses data from a real experiment in which:

A promotional message was sent to a randomly selected treatment group.

The message was withheld from a randomly selected control group.

Because assignment was random, the difference between the two groups estimates the true effect of the promotion.

This separates the impact of the offer from the customer's existing likelihood of purchasing.

Why It Matters

Large marketplace companies frequently discuss retention and membership programs. They may report that members spend several times more than non-members.

However, customers do not join membership programs randomly. The people who pay for memberships are often already the platform's heaviest users.

This creates an important question:

How much of the difference comes from the membership program, and how much comes from the type of customer who chose to join?

Simple comparisons between members and non-members cannot answer that question.

This project demonstrates what the analysis looks like when an offer is assigned randomly and its incremental effect can be measured separately from existing customer loyalty.
