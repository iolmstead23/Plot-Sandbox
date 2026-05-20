Proof by Cases (also known as case analysis) works by:

1. Breaking down a complex problem into exhaustive, non-overlapping cases
2. Proving the statement true for each case separately
3. Concluding the statement is true for all possibilities

## Structure of a Proof by Cases

1. **Statement**: Clearly state what needs to be proven
2. **Case Division**: List all possible cases (must be exhaustive)
3. **Individual [[Proofs]]**: Prove the statement for each case
4. **Conclusion**: Combine the cases to show the overall statement is true

## When to Use Proof by Cases

- When the problem naturally splits into distinct scenarios
- When different conditions require different approaches
- When the general proof is too complex but individual cases are manageable
- When dealing with piecewise functions or conditional statements
- When analyzing [[algorithm]] behavior under different inputs

## [[Computer Science]] Applications

### 1. [[Algorithm]] Analysis

Example: Analyzing [[time complexity]]

- Case 1: Best case scenario
- Case 2: Average case scenario
- Case 3: Worst case scenario

### 2. [[Data]] Structure Operations

Example: [[Binary Search]] Tree insertion

- Case 1: Empty tree
- Case 2: Value less than root
- Case 3: Value greater than root
- Case 4: Value equals root

### 3. Program Correctness

Example: Proving a [[function]] returns correct results

- Case 1: Input is null or empty
- Case 2: Input contains single element
- Case 3: Input contains multiple elements

## Classic Examples in [[Discrete Mathematics]]

### 1. Absolute Value Properties

Copy

```
Prove: |x| = max(x, -x)
Case 1: x ≥ 0 - When x ≥ 0, |x| = x - max(x, -x) = x since x ≥ -x Therefore |x| = max(x, -x)
Case 2: x < 0 - When x < 0, |x| = -x - max(x, -x) = -x since -x > x
Therefore |x| = max(x, -x)
Since these cases cover all possibilities, |x| = max(x, -x) is proven.
```

### 2. Divisibility Rules

Copy

```
Prove: For any integer n, n² - n is even
Case 1: n is even (n = 2k) - n² - n = (2k)² - 2k - = 4k² - 2k - = 2(2k² - k)
Therefore divisible by 2.
Case 2: n is odd (n = 2k + 1) - n² - n = (2k + 1)² - (2k + 1) - = 4k² + 4k + 1 - 2k - 1 - = 4k² + 2k - = 2(2k² + k)
Therefore divisible by 2.
```

## Common Pattern in CS Problems

1. **Identify Cases**: List all possible scenarios
2. **Verify Exhaustive**: Ensure cases cover all possibilities
3. **Check Non-overlapping**: Ensure cases are distinct
4. **Prove Each Case**: Use appropriate proof technique for each
5. **Connect Cases**: Show how cases combine to prove the whole

## Tips for CS Students

1. Draw decision trees to identify cases
2. Use pseudocode to outline different scenarios
3. Consider boundary conditions as separate cases
4. Common case divisions:
    - Positive/Zero/Negative
    - Empty/Single/Multiple
    - Even/Odd
    - Less than/Equal to/Greater than

## Proof Writing Guidelines

1. **Clear Case Statement**
    - Label each case clearly
    - State the condition defining each case
    - Show cases are exhaustive
2. **Individual Case [[Proofs]]**
    - Use appropriate proof technique for each case
    - Keep track of which case you're proving
    - Clearly mark the end of each case
3. **Case Combination**
    - Show how cases work together
    - Explain why no cases are missing
    - State final conclusion

## Common Mistakes to Avoid

1. Missing cases
2. Overlapping cases
3. Not proving cases are exhaustive
4. Using circular reasoning within cases
5. Not connecting cases to the main proof
6. Assuming what you're trying to prove in a case

## Verification Checklist

- [ ]  All cases identified
- [ ]  Cases are exhaustive (cover all possibilities)
- [ ]  Cases are mutually exclusive (don't overlap)
- [ ]  Each case properly proven
- [ ]  Cases properly combined
- [ ]  Clear conclusion stated
- [ ]  All variables and terms defined
- [ ]  Each case clearly labeled and organized

Remember: In [[computer science]], proof by cases is particularly useful when analyzing [[Algorithm|algorithms]] and [[data]] structures where behavior varies based on input conditions or structure states. The key is ensuring your cases cover all possibilities without overlap.