Derivatives measure the rate of change of a [[function]] with respect to its variable. Developed independently by [[Isaac Newton]] and [[Gottfried Wilhelm Leibniz]] in the 17th century, derivatives became essential tools in physics, engineering, and economics, particularly for analyzing motion, growth, and [[optimization]] problems. It is an essential in using [[Calculus]].

**Key [[Differentiation]] Techniques**

1. **[[Power Rule]]**: For $f(x)=xn$, the derivative $f′(x)=nx^{n−1}$.
    
    - Example: If $f(x)=x^3$, then $f′(x)=3x^2$.
    
1. **[[Chain Rule]]**: For a composite [[function]] $f(g(x))$, the derivative is $f'(g(x)) \cdot g'(x)$.
    
    - Example: If $f(x)=sin⁡(x^2)$, then $f′(x)=cos⁡(x^2)⋅2x$.
    
1. **[[Quotient Rule]]**: For $f(x)=\frac{g(x)}{h(x)}$​, the derivative is $f′(x)=\frac{g'(x)h(x) - g(x)h'(x)}{[h(x)]^2}$​.
    
    - Example: If $f(x) = \frac{x}{x+1}$​, then $f′(x)=\frac{(1)(x+1)−(x)(1)}{(x+1)^2}$​.
    
1. **Logarithmic [[Differentiation]]**: Useful when differentiating products or quotients of functions. For $f(x) = \ln(g(x))$, the derivative is $f'(x) = \frac{g'(x)}{g(x)}​$.
    
    - Example: If $f(x) = \ln(x^2 + 1)$, then $f'(x) = \frac{2x}{x^2 + 1}​$.
### Differentiating Trigonometric Functions

Trigonometric functions have specific rules for [[differentiation]]:

- $\frac{d}{dx}(\sin x) = \cos x$
- $\frac{d}{dx}(\cos x) = -\sin x$
- $\frac{d}{dx}(\tan x) = \sec^2 x$

These rules apply directly, and when trigonometric functions are part of more complex compositions, the [[Chain Rule]] is used.

- Example: If $f(x) = \sin(3x)$, then $f'(x) = \cos(3x) \cdot 3 = 3\cos(3x)$.

### Differentiating Exponential Functions

Exponential functions also follow specific [[differentiation]] rules:

- For $f(x) = e^x$, the derivative $f'(x) = e^x$.
    
- For a general exponential [[function]] $f(x) = a^x$, where $a$ is a constant, $f'(x) = a^x \ln a$.
    
    - Example: If $f(x) = e^{2x}$, then $f'(x) = e^{2x} \cdot 2 = 2e^{2x}$.

### Differentiating Logarithmic Functions

Logarithmic functions also have specific rules for [[differentiation]], which are closely tied to their properties and connections with exponential functions:

- The derivative of the natural logarithm, $\ln x$, is:
    
    $\frac{d}{dx}(\ln x) = \frac{1}{x}, \quad \text{for } x > 0$.
    
- For a logarithmic [[function]] with a different base, $\log_a x$, the derivative is:
    
    $\frac{d}{dx}(\log_a x) = \frac{1}{x \ln a}, \quad \text{for } x > 0 \text{ and } a > 0, a \neq 1$.

When logarithmic functions are part of a composition, the **[[Chain Rule]]** is applied.

**Example 1**: Natural Logarithm

- If $(x) = \ln(3x)$, then:
- $f'(x) = \frac{1}{3x} \cdot 3 = \frac{1}{x}$​.

**Example 2**: Logarithm with Base 10

- If $f(x) = \log_{10}(x^2)$, then:
- $f'(x) = \frac{1}{x^2 \ln 10} \cdot 2x = \frac{2}{x \ln 10}$​.

**Theorems Related to Derivatives**

1. **[[Mean Value Theorem]] (MVT)**: If a [[function]] $f$ is continuous on $[a,b]$ and differentiable on $(a,b)$, there exists a point $c \in (a, b)$ such that $f'(c) = \frac{f(b) - f(a)}{b - a}$​, meaning there’s a tangent parallel to the secant line.
    
2. **[[Rolle's Theorem]]**: If $f$ is continuous on $[a,b]$, differentiable on $(a,b)$, and $f(a) = f(b)$, then there exists $c \in (a, b)$ where $f'(c) = 0$, indicating a horizontal tangent.
    
3. **[[Squeeze Theorem]]**: Useful for limits, this theorem states that if $f(x) \leq g(x) \leq h(x)$ and $\lim_{{⁡x \to a}} f(x)= \lim⁡_{{x→a}}h(x) = L$, then $\lim⁡_{{x→a}} g(x)=L$.
    
**Applications of Derivatives**

1. **[[Linear Approximation]]**: By approximating a [[function]] $f(x)$ near $x=a$ using $f(x) \approx f(a) + f'(a)(x - a)$, derivatives help estimate values and model changes efficiently.
    
2. **Related Rates**: In problems involving quantities changing over time, derivatives link these quantities, allowing us to solve for unknown rates of change in real-time applications like fluid flow, velocity, and growth models.
    
**Applied Examples**

1. **Example 1**: Given $f(x)=x^2+3x$, find $f′(x)$ using the [[Power Rule]] to study velocity if $f(x)$ models displacement over time.
    
    - Solution: $f′(x)=2x+3$.
    
1. **Example 2**: For a growing radius $r$ in a circle where $\frac{dr}{dt} = 2$ cm/s, use Related Rates to find $\frac{dA}{dt}$ when $r=5$ cm, given $A = \pi r^2$.
    
    - Solution: $\frac{dA}{dt} = 2 \pi r \cdot \frac{dr}{dt} = 20 \pi$ cm²/s.