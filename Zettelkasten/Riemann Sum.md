### Riemann Sums: Overview

Riemann Sums are a foundational method in [[calculus]] used to approximate the area under a curve for a given [[function]]. Named after the 19th-century German mathematician Bernhard Riemann, this method was a major advancement in [[integral]] [[calculus]], providing a formal way to approximate and eventually calculate definite integrals. Riemann's work laid the groundwork for rigorous definitions of integration, focusing on partitioning intervals into smaller subintervals and summing areas of rectangles to approximate the total area under a curve. His approach fundamentally changed how mathematicians approach continuous functions and calculate areas, volumes, and other cumulative quantities.
### The Concept of Riemann Sums

A Riemann Sum is based on approximating the area under a curve for a [[function]] $f(x)$ on a closed interval $[a, b]$. This interval is divided into $n$ subintervals of equal width, denoted by $\Delta x$, where $\Delta x = \frac{b - a}{n}$.

For each subinterval, a sample point $x_i^*$ is chosen within each interval, and the [[function]] is evaluated at these points. The general form of a Riemann Sum is:
$$\sum_{i=1}^{n} f(x_i^*) \Delta x$$
By adding the areas of each rectangular segment, we approximate the area under the curve.

- **Left Riemann Sum**: Uses the left endpoint of each subinterval as $x_i^*$.
- **Right Riemann Sum**: Uses the right endpoint of each subinterval as $x_i^*$.
- **Midpoint Riemann Sum**: Uses the midpoint of each subinterval as $x_i^*$.

### Finding the Area as $\Delta x$ Becomes Infinitesimal

To get an exact area under the curve, we take the limit of the Riemann Sum as $n \to \infty$, which makes $\Delta x$ infinitesimally small. This leads to the concept of a definite [[integral]]:

$$lim⁡n→∞∑i=1nf(xi∗)Δx= \int_a^bf(x) dx$$
Here, the [[integral]] symbol $\int$ represents the limit of the Riemann Sum, and $dx$ represents an infinitesimally small width.
### Application and Example

Let’s approximate the area under $f(x) = x^2$ on $[0, 1]$ using a Riemann Sum.

1. Divide the interval into $n$ subintervals, each of width $\Delta x = \frac{1 - 0}{n} = \frac{1}{n}$.
2. Choose sample points $x_i = \frac{i}{n}$ (right endpoints).
3. Plugging into the Riemann Sum formula, we get:
$$\sum_{i=1}^{n} \left( \frac{i}{n} \right)^2 \cdot \frac{1}{n}$$

To find the area exactly, take the limit as $n \to \infty$:
$$\lim_{n \to \infty} \sum_{i=1}^{n} \left( \frac{i}{n} \right)^2 \cdot \frac{1}{n} = \int_{0}^{1} x^2 \, dx = \frac{1}{3}$$
### Historical Background

Bernhard Riemann (1826-1866) developed the concept of Riemann Sums while studying integrable functions. His method allowed mathematicians to rigorously define the area under curves, even for non-smooth functions. Riemann’s work extended the scope of [[integral]] [[calculus]] by showing how to sum over infinite intervals and apply this concept across continuous domains, influencing both pure and applied [[mathematics]].