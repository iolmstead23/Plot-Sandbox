In [[calculus]], $u$-substitution is a technique for finding the [[antiderivative]] ([[integral]]) of complex functions. This method is particularly useful for integrating functions that are composites, where one [[function]] is nested within another. By substituting a part of the [[function]] with a new variable $u$, we simplify the [[function]], making integration more manageable. $u$-substitution is based on the principle of reversing the [[chain rule]] in [[differentiation]], so it allows us to find the [[antiderivative]] by effectively "undoing" a [[differentiation]].

#### When to Use $u$-Substitution

You’ll want to consider using $u$-substitution when:

- You see a composite [[function]] (a [[function]] within another [[function]]) and need to simplify it for integration.
- The integrand (the expression being integrated) contains a [[function]] and its [[derivative]], or something close to it.

For example, if you have an [[integral]] like $\int f(g(x)) \times g′(x) dx$, you might choose $u=g(x)$, which will help you rewrite the [[integral]] in terms of $u$, simplifying the process.

#### How $u$-Substitution Works

1. **Choose a $u$-value**: Identify a part of the [[function]] $u=g(x)$ such that its differential, $du=g′(x)dx$, is also present in the integrand.
2. **Rewrite in terms of $u$**: Substitute $u$ and $du$ in place of $g(x)$ and $g′(x)dx$, respectively.
3. **Integrate with respect to $u$**: With the [[function]] now simplified, integrate it in terms of $u$.
4. **Substitute back**: Once integrated, replace $u$ with $g(x)$ to return the solution to terms of the original variable xx.