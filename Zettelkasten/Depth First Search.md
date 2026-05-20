Depth First Search represents a fundamental [[graph]] traversal [[algorithm]] that explores a [[graph]] by diving as deep as possible along each branch before backtracking. Unlike BFS's level-by-level approach, DFS plunges into the [[graph]]'s depths, systematically exploring each path to its conclusion before exploring alternatives. This distinctive exploration pattern makes DFS particularly suitable for problems involving path finding, cycle detection, and topological ordering.

## Core Concepts and Principles

### Basic [[Algorithm]] Structure

DFS explores a [[graph]] by following paths as far as possible, using a stack (either explicit or through [[recursion]]) to track the exploration path. The [[algorithm]] marks vertices as they are discovered and processed, creating a depth-first tree. The exploration process can be represented using discovery and finishing times:

$time[v] = \begin{cases} d[v] & \text{discovery time} \ f[v] & \text{finishing time} \end{cases}$

### Implementation Components

The [[algorithm]] utilizes several key components: a visited array to track explored vertices, a [[recursion]] stack (or explicit stack) for backtracking, and parent pointers for tree construction. The state of a [[vertex]] during DFS can be represented as:

$state(v) = \begin{cases} \text{WHITE} & \text{unvisited} \ \text{GRAY} & \text{discovered but not finished} \ \text{BLACK} & \text{finished} \end{cases}$

## [[Algorithm]] Implementation

### Recursive Structure

The basic recursive implementation of DFS can be expressed [[mathematics|mathematically]] as:

$DFS(G):$ 
$\text{For each vertex }v \in V:$ 
$\quad state[v] = \text{WHITE}$ 
$\quad parent[v] = \text{NIL}$

$DFS_Visit(u):$
$\quad state[u] = \text{GRAY}$ 
$\quad time = time + 1$ 
$\quad d[u] = time$ 
$\quad \text{For each }v \in Adj[u]:$ 
$\quad\quad \text{If }state[v] = \text{WHITE}:$ 
$\quad\quad\quad parent[v] = u$ 
$\quad\quad\quad DFS_Visit(v)$ 
$\quad state[u] = \text{BLACK}$ 
$\quad time = time + 1$ 
$\quad f[u] = time$

### Time and [[Space Complexity]]

The [[time complexity]] of DFS is $O(V + E)$ where V is the number of vertices and E is the number of edges. The [[space complexity]] is $O(V)$ for the [[recursion]] stack and visited array, though the actual stack depth depends on the [[graph]] structure and traversal order.

## Applications and Properties

### Cycle Detection

DFS excels at detecting cycles in directed graphs. A back edge, indicating a cycle, is identified when DFS encounters a gray [[vertex]] in its [[recursion]] stack. The cycle detection condition can be expressed as:

$\text{cycle exists if }\exists (u,v): state[v] = \text{GRAY}$

### Topological Sorting

For directed acyclic graphs (DAGs), DFS naturally produces a topological ordering by sorting vertices by decreasing finish time. The topological order τ can be expressed as:

$\tau(u) < \tau(v) \text{ if } (u,v) \text{ is an edge in the DAG}$

### Strongly Connected Components

DFS can identify strongly connected components in directed graphs through a two-pass [[algorithm]]. The process involves:

1. Running DFS to compute finishing times
2. Running DFS on the transpose [[graph]] in decreasing order of finishing times

## Advanced Applications

### Articulation Points and Bridges

DFS can identify articulation points (cut vertices) and bridges in an undirected [[graph]]. The process involves tracking discovery times and low points:

$low[v] = min\begin{cases} disc[v] \ disc[u] \text{ for any ancestor }u\text{ connected to }v \ low[w] \text{ for any child }w\text{ of }v \end{cases}$

### Biconnected Components

The [[algorithm]] can decompose a [[graph]] into its biconnected components using DFS. A [[vertex]] is an articulation point if either:

1. It is the root with multiple children
2. It has a child whose subtree cannot reach an ancestor of the [[vertex]]

## Implementation Considerations

### Stack Management

While recursive implementation is more intuitive, an explicit stack implementation might be preferred for large graphs to avoid stack overflow. The explicit stack version maintains the same properties while providing better control over memory usage:

$S = \text{empty stack}$ 
$S.push(start_vertex)$ 
$\text{While }S \text{ not empty}:$ 
$\quad v = S.top()$ 
$\quad \text{Process }v$ 
$\quad S.pop()$

### Edge Classification

DFS naturally classifies edges into four categories:

1. Tree edges: Edges in the DFS tree
2. Back edges: Edges pointing to ancestors
3. Forward edges: Non-tree edges pointing to descendants
4. Cross edges: All other edges

## Special Cases and Variations

### Iterative Deepening DFS

For situations where the search depth might be very large, iterative deepening DFS (IDDFS) provides a compromise between DFS and BFS. The depth limit increases iteratively:

$\text{For }d = 0 \text{ to }\infty:$ $\quad DFS(root, depth_limit = d)$

### Memory-Constrained Environments

In memory-constrained environments, DFS can be modified to use constant extra space by marking vertices in the [[graph]] itself or using bit manipulation techniques. This modification trades time efficiency for space efficiency.