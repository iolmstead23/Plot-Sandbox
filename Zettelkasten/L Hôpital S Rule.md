**L'Hôpital's Rule** is a powerful [[differentiation]] method used to evaluate limits that produce indeterminate forms, such as $\frac{0}{0}$ or $\frac{\infty}{\infty}$. The rule states that if $\lim_{x \to c} \frac{f(x)}{g(x)}$ results in an indeterminate form, then, provided certain conditions, we can compute this limit by taking the derivatives of the numerator and the denominator:$$\lim_{x \to c} \frac{f(x)}{g(x)} = \lim_{x \to c} \frac{f'(x)}{g'(x)}$$​
This rule can be applied iteratively until an indeterminate form no longer appears, as long as the derivatives $f'(x)$ and $g'(x)$ exist and $g'(x) \neq 0$.

### Conditions for L'Hôpital's Rule

L'Hôpital's Rule applies under these conditions:

1. **Indeterminate Form:** The original limit produces $\frac{0}{0}$ or $\frac{\infty}{\infty}$.
2. **Differentiability:** The functions $f(x)$ and $g(x)$ must be differentiable near $x = c$.
3. **Non-Zero [[Derivative]] of Denominator:** The [[derivative]] $g'(x)$ should not equal zero at $x = c$.
### Historical Background

The rule is named after the French [[mathematics|mathematician]] Guillaume de l'Hôpital, who published it in 1696 in the first textbook on differential [[calculus]]. However, it’s believed that the rule was developed by the Swiss mathematician Johann Bernoulli, who shared it with l'Hôpital. Bernoulli is credited with the formal proof, while l'Hôpital popularized it through his work.
### Example

Consider the limit:$$\lim_{x \to 0} \frac{\sin(x)}{x}$$​
Direct substitution results in $\frac{0}{0}$, an indeterminate form. By applying L'Hôpital's Rule, we take the [[derivative]] of the numerator and denominator:

1. $f(x) = \sin(x) \Rightarrow f'(x) = \cos(x)$
2. $g(x) = x \Rightarrow g'(x) = 1$

Now we substitute:$$\lim_{x \to 0} \frac{\sin(x)}{x} = \lim_{x \to 0} \frac{\cos(x)}{1} = \cos(0) = 1$$