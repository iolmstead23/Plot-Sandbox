Distance formulas are mathematical equations that allow us to calculate the spatial separation between two points in various coordinate systems and dimensional spaces. These formulas are fundamental to many fields, from pure [[mathematics]] to applied sciences, and form the backbone of computational [[geometry]], [[Computer]] graphics, and spatial analysis.

## Euclidean Distance

### Two-Dimensional Space

The most familiar distance formula is the Euclidean distance in two-dimensional space, derived from the [[Pythagorean theorem]]. For two points $P_1(x_1, y_1)$ and $P_2(x_2, y_2)$, the distance is: $d = \sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}$

This formula calculates the length of the straight line connecting two points in a plane. The result represents the shortest possible path between the points in Euclidean space.

### Three-Dimensional Space

In three-dimensional space, the Euclidean distance formula extends to include the z-coordinate. For points $P_1(x_1, y_1, z_1)$ and $P_2(x_2, y_2, z_2)$: $d = \sqrt{(x_2-x_1)^2 + (y_2-y_1)^2 + (z_2-z_1)^2}$

### N-Dimensional Space

The general form for n-dimensional Euclidean space is: $d = \sqrt{\sum_{i=1}^n (p_i - q_i)^2}$ where $p_i$ and $q_i$ are the coordinates in the $i$th dimension.

### [[Hamming Distance]]

The [[Hamming distance]] measures the number of positions at which two sequences of equal length differ. Originally developed for detecting and correcting errors in [[data]] transmission, it has found wide applications in information theory and [[computer science]]. For two strings $s_1$ and $s_2$ of equal length, the [[Hamming distance]] is: $d_H(s_1, s_2) = \sum_{i=1}^n [s_1(i) \neq s_2(i)]$

where $[s_1(i) \neq s_2(i)]$ equals 1 if the elements at position i differ, and 0 if they are the same. For binary strings, this can be implemented using the XOR operation: $d_H(s_1, s_2) = \sum_{i=1}^n (s_1(i) \oplus s_2(i))$

The [[Hamming distance]] is particularly useful in:

- Error detection and correction in communication systems
- DNA [[sequence]] analysis for measuring genetic differences
- Pattern recognition and [[machine learning]] for comparing feature vectors
- Information theory for analyzing code properties

### Jaccard Distance

The Jaccard distance measures dissimilarity between sample sets and is defined as the complement of the Jaccard coefficient. For two sets A and B, the Jaccard distance is: $d_J(A,B) = 1 - J(A,B) = 1 - \frac{|A \cap B|}{|A \cup B|}$

The Jaccard distance has several important properties:

- It ranges from 0 (identical sets) to 1 (completely different sets)
- It satisfies the triangle inequality
- It is particularly useful for sparse [[Data]] and binary features

Applications of Jaccard distance include:

- Document similarity analysis in text mining
- Recommender systems for comparing user preferences
- Image similarity assessment in computer vision
- Species distribution comparison in ecology
- [[Networks|Network]] analysis for comparing node neighborhoods

## Manhattan Distance

Also known as taxicab distance or L1 norm, Manhattan distance measures the path between points along a grid-like path. For two points in two-dimensional space: $d = |x_2-x_1| + |y_2-y_1|$

This metric is particularly useful in urban planning and routing [[Algorithm|algorithms]] where movement is restricted to a grid pattern. In n-dimensional space, it becomes: $d = \sum_{i=1}^n |p_i - q_i|$

## Minkowski Distance

The Minkowski distance is a generalization that includes both Euclidean and Manhattan distances as special cases. For two points in n-dimensional space: $d = (\sum_{i=1}^n |p_i - q_i|^p)^{\frac{1}{p}}$

where p is the order parameter:

- p = 1 gives Manhattan distance
- p = 2 gives Euclidean distance
- p = ∞ gives Chebyshev distance

## Applications in [[Computer Science]]

### [[Computer]] Graphics

Distance formulas are essential in [[Computer]] graphics for collision detection, ray tracing, and object placement. The choice of distance metric affects rendering performance and visual accuracy. [[euclidean geometry|Euclidean]] distance is commonly used for realistic 3D graphics, while Manhattan distance might be preferred for tile-based games.

### [[Machine Learning]]

In clustering [[Algorithm|algorithms]] and nearest neighbor calculations, distance metrics help determine similarity between [[data]] points. Different distance formulas can lead to different clustering results, making the choice of metric crucial for [[algorithm]] performance.

### Computational [[Geometry]]

Distance calculations are fundamental in computational [[geometry]] for problems like finding closest pairs of points, constructing Voronoi diagrams, and computing convex hulls.

## Applications in [[Data]] Analysis

### Feature Scaling

Distance metrics help in normalizing [[data]] features and computing similarities between [[data]] points. The choice of distance formula affects how differences between features are weighted and compared.

### Cluster Analysis

Different distance metrics lead to different clustering results. Euclidean distance is common for continuous [[data]], while Manhattan distance might be more appropriate for high-dimensional spaces.

## Applications in Physics

### [[Vector]] Analysis

Distance formulas are crucial in [[vector]] calculations, particularly in field theories and particle physics. The choice of metric affects how physical quantities are measured and compared.

### Quantum Mechanics

Distance metrics appear in quantum mechanical calculations, particularly in computing [[probability]] distributions and wave [[function]] analysis.

## Special Considerations

### Normalization

When working with different scales or units, normalization is often necessary before applying distance formulas: $d_{normalized} = \sqrt{\sum_{i=1}^n (\frac{p_i - q_i}{s_i})^2}$ where $s_i$ is the scale factor for dimension i.

### Weighted Distance

In some applications, different dimensions may have different importance. This leads to weighted distance formulas: $d_{weighted} = \sqrt{\sum_{i=1}^n w_i(p_i - q_i)^2}$ where $w_i$ represents the weight for dimension i.

## Real-World Applications

### Geographic [[Information]] Systems

Distance calculations are fundamental in GIS for computing routes, coverage areas, and spatial analysis. The choice between great circle distance and Euclidean distance depends on the scale of the geographic area.

### Robotics

Robot navigation requires continuous distance calculations for path planning and obstacle avoidance. The choice of distance metric affects path [[optimization]] and motion planning strategies.