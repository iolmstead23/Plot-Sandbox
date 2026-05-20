The **Laws of Propositional Logic** provide rules for manipulating logical statements (propositions) to simplify expressions and prove logical equivalences. These laws are essential in reasoning, proof construction, and designing digital circuits. The laws are taught in [[Discrete Mathematics]]

#### Key Laws and Their Descriptions:

1. **Identity Laws**
    
    - $P \land \text{True} \equiv P$
    - $P \lor \text{False} \equiv P$
    - A proposition combined with a neutral element (True for AND, False for OR) retains its original value.

1. **Domination Laws**
    
    - $P \lor \text{True} \equiv \text{True}$
    - $P \land \text{False} \equiv \text{False}$
    - A proposition combined with an extreme element (True for OR, False for AND) is dominated by that element.

1. **Idempotent Laws**
    
    - $P \land P \equiv P$
    - $P \lor P \equiv P$
    - Repeating a proposition with AND or OR does not change its value.

1. **Double Negation Law**
    
    - $\neg(\neg P) \equiv P$
    - Negating a negation returns the original proposition.

1. **Commutative Laws**
    
    - $P \lor Q \equiv Q \lor P$
    - $P \land Q \equiv Q \land P$
    - The order of operands in AND or OR does not matter.

1. **Associative Laws**
    
    - $(P \lor Q) \lor R \equiv P \lor (Q \lor R)$
    - $(P \land Q) \land R \equiv P \land (Q \land R)$
    - Grouping of operands in AND or OR does not matter.

1. **Distributive Laws**
    
    - $P \land (Q \lor R) \equiv (P \land Q) \lor (P \land R)$
    - $P \lor (Q \land R) \equiv (P \lor Q) \land (P \lor R)$
    - Distributes AND over OR and vice versa.

1. **Absorption Laws**
    
    - $P \lor (P \land Q) \equiv P$P∨(P∧Q)≡P
    - $P \land (P \lor Q) \equiv P$
    - A proposition absorbs redundant terms involving itself.

1. **[[DeMorgan's Laws]]**
    
    - $\neg(P \land Q) \equiv \neg P \lor \neg Q$
    - $\neg(P \lor Q) \equiv \neg P \land \neg Q$
    - Negations can be distributed across AND/OR with complementary operations.

1. **Negation Laws**
    
    - $P \lor \neg P \equiv \text{True}$
    - $P \land \neg P \equiv \text{False}$
    - A proposition combined with its negation always results in a tautology (OR) or a contradiction (AND).

1. **Implication Laws**
    
    - $P \rightarrow Q \equiv \neg P \lor Q$
    - $\neg(P \rightarrow Q) \equiv P \land \neg Q$
    - Implications can be expressed using OR and negation.

1. **Equivalence Laws**
    
    - $P \leftrightarrow Q \equiv (P \land Q) \lor (\neg P \land \neg Q)$
    - $\neg(P \leftrightarrow Q) \equiv (P \land \neg Q) \lor (\neg P \land Q)$
    - Logical equivalence relates to matching truth values.

#### Applications:

1. **Proof Simplification:**
    - These laws are used to rewrite logical expressions for easier manipulation in [[proofs]].
2. **Digital Logic Design:**
    - Foundational for building and optimizing logical circuits.
3. **Programming:**
    - Helps simplify conditional statements in [[Algorithm|algorithms]].
4. **[[Set Theory]] and [[Probability]]:**
    - Analogous rules apply in set operations and [[probability]] theory.