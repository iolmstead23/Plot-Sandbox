A geometric [[sequence]] is a [[sequence]] of numbers where each term after the first is found by multiplying the previous term by a fixed, non-zero number called the common ratio. This fundamental mathematical concept appears throughout various fields, from pure [[mathematics]] to applied sciences. The [[sequence]] can be represented as $a, ar, ar^2, ar^3, ..., ar^{n-1}$, where $a$ is the first term, $r$ is the common ratio, and $n$ is the position of the term. This is different than an [[Arithmetic Sequence]] in which $d$ is a sum not a product.

## Core Concepts

### Definition and Basic Properties

The general term (nth term) of a geometric [[sequence]] is given by: $a_n = a_1r^{n-1}$ where $a_1$ is the first term and $r$ is the common ratio. The common ratio can be found by dividing any term by its preceding term: $r = \frac{a_{n+1}}{a_n}$

### Geometric Series

The sum of terms in a geometric [[sequence]] forms a geometric series. For a finite geometric series with $n$ terms, the sum is given by: $S_n = a\frac{1-r^n}{1-r}$ when $r \neq 1$ $S_n = na$ when $r = 1$

For infinite geometric series where $|r| < 1$, the sum is: $S_{\infty} = \frac{a}{1-r}$

## Applications in [[Computer Science]]

### [[Algorithm]] Analysis

Geometric sequences appear in analyzing [[Algorithm|algorithms]] with logarithmic complexity. When studying divide-and-conquer [[Algorithm|algorithms]], the problem size often reduces by a constant factor at each step, forming a geometric [[sequence]]. [[Binary search]] trees demonstrate this with their height-based operations following geometric patterns.

### [[data structure|Data Structures]]

In [[data structure]] design, geometric sequences help analyze [[space complexity]]. Dynamic arrays often grow geometrically, typically doubling in size when capacity is reached. This growth pattern ensures amortized constant-time insertions.

### [[Computer]] Graphics

Geometric sequences are fundamental in [[computer]] graphics for creating scaling effects, zoom operations, and fractal generation. The scaling factor between successive levels of detail often follows a geometric progression.

## Applications in [[Linear Algebra]]

### [[Matrix]] Operations

Geometric sequences emerge in [[matrix]] powers, where a [[matrix]] $A$ is repeatedly multiplied by itself: $A, A^2, A^3, ..., A^n$. The entries of these [[matrix]] powers often form geometric sequences, particularly when dealing with eigenvalues and diagonalization.

### [[vector space|Vector Spaces]]

In [[vector space]] transformations, geometric sequences appear when studying scaling transformations. A linear transformation that scales vectors by a constant factor creates geometric progressions in the coordinates of transformed vectors.

## Applications in [[Calculus]]

### Infinite Series

Geometric series are crucial in [[calculus]] for understanding [[convergence]] and [[divergence]]. They serve as the simplest example of infinite series and provide a foundation for more complex series analysis. The ratio test for series [[convergence]] directly relates to geometric sequences.

### Exponential Functions

The exponential [[function]] $e^x$ can be expressed as an infinite series where the coefficients follow patterns related to geometric sequences: $e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + ...$

### Integration Techniques

When integrating functions involving exponentials or powers, geometric sequences often appear in the resulting series expansions. This is particularly evident in power series solutions to differential equations.

## Real-World Applications

### Finance

Geometric sequences model compound interest, where interest is earned on both principal and previously accumulated interest. The growth of investments over time often follows geometric patterns.

### Population Growth

Biological populations under ideal conditions often exhibit geometric growth patterns. Each generation multiplies by a constant factor, creating a geometric [[sequence]] of population sizes.

### Physics

Wave propagation and decay processes often follow geometric sequences. The amplitude of damped oscillations typically decreases geometrically with each cycle. Radioactive decay chains can be modeled using geometric sequences.