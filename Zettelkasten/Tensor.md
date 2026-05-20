A tensor is a mathematical object that generalizes the concepts of scalars, vectors, and matrices to higher dimensions. Fundamentally, a tensor is a geometric entity that exists independently of any coordinate system and follows specific transformation rules when changing between coordinate systems. Tensors can be thought of as multi-dimensional arrays of numbers that transform in specific ways under coordinate transformations, making them essential tools in physics, engineering, and various branches of [[mathematics]].

## Tensor Order and Components

The order (or rank) of a tensor is the number of indices required to specify its components. A [[scalar]] is a tensor of rank 0, a [[vector]] is a tensor of rank 1, and a [[matrix]] is a tensor of rank 2. In general, a tensor of rank n in three-dimensional space has $3^n$ components. For example, a rank-2 tensor has 9 components ($3^2$), which can be arranged in a 3×3 [[matrix]]. The components of a tensor $T$ are typically written with indices, such as $T^{i_1i_2...i_n}_{j_1j_2...j_m}$, where superscripts represent contravariant indices and subscripts represent covariant indices.

## Tensor Operations

Several fundamental operations can be performed with tensors:

### Tensor Addition

For tensors of the same rank and dimension, addition is performed component-wise: $(A + B)^{i_1...i_n}_{j_1...j_m} = A^{i_1...i_n}_{j_1...j_m} + B^{i_1...i_n}_{j_1...j_m}$

### Tensor Multiplication

The tensor product of two tensors $A$ and $B$ creates a new tensor of rank equal to the sum of the ranks of $A$ and $B$: $(A \otimes B)^{i_1...i_n,k_1...k_p}_{j_1...j_m,l_1...l_q} = A^{i_1...i_n}_{j_1...j_m}B^{k_1...k_p}_{l_1...l_q}$

### Contraction

Contraction reduces the rank of a tensor by summing over pairs of indices. For example, contracting a rank-2 tensor yields a [[scalar]]: $T^i_i = \sum_i T^i_i$

## Transformation Properties

One of the most important properties of tensors is how they transform under coordinate transformations. For a general tensor, the transformation law is: $T'^{\mu_1...\mu_n}_{\nu_1...\nu_m} = \frac{\partial x'^{\mu_1}}{\partial x^{\alpha_1}}...\frac{\partial x'^{\mu_n}}{\partial x^{\alpha_n}}\frac{\partial x^{\beta_1}}{\partial x'^{\nu_1}}...\frac{\partial x^{\beta_m}}{\partial x'^{\nu_m}}T^{\alpha_1...\alpha_n}_{\beta_1...\beta_m}$

## Applications in Physics and Engineering

### Stress Tensor

In continuum mechanics, the stress tensor $\sigma_{ij}$ represents the internal forces within a material. Each component represents the force per unit area acting on a specific plane: $\sigma_{ij} = \begin{pmatrix} \sigma_{xx} & \sigma_{xy} & \sigma_{xz} \ \sigma_{yx} & \sigma_{yy} & \sigma_{yz} \ \sigma_{zx} & \sigma_{zy} & \sigma_{zz} \end{pmatrix}$

### Inertia Tensor

The inertia tensor $I_{ij}$ describes how an object's mass is distributed relative to its rotational axes: $I_{ij} = \int \rho(r)(r^2\delta_{ij} - x_ix_j)dV$

### Electromagnetic Field Tensor

In electromagnetism, the electromagnetic field tensor $F_{\mu\nu}$ combines the electric and magnetic fields into a single mathematical object: $F_{\mu\nu} = \begin{pmatrix} 0 & -E_x/c & -E_y/c & -E_z/c \ E_x/c & 0 & -B_z & B_y \ E_y/c & B_z & 0 & -B_x \ E_z/c & -B_y & B_x & 0 \end{pmatrix}$

## Computational Applications

In [[computer science]] and [[machine learning]], tensors are fundamental [[data structure|data structures]] used to represent multi-dimensional arrays of [[data]]. Deep learning frameworks like TensorFlow and PyTorch use tensor operations as their primary computational building blocks. The efficient manipulation of these high-dimensional [[data structure|data structures]] is crucial for modern [[machine learning]] applications.

## Einstein Notation

Einstein notation (or Einstein summation convention) is a convenient shorthand for writing tensor equations. When an index appears twice in a term, once as a superscript and once as a subscript, summation over that index is implied: $A^i_jB^j_k = \sum_j A^i_jB^j_k$