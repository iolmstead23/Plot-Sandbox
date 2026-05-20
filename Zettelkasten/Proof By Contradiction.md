Proof by contradiction (also known as reductio ad absurdum) works by:

1. Assuming the opposite of what we want to prove
2. Showing this assumption leads to a logical contradiction
3. Concluding that our original statement must be true

## Structure of a Proof by Contradiction

1. **Statement**: Start with "Suppose, for the sake of contradiction, that (opposite of what we want to prove)"
2. **Reasoning**: Follow logical steps until reaching a contradiction
3. **Contradiction**: Identify where the logic breaks known [[mathematics|mathematical]] truths
4. **Conclusion**: State that the original assumption must be false, therefore the original statement is true

## When to Use Proof by Contradiction

- Proving something is impossible
- Proving something is irrational
- Proving uniqueness
- When [[direct proof]] seems difficult or impossible
- When dealing with infinite sets

## [[Computer Science]] Applications

### 1. [[Algorithm]] Correctness

Example: Proving a sorting [[algorithm]] always terminates

- Assume it doesn't terminate
- Show this would require infinite comparisons
- Contradict the finite input size

### 2. [[Data]] Structure Properties

Example: Proving a [[binary search]] tree property

- Assume two paths to the same node exist
- Show this violates tree definition
- Conclude path must be unique

### 3. Computability Theory

Example: Proving the halting problem is undecidable

- Assume a program can solve the halting problem
- Construct a paradoxical program
- Reach a contradiction about its behavior

## Classic Examples in [[Discrete Mathematics]]

### 1. The Irrationality of √2

```
Proof:
1. Assume √2 is rational
2. Then √2 = a/b where a,b are coprime integers
3. Square both sides: 2 = a²/b²
4. Therefore: a² = 2b²
5. Therefore: a is even (a = 2k)
6. Substitute: 4k² = 2b²
7. Therefore: b is even
8. Contradiction: a and b can't both be even if coprime
9. Therefore: √2 is irrational
```

### 2. Infinite Primes

```
Proof:
1. Assume there are finitely many primes: p₁, p₂, ..., pₙ
2. Let P = (p₁ × p₂ × ... × pₙ) + 1
3. P is either prime or has a prime factor
4. Any prime factor of P differs from p₁, p₂, ..., pₙ
5. Contradiction: found a prime not in our "complete" list
6. Therefore: there are infinitely many primes
```

## Common Pattern in CS Problems

1. **State**: Clear statement of what we're proving
2. **Negate**: Form the contradiction assumption
3. **Derive**: Use logical steps, often involving:
    - [[Algorithm]] properties
    - [[Data]] structure invariants
    - Program behavior
    - Mathematical relationships
4. **Contradict**: Find where it breaks known rules
5. **Conclude**: Original statement must be true

## Tips for CS Students

1. Draw diagrams when dealing with [[data]] structures
2. Use concrete examples before attempting the proof
3. Consider algorithmic properties that must hold
4. Look for violations of:
    - [[Time complexity]] bounds
    - Space constraints
    - Invariant properties
    - Logic rules

## Common Mistakes to Avoid

1. Not clearly stating what you're assuming for contradiction
2. Finding a contradiction to something other than your assumption
3. Not showing the logical steps clearly
4. Circular reasoning
5. Not identifying the exact point of contradiction

## Verification Checklist

- [ ]  Clear contradiction assumption stated
- [ ]  Each step logically follows
- [ ]  Contradiction clearly identified
- [ ]  No circular reasoning
- [ ]  Conclusion properly stated
- [ ]  All variables and terms defined
- [ ]  Logical implications explained

Remember: In [[computer science]], proof by contradiction is particularly useful when dealing with impossibility results, uniqueness properties, and [[algorithm]] correctness. The technique helps us understand why certain things must be true by showing that the alternative is impossible.