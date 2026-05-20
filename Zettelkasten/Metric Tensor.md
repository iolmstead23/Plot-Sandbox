The metric [[tensor]], often denoted as $g_{\mu\nu}$ or $g_{ij}$, is a fundamental mathematical object that defines the [[geometry]] of a space. It is a symmetric rank-2 [[tensor]] that allows us to measure distances, angles, and volumes in curved spaces. The metric [[tensor]] is essential in differential [[geometry]], general relativity, and many areas of theoretical physics.

## Basic Properties

The metric [[tensor]] has several fundamental properties:

1. [[Symmetry]]: $g_{\mu\nu} = g_{\nu\mu}$
2. Non-degeneracy: The determinant of $g_{\mu\nu}$ is non-zero
3. Local invertibility: There exists an inverse metric [[tensor]] $g^{\mu\nu}$ such that $g_{\mu\rho}g^{\rho\nu} = \delta^\nu_\mu$

## Distance and Length

The metric [[tensor]] defines the infinitesimal distance element $ds$ between two nearby points in a space: $ds^2 = g_{\mu\nu}dx^\mu dx^\nu$

For a curve parameterized by $\lambda$, the length is given by: $L = \int \sqrt{g_{\mu\nu}\frac{dx^\mu}{d\lambda}\frac{dx^\nu}{d\lambda}}d\lambda$

## Examples of Metric Tensors

### Euclidean Space

In three-dimensional Euclidean space with Cartesian coordinates, the metric [[tensor]] is: $g_{ij} = \begin{pmatrix} 1 & 0 & 0 \ 0 & 1 & 0 \ 0 & 0 & 1 \end{pmatrix}$

### Spherical Coordinates

In spherical coordinates $(r,\theta,\phi)$, the metric [[tensor]] is: $g_{ij} = \begin{pmatrix} 1 & 0 & 0 \ 0 & r^2 & 0 \ 0 & 0 & r^2\sin^2\theta \end{pmatrix}$

### Minkowski Spacetime

In special relativity, the Minkowski metric describes flat spacetime: $g_{\mu\nu} = \begin{pmatrix} -c^2 & 0 & 0 & 0 \ 0 & 1 & 0 & 0 \ 0 & 0 & 1 & 0 \ 0 & 0 & 0 & 1 \end{pmatrix}$

## Applications in General Relativity

In general relativity, the metric [[tensor]] describes the gravitational field and determines the [[geometry]] of spacetime. The Einstein field equations relate the metric [[tensor]] to the distribution of matter and energy: $R_{\mu\nu} - \frac{1}{2}Rg_{\mu\nu} + \Lambda g_{\mu\nu} = \frac{8\pi G}{c^4}T_{\mu\nu}$

### Schwarzschild Metric

The Schwarzschild metric describes the [[geometry]] around a spherically symmetric mass: $ds^2 = -(1-\frac{2GM}{rc^2})c^2dt^2 + (1-\frac{2GM}{rc^2})^{-1}dr^2 + r^2(d\theta^2 + \sin^2\theta d\phi^2)$

## Geodesics

Geodesics, the shortest paths between points in a curved space, are determined by the metric [[tensor]] through the geodesic equation: $\frac{d^2x^\mu}{d\tau^2} + \Gamma^\mu_{\alpha\beta}\frac{dx^\alpha}{d\tau}\frac{dx^\beta}{d\tau} = 0$

where $\Gamma^\mu_{\alpha\beta}$ are the Christoffel symbols derived from the metric: $\Gamma^\mu_{\alpha\beta} = \frac{1}{2}g^{\mu\nu}(\partial_\alpha g_{\beta\nu} + \partial_\beta g_{\alpha\nu} - \partial_\nu g_{\alpha\beta})$

## Covariant [[derivative|Derivatives]]

The metric [[tensor]] allows us to define covariant derivatives, which generalize ordinary derivatives to curved spaces: $\nabla_\mu V^\nu = \partial_\mu V^\nu + \Gamma^\nu_{\mu\lambda}V^\lambda$

## Applications in Differential [[Geometry]]

The metric [[tensor]] is fundamental in Riemannian [[geometry]], where it defines:

1. The Riemann curvature [[tensor]]: $R^\rho_{\sigma\mu\nu}$
2. The Ricci [[tensor]]: $R_{\mu\nu} = R^\rho_{\mu\rho\nu}$
3. The [[scalar]] curvature: $R = g^{\mu\nu}R_{\mu\nu}$

These quantities describe the intrinsic [[geometry]] of a manifold and are essential in both pure [[mathematics]] and theoretical physics.