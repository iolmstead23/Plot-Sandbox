A directed [[graph]], also known as a digraph, is a mathematical structure consisting of vertices (nodes) and edges, where each edge has a specific direction indicating a one-way relationship between two vertices. Unlike [[undirected graphs]], where edges represent symmetric relationships, directed graphs capture asymmetric relationships between entities. Formally, a directed [[graph]] $G$ is defined as an ordered pair $G = (V, E)$, where $V$ is a set of vertices and $E$ is a set of ordered pairs $(u, v)$ representing directed edges from [[vertex]] $u$ to [[vertex]] $v$.

## Mathematical Properties and Representations

The mathematical representation of directed graphs can take several forms. The most common representations include adjacency matrices and adjacency lists. For a directed [[graph]] with $n$ vertices, the [[adjacency matrix]] $A$ is an $n \times n$ [[matrix]] where $A_{ij} = 1$ if there exists a directed edge from [[vertex]] $i$ to [[vertex]] $j$, and $A_{ij} = 0$ otherwise. The in-degree of a [[vertex]] $v$, denoted as $d^-(v)$, represents the number of edges entering $v$, while the out-degree $d^+(v)$ represents the number of edges leaving $v$. A fundamental property of directed graphs is that the sum of all in-degrees equals the sum of all out-degrees: $\sum_{v \in V} d^-(v) = \sum_{v \in V} d^+(v) = |E|$.

## Applications in [[Computer Science]]

Directed graphs serve as fundamental [[data structure|data structures]] in [[computer science]], particularly in [[algorithm]] design and system modeling. In [[Networks|network]] routing [[Algorithm|algorithms]], directed graphs represent one-way connections between [[Networks|network]] nodes, with edge weights often indicating transmission costs or bandwidths. The shortest path problem, solved using [[Algorithm|algorithms]] like [[Dijkstra's algorithm]], operates on directed graphs where the shortest path from [[vertex]] $s$ to [[vertex]] $t$ may differ from the path from $t$ to $s$. The [[time complexity]] of [[Dijkstra's algorithm]] on a directed [[graph]] is $O(|V|^2)$ with a basic implementation, or $O(|E| + |V|\log|V|)$ using a priority queue.

## Applications in [[Linear Algebra]]

In [[linear algebra]], directed graphs provide a visual representation of linear transformations and [[matrix]] operations. A transition [[matrix]] $P$ in Markov chains can be represented as a directed [[graph]] where edge weights correspond to transition probabilities, satisfying $\sum_{j} P_{ij} = 1$ for each row $i$. The [[Eigenvalues And Eigenvectors]] of the [[adjacency matrix]] reveal important structural properties of the directed [[graph]], including its connectivity and periodicity. The spectral radius $\rho(A)$, which is the largest eigenvalue in absolute value, provides insights into the [[graph]]'s growth rate and stability properties.

## Applications in [[Discrete Mathematics]]

[[Discrete mathematics]] employs directed graphs to model logical relationships and dependencies. In [[Boolean Algebra]], directed graphs represent implication relationships between propositions. A directed acyclic [[graph]] (DAG) is particularly important in modeling partial orders and dependencies, where cycles are prohibited. The topological sorting of a DAG produces a linear ordering of vertices such that for every directed edge $(u, v)$, [[vertex]] $u$ comes before [[vertex]] $v$ in the ordering. This has applications in scheduling, dependency resolution, and program compilation.

## Applications in [[Calculus]]

In [[calculus]] and [[differentiation|differential equations]], directed graphs model state transitions and flow [[networks]]. [[Vector]] fields can be discretized and represented as directed graphs, where edges indicate the direction of flow or gradient. The [[divergence]] of a [[vector]] field at a [[vertex]] $v$ can be approximated by the difference between its out-degree and in-degree: $div(F) \approx \frac{d^+(v) - d^-(v)}{\Delta x}$. In numerical analysis, directed graphs help visualize the stability of numerical methods through their dependency structures.

## Real-world Applications

Directed graphs find extensive applications across various domains. In social [[networks]], directed edges represent one-way relationships like "follows" or "influences." In transportation systems, they model one-way streets and traffic flow patterns. In [[project management]], PERT charts use directed graphs to represent task dependencies, with critical path analysis identifying the [[sequence]] of tasks that determine the minimum project completion time. In biology, metabolic [[networks]] use directed graphs to represent chemical reaction pathways, where edges indicate the transformation of one molecule into another.

## Advanced Topics and Analysis

The study of directed graphs extends to advanced concepts such as strongly connected components, [[graph]] condensation, and flow [[networks]]. A strongly connected component is a maximal subset of vertices where every [[vertex]] is reachable from every other [[vertex]]. Tarjan's algorithm finds strongly connected components in $O(|V| + |E|)$ time. The max-flow min-cut theorem, applicable to directed graphs with edge capacities, states that the maximum flow from source to sink equals the minimum cut capacity, expressed as $max_flow(s,t) = min_cut(s,t)$.