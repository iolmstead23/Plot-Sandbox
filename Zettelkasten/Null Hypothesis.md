The null hypothesis (H₀) represents a statement of no effect, no difference, or no relationship between variables in a statistical test. This concept forms the cornerstone of statistical inference and hypothesis testing. It serves as the default position that researchers attempt to reject through [[statistics|statistical ]]evidence.

## Principles of Hypothesis Testing

### Framework Components

A complete hypothesis testing framework includes:

1. Null Hypothesis (H₀): The statement of no effect
2. Alternative Hypothesis (H₁ or Hₐ): The research hypothesis
3. Test Statistic: A mathematical measure used to assess the evidence
4. Critical Region: The values of the test statistic that lead to rejection
5. Significance Level (α): The [[probability]] of Type I error

The [[mathematics|mathematical ]]framework for hypothesis testing involves calculating a test statistic:

$t = \frac{\bar{x} - \mu_0}{s/\sqrt{n}}$

where $\bar{x}$ is the sample mean, $\mu_0$ is the hypothesized population mean, $s$ is the sample standard deviation, and $n$ is the sample size.

## Types of Errors

### Type I Error (α)

The [[probability]] of rejecting H₀ when it is true: $P(\text{Type I Error}) = P(\text{Reject } H_0 | H_0 \text{ is true}) = \alpha$

### Type II Error (β)

The [[probability]] of failing to reject H₀ when it is false: $P(\text{Type II Error}) = P(\text{Fail to reject } H_0 | H_0 \text{ is false}) = \beta$

## [[statistics|Statistical]] Power

Statistical power (1 - β) represents the [[probability]] of correctly rejecting a false null hypothesis. It depends on:

- Sample size
- Effect size
- Significance level (α)
- Population variability

## P-values and Decision Making

The p-value represents the [[probability]] of obtaining test results at least as extreme as those observed, assuming the null hypothesis is true. The decision rule is:

If p-value ≤ α, reject H₀ If p-value > α, fail to reject H₀

## Common Statistical Tests

### Z-test

Used when population standard deviation is known: $Z = \frac{\bar{x} - \mu_0}{\sigma/\sqrt{n}}$

### T-test

Used when population standard deviation is unknown: $t = \frac{\bar{x} - \mu_0}{s/\sqrt{n}}$

### Chi-square test

For categorical [[data]]: $\chi^2 = \sum \frac{(O_i - E_i)^2}{E_i}$

## Practical Considerations

### Sample Size Determination

Sample size affects the power of the test. The minimum sample size can be calculated using: $n = \frac{2(Z_{\alpha/2} + Z_\beta)^2\sigma^2}{\Delta^2}$

where Δ is the minimum detectable difference.

### Effect Size

Effect size quantifies the magnitude of the difference or relationship being tested. Common measures include Cohen's d and Pearson's r.

## Modern Approaches and Criticisms

Recent developments in statistical thinking have led to:

- Emphasis on confidence intervals
- Use of effect sizes
- Consideration of practical significance
- Movement toward Bayesian approaches
- Replication crisis awareness