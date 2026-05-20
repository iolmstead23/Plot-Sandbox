## Complete [[Graph]] $K_n$

A complete [[graph]] represents a [[networks|network]] where every [[vertex]] connects directly to every other [[vertex]]. Mathematically represented as $K_n$, this [[graph]] ensures maximum connectivity among $n$ vertices. Each [[vertex]] has a degree of $n-1$, creating a fully interconnected structure. Complete graphs are fundamental in combinatorial [[mathematics]] and [[Networks|network]] theory.

## Cycle [[Graph]] $C_n$

Cycle graphs form a circular [[networks|network]] where vertices are connected sequentially, with the last [[vertex]] connecting back to the first. Denoted as $C_n$, these graphs create a ring-like structure where each [[vertex]] has exactly two edges. In a cycle [[graph]] with $n$ vertices, the total number of edges equals the number of vertices, maintaining a symmetric circular pattern.

## Hypercube [[Graph]] $Q_n$

Hypercube graphs represent complex multidimensional [[Networks|network]] structures. For an $n$-dimensional hypercube $Q_n$:

- Total vertices: $2^n$
- [[Vertex]] labeling uses binary strings of length $n$
- Edges connect vertices differing by single bit position
- Demonstrates recursive geometric connectivity

## Bipartite [[Graph]] $K_{n,m}$

Bipartite graphs divide vertices into two disjoint sets with specific connection rules:

- Total vertices: $n + m$
- No edges within same [[vertex]] set
- Every [[vertex]] in one set connects to all vertices in the other set
- Represents systems with two distinct, interconnected groups

### Mathematical Properties

- Complete [[graph]] $K_n$: $\binom{n}{2}$ total edges
- Cycle [[graph]] $C_n$: Symmetric circular structure
- Hypercube $Q_n$: $n \cdot 2^{n-1}$ total edges
- Bipartite [[graph]] $K_{n,m}$: $n \cdot m$ total edges