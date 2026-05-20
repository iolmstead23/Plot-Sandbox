#### Definition:

The **Rational Root Theorem** is a principle in [[mathematics]] used to identify all possible rational roots (or zeros) of a [[polynomial]] equation with integer coefficients. It is particularly useful when trying to factor or solve [[polynomial]] equations.

#### Statement of the Theorem:

If a [[polynomial]] $f(x) = a_nx^n + a_{n-1}x^{n-1} + \ldots + a_1x + a_0$ has rational roots, say $\frac{p}{q}$​, then:

1. $p$ (the numerator) is a factor of the constant term $a_0$​.
2. $q$ (the denominator) is a factor of the leading coefficient $a_n$​.

#### Rational Root Candidates:

The possible rational roots are all the fractions $\frac{p}{q}$​ formed by:

1. Taking all factors of $a_0$ (constant term).
2. Dividing them by all factors of $a_n$ (leading coefficient).

#### Steps to Apply the Rational Root Theorem:

1. Write down the [[polynomial]] in standard form.
2. Identify the constant term ($a_0$) and the leading coefficient ($a_n$​).
3. List all factors of $a_0$ and $a_n$.
4. Form all possible fractions $\frac{p}{q}$​, where $p$ divides $a_0$​ and $q$ divides $a_n$​. Include both positive and negative values.
5. Test each candidate root by substituting it into the [[polynomial]] equation. A candidate is a root if it satisfies $f(x) = 0$.

#### Example:

Solve $f(x) = 2x^3 - 9x^2 + 5x - 3$ using the Rational Root Theorem.

1. **Identify coefficients**:
    
    - $a_0 = -3$ (constant term)
    - $a_n = 2$ (leading coefficient)
2. **Find factors**:
    
    - Factors of $a_0​: \pm 1, \pm 3$
    - Factors of $a_n$​: $\pm 1, \pm 2$
3. **Form possible roots**:
    
    Possible roots: $\text{Possible roots: } \pm 1, \pm \frac{1}{2}, \pm 3, \pm \frac{3}{2}$
4. **Test candidates**: Substitute each candidate into $f(x)$ to find roots. For example:
    
    - $f(1) = 2(1)^3 - 9(1)^2 + 5(1) - 3 = 2 - 9 + 5 - 3 = -5$ (not a root).

#### Applications:

- The Rational Root Theorem is a systematic way to find rational roots of polynomials, especially when factoring manually.
- It helps determine if a [[polynomial]] is irreducible over the rationals.
- It is often the first step in solving higher-degree polynomials.

#### Limitations:

- The theorem only finds **rational** roots. Irrational or complex roots require additional methods like factoring, completing the square, or numerical approximation.
- The list of candidates can be long, making the method tedious for large coefficients.

#### Key Takeaways:

- Use the Rational Root Theorem to narrow down potential roots.
- Test systematically to verify actual roots.
- Combine with synthetic division or factoring to simplify polynomials once a root is found.