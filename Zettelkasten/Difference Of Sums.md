The **Difference of Sums** is a technique in [[algebra]] used to evaluate the difference between two summation expressions, often represented as:

$S_n = \sum_{i=1}^n a_i \quad \text{and} \quad T_n = \sum_{i=1}^n b_i$

The **difference** is expressed as:

$D_n = S_n - T_n = \sum_{i=1}^n (a_i - b_i)$

This method is useful for simplifying problems involving sequences, series, or comparing cumulative totals.
### **General Formula**

Given two series:

$S_n = \sum_{i=1}^n a_i \quad \text{and} \quad T_n = \sum_{i=1}^n b_i$,

the difference can be written as:

$D_n = \sum_{i=1}^n (a_i - b_i)$

This equation allows you to compare terms $a_i$ and $b_i$​ directly term by term.

### **Applications**

1. **Analyzing Sequences:**
    
    - Used to determine how two sequences differ cumulatively over a range of values.
2. **Finding Patterns:**
    
    - Identifies recurring differences or trends between two series, aiding in predicting future values.
3. **Simplification in Summations:**
    
    - Helps break down complex summation problems by comparing related sums.
4. **Evaluating Finite Differences:**
    
    - Applies in numerical methods or [[calculus]] for approximating derivatives using discrete sums.

### **Worked Examples**

#### Example 1: Simple Series Difference

Evaluate the difference:

$\sum_{i=1}^5 (2i) - \sum_{i=1}^5 (i^2)$

Step 1: Break into separate sums:

$\sum_{i=1}^5 (2i - i^2)$

Step 2: Simplify term by term:

$(2(1) - 1^2) + (2(2) - 2^2) + (2(3) - 3^2) + (2(4) - 4^2) + (2(5) - 5^2)$

Result:

$1 + 0 - 3 - 8 - 15 = -25$
#### Example 2: Continuous Sum Differences

Find $D_n = \sum_{i=1}^n i - \sum_{i=1}^n (i-1)$

Step 1: Substitute the terms:

$\sum_{i=1}^n (i - (i-1))$

Step 2: Simplify:

$\sum_{i=1}^n 1 = n$

The difference is simply $n$.
### **Tips and Tricks**

1. **Compare Formulas First**:
    
    - Before calculating sums, look for simplifications in the difference $a_i - b_i$.
2. **Use Standard Formulas**:
    
    - For common series like $\sum i$ or $2\sum i^2$, use their standard formulas:$$\sum_{i=1}^n i = \frac{n(n+1)}{2}, \quad \sum_{i=1}^n i^2 = \frac{n(n+1)(2n+1)}{6}$$
1. **Factor and Combine**:
    
    - If $a_i$ and $b_i$​ share terms, factor them to simplify the difference.
### **Applications in Real-World Problems**

- **Economics**: Comparing cumulative revenues and expenses over time.
- **Physics**: Summing forces or energy differences in discrete systems.
- **Data Analysis**: Evaluating differences in cumulative trends between datasets.