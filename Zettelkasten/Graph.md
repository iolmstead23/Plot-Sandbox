### Graphs in [[Discrete Mathematics]]

A **graph** is a [[mathematics|mathematical]] structure consisting of a set of **vertices** (or nodes) and a set of **edges** connecting pairs of vertices. Formally, a graph $G$ is defined as $G = (V, E)$. where $V$ is the set of vertices and $E$ is the set of edges.

### Types of Graphs:

- **[[Undirected Graphs]]:** Edges have no direction, e.g. $(v_1, v_2)$.
- **Directed Graphs (Digraphs):** Edges have a direction, e.g. $v_1 \to v_2$​.
- **Weighted Graphs:** Edges have weights representing costs, distances, or other values.
- **Simple Graphs:** No loops or multiple edges between vertices.
- **Multigraphs:** May have multiple edges or loops.
- **Complete Graphs ($K_n$):** Every [[vertex]] connects to every other [[vertex]].

### Key Concepts:

- **[[Adjacency Matrix]]:** Represents graph connections in a [[matrix]] form.
- **[[Graph Isomorphism]]:** Two graphs are isomorphic if there’s a [[bijection]] between their [[vertex]] sets and edges.
- **Degree of a [[Vertex]]:** Number of edges connected to a [[vertex]] (in-degree/out-degree for digraphs).
- **Connectedness:** A graph is connected if there’s a path between every pair of vertices.
- **Planarity:** A graph is planar if it can be drawn in a plane without edge crossings.

### Applications:

1. **[[Geometry]]:** Graphs model geometric shapes, including planar graphs and tessellations.
2. **[[Topology]]:** Used to study surfaces, connectivity, and Euler characteristics.
3. **[[Computer Science]]:** [[Networks]], shortest paths (Dijkstra’s [[algorithm]]), and spanning trees.
4. **Physics and Chemistry:** Represent molecule structures or physical systems.
5. **Social Sciences:** Model relationships and interactions in social [[networks]].

### Fundamental Theorems and Properties:

1. **Euler’s Formula (for planar graphs):**  
    $V - E + F = 2$, where $V$, $E$ and $F$ are the numbers of vertices, edges, and faces.
2. **Graph Coloring:** Assigning colors to vertices such that no two adjacent vertices share the same color (e.g., Four-Color Theorem).

### Theoretical Studies:

Graphs form the basis of advanced topics, including:

- **[[Graph Theory]]:** Study of properties and types of graphs.
- **Network Theory:** Focuses on large-scale graphs like the Internet.
- **Dynamic Graphs:** Graphs that change over time, applied in simulations and modeling.