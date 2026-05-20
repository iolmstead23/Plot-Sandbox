**Existential [[Quantifier]] $\exists$**

- Symbol: $\exists$
- Meaning: "There exists" or "There is at least one."
- Example: $\exists x \, P(x)$ means "There exists an $x$ such that $P(x)$ is true."
- Truth Condition: $\exists x \, P(x)$ is true if there is at least one element in the [[domain]] for which $P(x)$ is true.

#### **Existential [[Quantifier]] $\exists x$**

If $P(a)$ and $P(b)$ are the truth values for $P(x)$:

| $P(a)$ | $P(b)$ | $\exists x \, P(x)$ |
| ------ | ------ | ------------------- |
| T      | T      | T                   |
| T      | F      | T                   |
| F      | T      | T                   |
| F      | F      | F                   |

- $\exists x \, P(x)$ is true if at least one of $P(a)$ or $P(b)$ is true.

**Existential [[Quantifier]] Example**:

- [[Domain]]: $\{1, 2, -1\}$.
- Predicate: $P(x): x < 0$.
- Statement: $\exists x \, (x < 0)$.
- Since $-1 < 0$, $\exists x \, P(x)$ is true.