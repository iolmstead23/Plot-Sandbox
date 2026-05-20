## General Description

A function is a mathematical relationship that maps each element of a set (the [[domain]]) to exactly one element of another set (the codomain). Formally, a function $f:A→B$ assigns to each $x∈A$ a unique $f(x)∈B$. Functions can be injective (one-to-one), surjective (onto), or bijective (both). In programming, functions encapsulate reusable logic, such as `def square(x): return x**2`. In [[calculus]], functions are used to model relationships between variables, and their derivatives ($f′(x)= \frac {dx}{df}$​) measure the rate of change. In [[machine learning]], activation functions like ReLU ($f(x)=max(0,x)$) introduce non-linearity into [[neural network|neural networks]]. In cryptography, hash functions map inputs to fixed-size outputs, ensuring [[data]] integrity. Functions are also central to [[graph theory]], where adjacency functions describe connections between nodes. Examples of functions include linear functions ($f(x)=mx+b$), exponential growth ($f(t)=Aekt$), and sigmoid functions ($f(x)=1+e−x1​$). Functions are a unifying concept across [[mathematics]], [[computer science]], and engineering, providing a framework for modeling and solving problems.
## Key Characteristics

1. **[[Domain]]**: Set of all possible input values
2. **Codomain**: Set of all possible output values
3. **Range**: Actual set of outputs produced

## Types of Functions

1. **Injective (One-to-One)**: Each element in the codomain is mapped to by at most one element in the [[domain]]
    - Mathematically: $\forall a,b \in X, f(a) = f(b) \implies a = b$
2. **Surjective (Onto)**: Every element in the codomain is mapped to by at least one element in the [[domain]]
3. **Bijective**: Function that is both injective and surjective

## Applications in Different Fields

### [[Mathematics]]

- **[[Discrete Mathematics]]**:
    - [[Set Theory]] representation
    - Mapping relationships
    - Proof techniques
    - Equation: $f(x) = {(x,y) | \text{relationship between x and y}}$

### [[Computer Science]]

- **[[Algorithm]] Design**:
    - Function mapping for computational processes
    - Input-output transformations
    - Mapping [[algorithm]] complexity
    - Equation: $T(n) = f(n)$ ([[Time Complexity]] function)

### Physics

- **Modeling Physical Systems**:
    - Describing motion
    - Energy transformations
    - Equation: $F(x) = ma$ (Force function)

### Engineering

- **Signal Processing**:
    - Transfer functions
    - System behavior analysis
    - Equation: $H(s) = \frac{Y(s)}{X(s)}$ (Transfer function)

### Economics

- **Economic Modeling**:
    - Supply and demand curves
    - Cost and revenue functions
    - Equation: $P(q) = f(\text{quantity})$ (Price function)

### [[Statistics]]

- **[[Probability]] Distributions**:
    - Mapping random variables
    - Calculating probabilities
    - Equation: $P(X = x) = f(x)$ ([[Probability]] density function)

## Important Functional Properties

1. **Continuity**: Function without abrupt changes
    - Equation: $\forall \epsilon > 0, \exists \delta > 0$ such that $|x-a| < \delta \implies |f(x) - f(a)| < \epsilon$
2. **Monotonicity**: Preserving order of inputs
    - Increasing: $x_1 < x_2 \implies f(x_1) \leq f(x_2)$
    - Decreasing: $x_1 < x_2 \implies f(x_1) \geq f(x_2)$

## [[Calculus]]-Specific Function Concepts

- **[[Derivative]]**: Rate of change
    - Equation: $f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$
- **[[Integral]]**: Accumulation of quantities
    - Equation: $\int_{a}^{b} f(x) dx$