ordering of distinct objects

Permutations are arrangements of a set of elements where the order of the elements matters. They fall under the category of **[[Combinatorics]]** in [[Discrete Mathematics]], which deals with counting, arrangement, and combination of elements.

### **Definition**

A **permutation** of a set of $n$ distinct elements is any ordered arrangement of these elements. The total number of permutations of $n$ elements is given by:

$P(n) = n!$

where $n!$ (n factorial) is the product of all positive integers up to $n$:

$n! = n \cdot (n-1) \cdot (n-2) \cdot \ldots \cdot 1$

### **Permutations of a Subset**

If you want to arrange $r$ elements chosen from $n$ distinct elements, the number of permutations is given by:

$P(n, r) = \frac{n!}{(n-r)!}$

- $N$: Total number of elements.
- $r$: Number of elements chosen for the arrangement.

### **Applications in [[Discrete Mathematics]]**

1. **Counting Problems**:
    
    - Permutations are used to count possible arrangements in scheduling, seating, and organizing items.

2. **[[Probability]]**:
    
    - In [[probability]] theory, permutations help calculate outcomes where order affects the result.

3. **Cryptography**:
    
    - Arrangements of symbols in permutations are critical in generating [[encryption]] keys.

4. **[[Algorithm]] Design**:
    
    - Permutations are essential in [[Algorithm|algorithms]] that deal with exhaustive search and [[optimization]].

### **Properties of Permutations**

1. **Order Matters**:
    
    - Changing the order of elements creates a different permutation.

1. **Factorial Growth**:
    
    - The number of permutations grows very quickly as $n$ increases.

1. **Distinct Elements**:
    
    - Permutations assume all elements are distinct unless specified otherwise.

### **Examples**

1. **All Elements**:
    
    - How many ways can you arrange 3 letters {A,B,C}\{A, B, C\}{A,B,C}?
    - Total arrangements: $3! = 3 \cdot 2 \cdot 1 = 6$.
    - Possible permutations: $\{ABC, ACB, BAC, BCA, CAB, CBA\}$.

1. **Subset of Elements**:
    
    - How many ways can you arrange 2 letters chosen from $\{A, B, C\}$?
    - Use $P(3, 2) = \frac{3!}{(3-2)!} = \frac{3 \cdot 2 \cdot 1}{1} = 6$.
    - Possible permutations: $\{AB, AC, BA, BC, CA, CB\}$.