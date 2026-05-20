Probability theory provides a [[mathematics|mathematical ]]framework for understanding random phenomena. It allows us to quantify uncertainty and make predictions about the likelihood of events. The foundation of probability rests on several key concepts that help us model real-world situations involving chance and uncertainty.

## Sample Spaces and Events

A sample space ($\Omega$) represents all possible outcomes of a random experiment. Events are subsets of the sample space. For any event A, the probability P(A) must satisfy three axioms:

1. $P(A) \geq 0$ (Non-negativity)
2. $P(\Omega) = 1$ (Total probability)
3. For mutually exclusive events, $P(A \cup B) = P(A) + P(B)$ (Additivity)

## Probability Rules and Operations

### Addition Rule

For any two events A and B: $P(A \cup B) = P(A) + P(B) - P(A \cap B)$

### Multiplication Rule

For dependent events: $P(A \cap B) = P(A)P(B|A)$

For independent events: $P(A \cap B) = P(A)P(B)$

## Conditional Probability

Conditional probability represents the likelihood of an event occurring given that another event has occurred. It is expressed as:

$P(A|B) = \frac{P(A \cap B)}{P(B)}$

This concept forms the basis for many advanced probability topics, including [[Bayes' Theorem]].

## Random Variables and Distributions

### Discrete Random Variables

A discrete random variable has a countable number of possible values. Its probability mass [[function]] (PMF) must satisfy: $\sum_{x} P(X = x) = 1$

The expected value is calculated as: $E(X) = \sum_{x} xP(X = x)$

### Continuous Random Variables

Continuous random variables are described by probability density functions (PDF). The probability of a continuous random variable falling within an interval is: $P(a \leq X \leq b) = \int_{a}^{b} f(x)dx$

## Important Probability Distributions

### Binomial Distribution

For n independent trials with probability p of success: $P(X = k) = \binom{n}{k}p^k(1-p)^{n-k}$

### Poisson Distribution

For rare events with rate λ: $P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}$

### Normal Distribution

The standard normal distribution's PDF: $f(x) = \frac{1}{\sqrt{2\pi}}e^{-\frac{x^2}{2}}$

## Applications in Real-World Scenarios

Probability theory finds applications in:

- Risk assessment and insurance
- Quality control in manufacturing
- Genetic studies and inheritance
- Game theory and decision making
- Financial modeling and investment
- [[Machine learning]] and AI [[Algorithm|algorithms]]