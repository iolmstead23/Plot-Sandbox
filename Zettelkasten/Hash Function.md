A hash [[function]] is a mathematical [[function]] that transforms input [[data]] of arbitrary size into a fixed-size output, typically a bit string of predetermined length. These functions play a crucial role in [[computer science]] and cryptography, serving as the backbone for [[data structure|data structures]], digital signatures, and [[data]] integrity verification. The transformation process must be deterministic, meaning the same input will always produce the same output, while maintaining efficiency in computation and uniformity in output distribution.

## Mathematical Foundation

### Basic Properties

A hash [[function]] $h$ maps an input set $X$ to an output set $Y$, formally expressed as:

$h: X \rightarrow Y$

where $|Y| < |X|$ in most practical applications. The fundamental properties include:

- Determinism: For any $x \in X$, $h(x)$ always produces the same value
- Efficiency: $h(x)$ should be computable in $O(n)$ time, where $n$ is the input size
- Uniformity: The [[probability]] of any output $y \in Y$ should be approximately $\frac{1}{|Y|}$

### Distribution Analysis

The quality of a hash [[function]] can be measured through its avalanche effect, quantified by:

$P(h_i(x) \neq h_i(x')) = \frac{1}{2}$

where $h_i$ represents the i-th bit of the hash output, and $x'$ differs from $x$ in exactly one bit.

## Common Hash [[Function]] Types

### Division Method

The simplest form of hashing uses the modulo operator:

$h(k) = k \bmod m$

where $m$ is typically chosen as a prime number to ensure better distribution. This method's simplicity makes it suitable for educational purposes and basic applications.

### Multiplication Method

Knuth's multiplication method utilizes the fractional part of multiplication:

$h(k) = \lfloor m(kA \bmod 1) \rfloor$

where $A$ is a constant in the range $(0,1)$, often chosen as $A = \frac{\sqrt{5}-1}{2}$.

### Universal Hashing

Universal hash functions provide probabilistic guarantees against collision clustering. For keys $x, y$, and hash [[function]] $h$ randomly chosen from a family $H$:

$P_{h \in H}[h(x) = h(y)] \leq \frac{1}{m}$

## Cryptographic Hash Functions

### Security Properties

Cryptographic hash functions must satisfy additional properties:

1. Pre-image resistance: Given $h(x)$, finding any $x'$ such that $h(x') = h(x)$ requires approximately $2^n$ operations
2. Second pre-image resistance: Given $x$, finding $x' \neq x$ such that $h(x') = h(x)$ requires approximately $2^n$ operations
3. Collision resistance: Finding any pair $(x,x')$ where $h(x) = h(x')$ requires approximately $2^{n/2}$ operations

The birthday paradox explains the $2^{n/2}$ bound through:

$P(collision) \approx 1 - e^{-k^2/(2n)}$

where $k$ is the number of hashed values and $n$ is the output size.

## Applications in Different Fields

### [[data structure|Data Structures]]

In hash tables, the load factor $\alpha$ affects performance:

$\alpha = \frac{n}{m}$

where $n$ is the number of stored items and $m$ is the table size. The expected number of probes in open addressing is:

$\frac{1}{1-\alpha}$

### Cryptography

Message authentication codes (MACs) combine hash functions with secret keys:

$MAC(k,m) = h(k \oplus opad , | , h(k \oplus ipad , | , m))$

where $opad$ and $ipad$ are fixed padding values.

### [[Database]] Systems

Locality-sensitive hashing (LSH) enables similar items to hash to similar values. For vectors $x$ and $y$:

$P(h(x) = h(y)) = 1 - \frac{\theta(x,y)}{\pi}$

where $\theta(x,y)$ is the angle between vectors.

### [[Computer]] Graphics

Spatial hashing maps 3D coordinates to 1D indices:

$h(x,y,z) = (x p_1 \oplus y p_2 \oplus z p_3) \bmod n$

where $p_1$, $p_2$, and $p_3$ are large [[prime numbers]].

## Performance [[Optimization]]

### Load Balancing

Dynamic perfect hashing achieves $O(1)$ worst-case lookup with two-level hashing:

$h(x) = (h_1(x) + h_2(x)) \bmod m$

where $h_1$ and $h_2$ are independently chosen universal hash functions.

### Cache Performance

Cache-conscious hashing improves locality through aligned access patterns:

$bucket = h(key) & (num_buckets - 1)$

requiring $num_buckets$ to be a power of 2.

## Modern Developments

### Quantum Resistance

Post-quantum cryptographic hash functions must resist attacks from quantum computers. The complexity of quantum attacks on collision resistance is:

$O(2^{n/3})$

using Grover's algorithm, compared to classical $O(2^{n/2})$.

### [[Machine Learning]] Applications

Feature hashing reduces [[dimensionality]] while preserving similarity:

$\phi_j(x) = \sum_{i:h(i)=j} sign(h'(i))x_i$

where $h$ and $h'$ are independent hash functions.