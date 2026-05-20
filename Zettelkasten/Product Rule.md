The Product Rule is a [[Differentiation|differentiation]] in [[Calculus|calculus]] method used to find the [[Derivative|derivative]] of a [[function]] that is the product of two differentiable functions. If you have two functions, $f(x)$ and $g(x)$, their product is $h(x) = f(x) \cdot g(x)$. The Product Rule states that the [[derivative]] of $h(x)$ with respect to $x$ is:

$h'(x) = f(x) \cdot g'(x) + g(x) \cdot f'(x)$

This rule applies when both $f(x)$ and $g(x)$ are functions of $x$ and both are differentiable. Rather than trying to directly differentiate the product $f(x) \cdot g(x)$, the rule simplifies the process by breaking it down into components: the [[derivative]] of $f(x)$ while keeping $g(x)$ constant, and vice versa.
### Why the Product Rule Works

The Product Rule essentially separates the process of [[differentiation]] into two parts, accounting for the changing rate of each [[function]] within the product. It is a direct application of the limit definition of a [[derivative]], helping to calculate the combined rate of change when two functions are multiplied together.
### Example

For instance, consider differentiating $h(x) = x^2 \cdot e^x$. Let $f(x) = x^2$ and $g(x) = e^x$. Then, the Product Rule gives:

$h'(x) = f(x) \cdot g'(x) + g(x) \cdot f'(x)$

Substitute in the derivatives:

1. $f(x) = x^2 \Rightarrow f'(x) = 2x$
2. $g(x) = e^x \Rightarrow g'(x) = e^x$

Then:

$h'(x) = x^2 \cdot e^x + e^x \cdot 2x = e^x(x^2 + 2x)$