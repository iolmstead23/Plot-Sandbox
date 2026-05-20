An **antiderivative** of a [[function]] $f(x)$ is a [[function]] $F(x)$ such that:

$F'(x) = f(x)$.

In other words, the antiderivative is the reverse process of [[differentiation]].

For example:

- If $f(x) = 2x$, then an antiderivative is $F(x) = x^2 + C$, where $C$ is the **constant of integration**.
- The constant $C$ arises because the [[derivative]] of a constant is zero, meaning there are infinitely many antiderivatives for a given [[function]].
#### **How to Find Antiderivatives**

1. **Basic Rules for Power Functions**:
    
    $\int x^n \, dx = \frac{x^{n+1}}{n+1} + C, \quad \text{for } n \neq -1$.
    
    Example: $\int x^2 \, dx = \frac{x^3}{3} + C$.
    
2. **Constants**:
    
    $\int k \, dx = kx + C$.
    
    Example: $\int 5 \, dx = 5x + C$.
    
3. **Exponential Functions**:
    
    $\int e^x \, dx = e^x + C, \quad \int a^x \, dx = \frac{a^x}{\ln a} + C \, (a > 0, a \neq 1)$.
4. **Trigonometric Functions**:
    
    $\int \sin x \, dx = -\cos x + C, \quad \int \cos x \, dx = \sin x + C$.
5. **Logarithmic Rule**:
    
    $\int \frac{1}{x} \, dx = \ln|x| + C, \quad x \neq 0$.
#### **Antiderivatives vs. Derivatives**

- **[[Derivative]]**: Measures the rate of change or slope of a [[function]]. For $f(x)=x^3$,$f′(x)=3x^2$.
- **Antiderivative**: Reverses the process of [[differentiation]], finding a [[function]] whose [[derivative]] is the given [[function]]. For $f(x)=3x^2$, an antiderivative is $F(x) = x^3 + C$.
#### **Antiderivatives and Area**

The **definite [[integral]]** uses antiderivatives to calculate the area under a curve:

$\int_a^b f(x) \, dx = F(b) - F(a)$,

where $F(x)$ is any antiderivative of $f(x)$.

1. Compute the **antiderivative** of $f(x)$.
2. Evaluate $F(x)$ at the limits of integration, $b$ (upper) and $a$ (lower).
3. Subtract: $F(b) - F(a)$.
#### **Example: Calculating Area Using Antiderivatives**

Find the area under $f(x) = x^2$ from $x = 1$ to $x=3$:

1. Find the antiderivative:
    
    $F(x) = \frac{x^3}{3}$​.
2. Evaluate the definite [[integral]]:
    
    $\int_1^3 x^2 \, dx = F(3) - F(1) = \left(\frac{3^3}{3}\right) - \left(\frac{1^3}{3}\right) = \frac{27}{3} - \frac{1}{3} = \frac{26}{3}$.

The area under the curve is $\frac{26}{3}$.
#### **Key Points to Remember**

1. **Antiderivative is the Reverse of [[Derivative]]**:
    
    - [[Differentiation]] gives the rate of change, while the antiderivative reconstructs the original [[function]].
2. **The Constant of Integration ($C$)**:
    
    - Always include $+C$ when finding an indefinite [[integral]].
3. **Definite Integrals Use Antiderivatives**:
    
    - Compute exact areas or net changes by evaluating the antiderivative at the bounds.
4. **Applications**:
    
    - Antiderivatives are used in physics, engineering, and economics to calculate areas, displacements, and accumulated quantities.

Antiderivatives provide a powerful tool for understanding the accumulation of quantities and connecting [[differentiation]] with integration!