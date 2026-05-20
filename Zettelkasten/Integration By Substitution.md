**Integration by substitution** is a powerful method in [[calculus]] used to simplify complex integrals. It is essentially the reverse process of the [[chain rule]] for [[differentiation]]. By changing the variable of integration, the method transforms a difficult [[integral]] into a simpler one, making it more manageable to evaluate.
#### **Key Concept**

The method relies on substituting a part of the [[function]] with a new variable, $u$, to simplify the [[integral]].

- If the [[integral]] is of the form:
    
    $\int f(g(x)) \cdot g'(x) \, dx$,
    
    we make the substitution:
    
    $u = g(x), \quad \text{so that} \quad du = g'(x)dx$.
- The [[integral]] then becomes:
    
    $\int f(g(x)) \cdot g'(x) \, dx = \int f(u)du$.

By restructuring the [[integral]] in terms of $u$ and $du$, the integration becomes more straightforward.

#### **Steps for Using Integration by Substitution**

1. **Identify $g(x)$:**
    
    - Look for a part of the integrand (often inside another [[function]] or its [[derivative]] is present) to set as $u = g(x)$.
2. **Differentiate $u$:**
    
    - Compute $du = g'(x)dx$ and substitute for $dx$ in the original [[integral]].
3. **Rewrite the [[Integral]] in Terms of $u$:**
    
    - Replace all occurrences of $g(x)$ with $u$, and express $dx$ in terms of $du$. The goal is to rewrite the [[integral]] entirely in terms of $u$.
4. **Evaluate the New [[Integral]]:**
    
    - Perform the integration with respect to $u$.
5. **Back-Substitute:**
    
    - Replace $u$ with the original [[function]] $g(x)$ to return to the variable $x$.