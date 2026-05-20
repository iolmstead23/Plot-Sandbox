**Definition:**  
An **adjacency [[Matrix]]** is a square [[matrix]] used to represent a [[graph]]. It describes the connections between vertices in the [[graph]]. For a [[graph]] $G = (V, E)$ with $n$ vertices, the adjacency [[Matrix]] $A$ is an $n \times n$ [[matrix]] where:

$$A[i][j] = \begin{cases} 1 & \text{if there is an edge from [[vertex]] } i \text{ to [[Vertex]] } j \\ 0 & \text{otherwise} \end{cases}$$
### Features:

1. **Size:**  
    The [[matrix]] has dimensions $n \times n$, where $n$ is the number of vertices.

	
2. **[[Symmetry]]:**
    - For [[undirected graphs]]: $A[i][j] = A[j][i$], making the [[matrix]] symmetric.
    - For directed graphs: No [[symmetry]] is guaranteed.


1. **Weights:**  
    In weighted graphs, $A[i][j]$ contains the weight of the edge instead of 111.


4. **Diagonal Entries:**
    - **Self-loops:** If a [[vertex]] has a loop, $A[i][i] = 1$.
    - Otherwise, the diagonal entries are $0$.

### Uses:

1. **[[Graph]] Representation:**  
    Encodes the structure of a [[graph]] for computational purposes.
    
2. **[[Graph]] [[Algorithm|Algorithms]]:**
    
    - **Shortest Path:** Input for [[Algorithm|algorithms]] like Floyd-Warshall.
    - **Counting Paths:** $A^k[i][j]$ gives the number of paths of length $k$ from [[vertex]] $i$ to [[vertex]] $j$.

1. **[[networks|Network]] Analysis:**  
    Adjacency matrices model relationships in [[networks]] like social graphs or transportation grids.
    
4. **[[Linear Algebra]] Connections:**  
    The [[matrix]] can be used for eigenvalue analysis and studying [[graph]] properties like connectivity.

### Example:

For a [[graph]] $G$ with vertices $V = \{1, 2, 3\}$ and edges $E = \{(1, 2), (2, 3), (3, 1)\}$:

$$A = \begin{bmatrix} 0 & 1 & 1 \\ 0 & 0 & 1 \\ 1 & 0 & 0 \end{bmatrix}​$$

