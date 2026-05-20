Eigenvectors and eigenvalues represent fundamental concepts in [[linear algebra]] that describe special vectors and scalars associated with linear transformations. When a linear transformation is applied to an eigenvector, the [[vector]] changes only in magnitude (scaled by the eigenvalue) while maintaining its direction or becoming exactly opposite. This property makes these concepts invaluable in various fields of [[mathematics]], physics, and engineering.

## Mathematical Foundation

The fundamental equation defining eigenvectors and eigenvalues states that for a square matrix A, an eigenvector v, and an eigenvalue λ:

$Av = \lambda v$

This equation indicates that when [[matrix]] A transforms the eigenvector v, the result equals the same [[vector]] scaled by λ. More explicitly, for a non-zero [[vector]] v:

$(A - \lambda I)v = 0$

where I represents the identity matrix. This equation forms the basis for finding eigenvectors and eigenvalues.

## Computing Eigenvalues

Finding eigenvalues involves solving the characteristic equation:

$det(A - \lambda I) = 0$

For a 2×2 [[matrix]], this yields a quadratic equation. For larger matrices, the process becomes more complex, often requiring numerical methods. The degree of the characteristic [[polynomial]] equals the size of the [[matrix]], potentially yielding that many eigenvalues.

## Determining Eigenvectors

Once eigenvalues are known, eigenvectors can be found by solving:

$(A - \lambda_i I)v = 0$

This system of equations determines the direction of eigenvectors. Importantly, eigenvectors are not unique – any [[scalar]] multiple of an eigenvector is also an eigenvector for the same eigenvalue. Conventionally, eigenvectors are often normalized to have a length of 1.

## Geometric Interpretation

Geometrically, eigenvectors represent directions in which a linear transformation acts simply as a scaling operation. The corresponding eigenvalue determines whether the scaling:

- Stretches (|λ| > 1)
- Shrinks (|λ| < 1)
- Reflects (λ < 0)
- Leaves unchanged (|λ| = 1)

This geometric understanding proves crucial in applications involving rotations, reflections, and other linear transformations.

## Diagonalization

A [[matrix]] A is diagonalizable if it has n linearly independent eigenvectors (where n is the [[matrix]] dimension). When this occurs:

$A = PDP^{-1}$

where D is a diagonal [[matrix]] of eigenvalues and P contains the corresponding eigenvectors as columns. This decomposition significantly simplifies [[matrix]] operations, especially powers of matrices:

$A^k = PD^kP^{-1}$

## Properties and Theorems

Several important properties govern eigenvectors and eigenvalues:

The trace of a [[matrix]] equals the sum of its eigenvalues: $tr(A) = \sum_{i=1}^n \lambda_i$

The determinant equals the product of eigenvalues: $det(A) = \prod_{i=1}^n \lambda_i$

Eigenvectors corresponding to distinct eigenvalues are linearly independent.

## Applications in Various Fields

### [[Mathematics]]

Eigenvectors and eigenvalues play crucial roles in:

- [[Matrix]] decomposition
- Solving systems of differential equations
- [[Principal component analysis]]
- Fourier transforms

### Physics

Applications include:

- Quantum mechanics (wave functions)
- Vibration analysis
- Inertia [[tensor]] calculations
- Stability analysis

### [[Computer Science]]

Key uses involve:

- Image processing
- [[Data]] [[compression]]
- [[Machine learning]] [[Algorithm|algorithms]]
- [[Graph theory]] applications

### Engineering

Applications extend to:

- Structural analysis
- Control systems
- Signal processing
- Modal analysis

## Numerical Methods

Computing eigenvalues and eigenvectors for large matrices requires sophisticated numerical methods:

The Power Method iteratively approximates the dominant eigenvalue: $v_{k+1} = \frac{Av_k}{|Av_k|}$

QR [[Algorithm]] provides a more comprehensive approach for finding all eigenvalues:

1. Decompose $A = QR$
2. Form $A_{k+1} = RQ$
3. Iterate until [[convergence]]

## Special Cases and Considerations

### Complex Eigenvalues

When dealing with real matrices, complex eigenvalues always occur in conjugate pairs. These often represent rotational components of transformations.

### Repeated Eigenvalues

Algebraic multiplicity (repetition in characteristic equation) may differ from geometric multiplicity (dimension of eigenspace), leading to important considerations in diagonalization.

### Symmetric Matrices

Symmetric matrices have special properties:

- All eigenvalues are real
- Eigenvectors are orthogonal
- Always diagonalizable

## Practical Implementation

When working with eigenvectors and eigenvalues:

4. Verify [[matrix]] properties first
5. Choose appropriate numerical methods
6. Consider conditioning and stability
7. Validate results through verification
8. Interpret results in context