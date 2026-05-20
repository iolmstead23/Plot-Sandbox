#### Definition:
The **Sum and Difference Rule** in [[differentiation]] is a fundamental method that allows us to differentiate functions composed of sums or differences of terms. This rule simplifies the [[differentiation]] process by enabling us to handle each term of the [[function]] individually.

#### The Rule:
If $f(x) = g(x) + h(x)$ or $f(x) = g(x) - h(x)$, then:
$$\frac{d}{dx}[f(x)] = \frac{d}{dx}[g(x)] + \frac{d}{dx}[h(x)] \quad \text{(for sums)}$$
$$\frac{d}{dx}[f(x)] = \frac{d}{dx}[g(x)] - \frac{d}{dx}[h(x)] \quad \text{(for differences)}.$$

This means that [[differentiation]] distributes over addition and subtraction.

#### Why It Works:
The Sum and Difference Rule is a direct consequence of the **linearity** of derivatives, which states that the [[derivative]] of a sum or difference of functions is the sum or difference of their derivatives.

#### Steps to Differentiate Using the Rule:
1. **Break down the [[function]]** into individual terms.
2. **Differentiate each term** separately.
3. **Combine the results** using addition or subtraction.

#### Example 1: Differentiating a [[Polynomial]]
Let $f(x) = x^3 + 2x^2 - 4x + 7$.  
Using the Sum and Difference Rule:
$$\frac{d}{dx}[f(x)] = \frac{d}{dx}[x^3] + \frac{d}{dx}[2x^2] - \frac{d}{dx}[4x] + \frac{d}{dx}[7].$$
Calculating each term:
- $\frac{d}{dx}[x^3] = 3x^2$
- $\frac{d}{dx}[2x^2] = 4x$
- $\frac{d}{dx}[4x] = 4$
- $\frac{d}{dx}[7] = 0$

Result:
$$\frac{d}{dx}[f(x)] = 3x^2 + 4x - 4.$$
#### Example 2: Differentiating a Trigonometric [[Function]]
Let $f(x) = \sin(x) - \cos(x) + x^2$.  
Using the Sum and Difference Rule:
$$\frac{d}{dx}[f(x)] = \frac{d}{dx}[\sin(x)] - \frac{d}{dx}[\cos(x)] + \frac{d}{dx}[x^2].$$
Calculating each term:
- $\frac{d}{dx}[\sin(x)] = \cos(x)$
- $\frac{d}{dx}[\cos(x)] = -\sin(x)$
- $\frac{d}{dx}[x^2] = 2x$

Result:
$$\frac{d}{dx}[f(x)] = \cos(x) + \sin(x) + 2x.$$
#### Applications:
1. **Antiderivatives and Integration**:  
   The Sum and Difference Rule is the basis for integrating functions term by term. For example:
   $$\int (x^2 + 3x - 4) \, dx = \int x^2 \, dx + \int 3x \, dx - \int 4 \, dx.$$
   Each term is integrated separately.

2. **Physics**:  
   Used to differentiate motion equations to find velocity or acceleration when position functions are given as sums of terms.

3. **Economics**:  
   Applied in marginal analysis when differentiating cost, revenue, or profit functions.

#### Key Takeaways:
- The Sum and Difference Rule simplifies [[differentiation]] for complex functions.
- Each term of the [[function]] can be treated independently.
- This rule is foundational for handling derivatives in higher [[mathematics]] and applied fields.