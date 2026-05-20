A Markov Chain represents a mathematical system that transitions between different states according to probabilistic rules, where the next state depends only on the current state and not on the [[sequence]] of events that preceded it. This fundamental property, known as the Markov property, makes these chains powerful tools for modeling various real-world processes in fields ranging from economics to biology.

## Mathematical Foundation

The formal definition of a Markov Chain involves a set of states S and a transition [[matrix]] P where each entry $p_{ij}$ represents the [[probability]] of transitioning from state i to state j. The mathematical representation follows:

$P(X_{n+1} = j | X_n = i, X_{n-1} = i_{n-1}, ..., X_0 = i_0) = P(X_{n+1} = j | X_n = i) = p_{ij}$

The transition probabilities must satisfy two fundamental properties:

$p_{ij} \geq 0$ for all i, j (non-negativity)

$\sum_{j} p_{ij} = 1$ for all i (row sums equal one)

## State Classifications

States in a Markov Chain exhibit specific properties that determine the long-term behavior of the system. A state j is accessible from state i if there exists a positive [[probability]] of reaching j from i in a finite number of steps. The formal expression is:

$P(X_n = j | X_0 = i) > 0$ for some n ≥ 0

Several important state classifications emerge from these relationships:

Recurrent states return to themselves with [[probability]] 1, while transient states may never return. A state i is recurrent if:

$\sum_{n=1}^{\infty} P(X_n = i | X_0 = i) = \infty$

Periodic states return at regular intervals, while aperiodic states do not exhibit this behavior. The period d of a state is defined as:

$d = gcd{n > 0 : P(X_n = i | X_0 = i) > 0}$

## Steady State Analysis

The steady state or stationary distribution π represents the long-term probabilities of being in each state. It satisfies the equation:

$\pi = \pi P$

where π is a row [[vector]] and P is the transition [[matrix]]. Additionally:

$\sum_{i} \pi_i = 1$

For an irreducible and aperiodic Markov Chain, the steady state distribution exists and is unique, providing crucial insights into the system's long-term behavior.

## Applications in Various Fields

### Finance and Economics

In financial modeling, Markov Chains help analyze market trends and credit ratings. Credit rating transitions often follow Markovian behavior, where the [[probability]] of a rating change depends only on the current rating. The transition [[matrix]] represents the probabilities of moving between different credit ratings over a specified time period.

### Biology and Genetics

Population genetics employs Markov Chains to model gene frequencies across generations. The Wright-Fisher model, a fundamental concept in population genetics, uses Markov Chains to describe the random sampling of alleles from one generation to the next. The states represent different allele frequencies in the population.

### [[Computer Science]]

Web page ranking [[Algorithm|algorithms]], including early versions of Google's PageRank, utilize Markov Chains to model user browsing behavior. Each web page represents a state, and the transition probabilities correspond to the likelihood of users following links between pages. The steady state distribution provides insights into page importance.

## Hidden Markov Models

Hidden Markov Models (HMMs) extend the basic Markov Chain concept by incorporating hidden states that are not directly observable. The system produces observable outputs according to state-dependent [[probability]] distributions. The mathematical framework includes:

Emission probabilities: $P(O_t | X_t)$ State transition probabilities: $P(X_{t+1} | X_t)$

These models find extensive applications in speech recognition, biological [[sequence]] analysis, and pattern recognition.

## Computational Methods

Several [[Algorithm|algorithms]] facilitate practical applications of Markov Chains:

Forward-backward [[algorithm]]: Computes the [[probability]] of an observation [[sequence]] and hidden state [[sequence]] in HMMs.

Viterbi [[algorithm]]: Finds the most likely [[sequence]] of hidden states given observed outputs:

$V_{t,k} = \max_{x_{1:t-1}} P(x_{1:t-1}, x_t = k, y_{1:t})$

Baum-Welch algorithm: Estimates HMM parameters through expectation-maximization.

## Continuous-Time Markov Chains

Continuous-time Markov Chains extend the discrete-time framework to processes where transitions can occur at any time. The transition rates between states are described by a generator [[matrix]] Q, where:

$q_{ij} \geq 0$ for i ≠ j $q_{ii} = -\sum_{j≠i} q_{ij}$

The steady-state equations become:

$\pi Q = 0$

## Advanced Concepts

### Absorption Probabilities

For Markov Chains with absorbing states, we can calculate the [[probability]] of absorption and the expected time until absorption. The fundamental [[matrix]] N = (I - Q)^(-1) provides these insights, where Q represents the transition probabilities between transient states.

### Time Reversibility

A Markov Chain is time-reversible if it appears statistically identical whether run forward or backward in time. Mathematically, this requires:

$\pi_i p_{ij} = \pi_j p_{ji}$ for all i, j

### Ergodicity

An ergodic Markov Chain converges to its stationary distribution regardless of the initial state. This property requires the chain to be irreducible and aperiodic. The [[convergence]] rate depends on the second-largest eigenvalue of the transition [[matrix]].