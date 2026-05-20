Integration by Parts is a [[Calculus]] technique used to evaluate integrals where the standard methods (e.g., substitution) are not directly applicable. It is derived from the [[product rule]] for [[differentiation]].
#### **Formula**

The formula for Integration by Parts is:$$\int u \, dv = u \, v - \int v \, du$$
Here:

- $u$: A [[function]] chosen to differentiate ($u \to du$).
- $dv$: A [[function]] chosen to integrate ($dv \to v$).
#### **Steps to Apply Integration by Parts**

1. **Choose $u$ and $dv$:**  
    Use the **LIATE** rule as a guideline for selecting $u$:
    
    - $L$: Logarithmic ($\ln x$)
    - $I$: Inverse trigonometric ($\arctan x, \arcsin x, \dots$)
    - $A$: Algebraic ($x, x^2,\dots$)
    - $T$: Trigonometric ($\sin x, \cos x, \dots$)
    - $E$: Exponential ($e^x, 2^x, \dots$)
    
    Choose $u$ from higher priority in this list and $dv$ as the rest of the [[function]].
    
2. **Differentiate $u$:** 
    Compute $du = \frac{du}{dx}$.
    
3. **Integrate $dv$:**  
    Compute $v = \int dv$.
    
4. **Substitute into the formula:**  
    Substitute $u, v$ and $\int v \, du$ into the Integration by Parts formula.
    
5. **Simplify and evaluate the remaining [[integral]]:**  
    Repeat the process if the resulting [[integral]] is still complex.
#### **Examples**

1. **Example 1: Simple [[Polynomial]] and Exponential** Evaluate $\int x \, e^x \, dx$.
    
    - Let $u = x$, so $du = dx$.
    - Let $x \, dv = e^x \, dx$.
    
    Using the formula:
    
    $\int x \, e^x \, dx = u \, v - \int v \, du = x \, e^x - \int e^x \, dx$.
    
    Simplify:
    
    $\int x \, e^x \, dx = x \, e^x - e^x + C$.
    
    Final Answer:
    
    $\boxed{x \, e^x - e^x + C}$.
    
1. **Example 2: Logarithmic [[Function]]** Evaluate $\int \ln x \, dx$.
    
    - Let $u = \ln x$, so $du = \frac{1}{x} \, dx$.
    - Let $dv = dx$, so $v = x$.
    
    Using the formula:
    
    $\int \ln x \, dx = u \, v - \int v \, du = x \, \ln x - \int x \cdot \frac{1}{x} \, dx$.
    
    Simplify:
    
    $\int \ln x \,dx = x \ln x - \int 1 \, dx = x \ln x - x + C$.
    
    Final Answer:
    
    $\boxed{x \ln x - x + C}$.
#### **Common Applications**

1. **Repeated Integration by Parts:**  
    Sometimes the remaining [[integral]] requires further application of Integration by Parts, e.g., $\int x^2 \, e^x \, dx$.
    
2. **Reduction Formulae:**  
    Some integrals can be expressed recursively, e.g., $\int x^n e^x \, dx$ or $\int \sin^n x \, dx$.
    
3. **Definite Integrals:**  
    Integration by Parts can be applied to definite integrals. Be sure to evaluate the $uv$ term at the limits.