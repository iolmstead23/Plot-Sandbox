Hash tables are fundamental [[data structure|data structures]] that implement an associative array abstract [[data]] type, providing a mapping between keys and values. At their core, they use a hash [[function]] to compute an index into an array where the desired value can be found. The essential principle lies in the transformation of keys into array indices through the process of hashing, enabling average case $O(1)$ [[time complexity]] for insertions, deletions, and lookups.

## [[hash function|Hash Functions]]

A [[Zettelkasten/Hash Function]] $h(k)$ maps a key $k$ to an integer in the range $[0, m-1]$, where $m$ is the size of the hash table. The ideal [[Zettelkasten/Hash Function]] should be uniform, deterministic, and efficient to compute. One common method is the division method, where:

$h(k) = k \bmod m$

For string keys, a popular approach is the [[polynomial]] [[Zettelkasten/Hash Function]]:

$h(string) = \sum_{i=0}^{n-1} string[i] \cdot p^i \bmod m$

where $p$ is a prime number and $string[i]$ represents the i-th character's [[ASCII]] value.

## Collision Resolution

Hash collisions occur when different keys hash to the same index. Two primary methods address this challenge:

### Chaining

In chaining, each array element contains a linked list of elements that hash to that index. The load factor $\alpha$ represents the average number of elements per bucket:

$\alpha = \frac{n}{m}$

where $n$ is the number of stored elements and $m$ is the table size. The expected search time in a chained hash table is $O(1 + \alpha)$.

### Open Addressing

Linear probing explores consecutive slots until finding an empty one:

$h(k,i) = (h'(k) + i) \bmod m$

where $i$ represents the probe number and $h'(k)$ is the initial hash. Quadratic probing uses quadratic [[polynomial]] exploration:

$h(k,i) = (h'(k) + c_1i + c_2i^2) \bmod m$

## Applications in Different Fields

### [[Database]] Systems

Hash tables form the backbone of [[database]] [[indexing]] structures, particularly for equality queries. They enable rapid access to records based on primary keys, facilitating efficient JOIN operations and query [[optimization]]. The concept extends to [[distributed databases]] through consistent hashing, where:

$position = hash(key) \bmod 2^m$

### Cryptography

Cryptographic hash functions extend basic hashing principles to create secure, one-way functions. These functions must satisfy additional properties including pre-image resistance and collision resistance. The output size influences security, typically following:

$security_bits = \log_2(2^n/P_{collision})$

where $n$ is the hash length in bits.

### [[Compiler]] Design

Symbol tables in compilers utilize hash tables for storing identifier [[information]] during compilation. The efficiency of symbol lookup directly impacts compilation speed. Scope management often employs nested hash tables, where each scope level maintains its own table.

### Cache Systems

Modern CPU cache systems employ hash tables for virtual memory page tables. The translation lookaside buffer (TLB) uses a specialized hash table structure where:

$page_number = \lfloor \frac{virtual_address}{page_size} \rfloor$

### [[Machine Learning]]

Feature hashing, or the "hashing trick," reduces [[dimensionality]] in [[machine learning]] applications. For a feature [[vector]] $x$, the hashed feature space is computed as:

$\phi_j(x) = \sum_{i:h(i)=j} x_i$

where $h$ is the [[hash function]] mapping original features to a smaller dimension.

## Performance Analysis

The average-case [[time complexity]] for basic operations assumes simple uniform hashing:

- Insertion: $O(1)$
- Deletion: $O(1)$
- Lookup: $O(1)$

The worst-case scenario occurs with many collisions, degrading to:

- Chaining: $O(n)$
- Open Addressing: $O(n)$

The [[space complexity]] is $O(n)$ where $n$ is the number of stored elements. The actual memory overhead varies by implementation, typically:

$memory = m \cdot (size_{entry} + overhead_{implementation})$

## Advanced Concepts

### Dynamic Resizing

Hash tables maintain efficiency through dynamic resizing when the load factor exceeds a threshold. The process typically involves:

1. Creating a new table of size $m' = 2m$
2. Recomputing hash values for all elements
3. Transferring elements to the new table

The amortized cost analysis shows that despite occasional $O(n)$ resize operations, the average cost per operation remains $O(1)$.

### Perfect Hashing

For static sets, perfect hashing achieves guaranteed $O(1)$ lookup time. Two-level universal hashing creates a collision-free structure where:

$h(k) = ((ak + b) \bmod p) \bmod m$

with carefully chosen parameters $a$, $b$, and prime $p$.