Linear Approximation is a method in [[calculus]] used to approximate the value of a [[function]], $f(x)$, near a specific point, $a$. By using the tangent line of the [[function]] at $a$, we replace the curve with a straight line, simplifying calculations. The method assumes the [[function]] is differentiable at $a$, though it may not be continuous.

This approach leverages the idea that a differentiable [[function]] behaves locally like a straight line. The formula is derived from the equation of the tangent line.

### **Key Observations**

- **Tangent Line as a Local Approximation**: The closer $x$ is to $a$, the better the approximation.
- **Differentiability and Continuity**: The method requires $f(x)$ to be differentiable at $a$. While continuity is not strictly required for [[differentiation]], functions used in practical applications are usually continuous near $a$.
### **Formula for Linear Approximation**

The linear approximation of a [[function]] $f(x)$ at $x=a$ is given by:
$$L(x) = f(a) + f'(a)(x - a)$$

Where:

- $L(x)$: Approximated value of $f(x)$.
- $f(a)$: Value of the [[function]] at $a$.
- $f′(a)$: [[Derivative]] of the [[function]] at $a$.
- $(x−a)$: The change in $x$, often written as $\Delta x$.

### **Steps to Apply Linear Approximation**

1. **Find the [[Derivative]]**: Differentiate $f(x)$ to determine $f′(x)$.
2. **Evaluate at Point $a$**: Compute $f(a)$ and $f′(a)$.
3. **Substitute into the Formula**: Use the formula $L(x) = f(a) + f'(a)(x - a)$.
4. **Approximate**: Substitute the value of $x$ or $\Delta x$ to get the approximated value of $f(x)$.

### **Applications of Linear Approximation**

1. **Physics**: Approximating small changes in velocity, position, or energy.
2. **Engineering**: Simplifying complex models for real-time calculations.
3. **Economics**: Estimating marginal costs or revenue.
4. **Numerical Analysis**: Providing a base for numerical integration or differential equations.
