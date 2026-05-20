## General Description

An undirected [[graph]] is a [[mathematics|mathematical]] structure consisting of vertices (nodes) connected by edges, where connections have no specific direction. Formally, $G = (V, E)$ where $V$ is a set of vertices and $E$ is a set of unordered pairs of vertices representing edges.

## Key Characteristics

1. Symmetric connections between vertices
2. No directional preference in edges
3. Edges represent mutual relationships

## [[Graph]] Components

- **[[Vertex]] (Node)**: Individual point in the [[graph]]
- **Edge**: Connection between two vertices
- **Degree**: Number of edges connected to a [[vertex]]
- **Adjacent Vertices**: Directly connected by an edge

## Types of Undirected Graphs

1. **Simple [[Graph]]**: No multiple edges between vertices
2. **Complete [[Graph]]**: Every [[vertex]] connected to every other [[vertex]]
3. **Connected [[Graph]]**: Path exists between all vertices
4. **Disconnected [[Graph]]**: Some vertices cannot be reached

## Mathematical Representation

- **[[Adjacency Matrix]]**: $A_{ij} = 1$ if vertices $i$ and $j$ are connected
- **Incidence [[Matrix]]**: Represents [[vertex]]-edge relationships

## Applications in Different Fields

### [[Computer Science]]

- **[[networks|Network]] Design**
- **Routing [[Algorithm|Algorithms]]**
- **Social Network Analysis**
- Path finding and connectivity problems

### [[Mathematics]]

- **[[Graph Theory]]**
- **Combinatorial [[Optimization]]**
- **[[algebra|Algebraic Structures]]**

### Physics

- **Complex System Modeling**
- **Quantum Mechanics**
- Interaction [[networks|network]] representations

### Biology

- **Protein Interaction [[Networks]]**
- **Ecological Relationships**
- Genetic mapping

### Social Sciences

- **Social Network Analysis**
- **Communication Patterns**
- Relationship mapping

## Important [[Graph]] Metrics

- **Clustering Coefficient**: $C_i = \frac{2E_i}{k_i(k_i-1)}$
- **Path Length**: Minimum edges between vertices
- **[[Graph]] Diameter**: Maximum shortest path

## Computational Complexity

- **Breadth-First Search**: $O(V+E)$
- **Depth-First Search**: $O(V+E)$
- **Connectivity Check**: $O(V+E)$