**Definition:**  
Boolean Algebra is a branch of [[mathematics]] that deals with binary variables and logical operations. It provides the foundation for digital logic design and computational logic. In Boolean Algebra, values are typically represented as 000 (False) and 111 (True).

### Features:

1. **Binary Operations:**
    
    - **AND $(\land)$:** $A \land B = 1$ if both $A$ and $B$ are 111.
    - **OR $(\lor)$:** $A \lor B = 1$ if at least one of $A$ or $B$ is 111.
    - **NOT $(\neg)$:** $\neg A = 1$ if $A = 0$, and $\neg A = 0$ if $A = 1$.

1. **Duality Principle:**  
    Each Boolean expression remains valid if $\land$ and $\lor$ are interchanged, and 000 and 111 are swapped.

3. **Boolean Laws:**
    
    - **Identity Laws:** $A \land 1 = A$, $A \lor 0 = A$.
    - **Domination Laws:** $A \land 0 = 0$, $A \lor 1 = 1$.
    - **Idempotent Laws:** $A \land A = A$, $A \lor A = A$.
    - **Distributive Laws:** $A \land (B \lor C) = (A \land B) \lor (A \land C)$.
    - **[[DeMorgan's Laws]]:**  
        $\neg (A \land B) = \neg A \lor \neg B$,  
        $\neg (A \lor B) = \neg A \land \neg B$.
### Uses:

1. **Digital Logic Design:**  
    Boolean Algebra is the basis for designing digital circuits, including AND, OR, and NOT gates in computing [[hardware]].
    
2. **Programming and [[Algorithm|Algorithms]]:**  
    Logical operators in programming languages are derived from Boolean Algebra.
    
3. **[[Set Theory]]:**  
    Boolean operations mirror set operations like union $(\lor)$, intersection $(\land)$, and complement $(\neg)$.
    
4. **Propositional Logic:**  
    Boolean Algebra simplifies logical expressions and aids in proving logical equivalences.
    
5. **Error Detection and Correction:**  
    Applications in coding theory rely on Boolean principles for developing efficient error-checking mechanisms.

### Example: Simplifying Boolean Expressions

**Expression:** $(A \land 1) \lor (A \land 0)$

**Simplification:**

$(A \land 1) = A \quad \text{(Identity Law)}$
$(A \land 0) = 0 \quad \text{(Domination Law)}$
$A \lor 0 = A \quad \text{(Identity Law)}$

**Result:** $A$