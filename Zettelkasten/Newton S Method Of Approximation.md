**Newton's Method**, also known as the Newton-Raphson method, is an iterative technique for finding approximate roots (solutions) of a real-valued [[function]]. It is named after [[Isaac Newton]] and Joseph Raphson. It is particularly useful when solving nonlinear equations or finding points where a [[function]] equals zero. The method applies [[Differentiation|differentiation]] by iterating closer to a root using the [[function]]'s [[Derivative|derivative]].

Newton's method is a root-finding [[algorithm]] that uses the tangent line of a [[function]] at a given point to find better approximations of the [[function]]'s roots, while [[linear approximation]] estimates the value of a [[function]] near a specific point using its tangent line. Both methods rely on the concept of using a linear [[function]] to approximate a more complex [[function]], but Newton's method specifically focuses on finding roots.

For a [[function]] $f(x)$, an initial guess $x_1$ is selected, and then the [[sequence]] of approximations is given by the formula:$$x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$$
This formula adjusts the current guess $x_n$ to a better approximation $x_{n+1}$ by moving down the tangent line from $x_n$ to the $x$-axis.

### How Newton's Method Works

1. **Start with an initial guess** $x_1$ close to the root.
2. **Compute the next approximation** using $x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$.
3. **Iterate** until the difference between $x_{n+1}$ and $x_n$ is sufficiently small, indicating that the approximation has stabilized near the actual root.

The method converges quickly if the initial guess is close to the root and $f(x)$ is well-behaved around that root. However, Newton's Method may diverge or converge slowly if these conditions aren’t met.

### Historical Background

Newton's Method was introduced by Sir [[Isaac Newton]] in the 17th century. Though Newton is credited with its discovery, the method was later generalized and independently rediscovered by Joseph Raphson, leading to the combined name "Newton-Raphson Method."

### Example

Let’s find an approximation for the root of $f(x) = x^2 - 5$, starting with an initial guess $x_1 = 2$.

1. **Define** $f(x) = x^2 - 5$ and $f'(x) = 2x$.
2. **Apply Newton's formula**: $$x2=x1−f(x1)f′(x1)=2−\frac {4−5}{4}=2.25$$
3. **Continue iterating** if a more precise approximation is required.