The Squeeze Theorem (or Sandwich Theorem) is a method used in [[Calculus|calculus]] to determine the limit of a [[function]] by “squeezing” it between two other functions that have the same limit at a particular point. It’s especially helpful for finding limits when the [[function]] is difficult to evaluate directly.

#### Statement of the Squeeze Theorem:
If we have three functions $f(x)$, $g(x)$, and $h(x)$ on an interval around a point $c$ (except possibly at $c$ itself), and they satisfy the inequalities:$$f(x) \leq g(x) \leq h(x)$$
for all $x$ near $c$, then if:$$\lim_{x \to c} f(x) = \lim_{x \to c} h(x) = L$$
it follows that:
$$\lim_{x \to c} g(x) = L$$

In other words, if $g(x)$ is "squeezed" between $f(x)$ and $h(x)$, and both $f(x)$ and $h(x)$ approach the same limit $L$ as $x \to c$, then $g(x)$ must also approach $L$.

#### How to Use the Squeeze Theorem:
1. Identify two functions $f(x)$ and $h(x)$ that bound $g(x)$ such that $f(x) \leq g(x) \leq h(x)$.
2. Verify that both $\lim_{x \to c} f(x)$ and $\lim_{x \to c} h(x)$ exist and are equal.
3. Conclude that $\lim_{x \to c} g(x)$ also exists and is equal to the same value.

#### Example:
Consider finding $\lim_{x \to 0} x^2 \sin\left(\frac{1}{x}\right)$.

1. We know that $-1 \leq \sin\left(\frac{1}{x}\right) \leq 1$, so:
   $$-x^2 \leq x^2 \sin\left(\frac{1}{x}\right) \leq x^2$$
2. As $x \to 0$, both $-x^2$ and $x^2$ approach 0.
3. By the Squeeze Theorem, we conclude:$$\lim_{x \to 0} x^2 \sin\left(\frac{1}{x}\right) = 0$$

The Squeeze Theorem is widely applied when dealing with trigonometric functions multiplied by terms that approach zero, making it a useful tool for calculating complex limits.