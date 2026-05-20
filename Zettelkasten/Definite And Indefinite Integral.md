Although the notation for indefinite integrals may look similar to the notation for a definite [[integral]], they are not the same. A **definite [[integral]]** is a number, while an **indefinite [[integral]]** is a family of functions. However, close attention should always be paid to the notation so that we know whether we’re working with a definite [[integral]] or an indefinite [[integral]].

[[Integral]] notation dates back to the late seventeenth century and is one of the contributions of [[Gottfried Wilhelm Leibniz]], who is often considered to be the co-discoverer of [[calculus]], along with [[Isaac Newton]]. The integration symbol $\int$ is an elongated "S", suggesting **sigma** or **summation**. In a definite [[integral]], the numbers $a$ and $b$ are written above and below the summation symbol and are the boundaries of the interval, $[a,b]$. The numbers $a$ and $b$ are $x$-values and are called the **limits of integration**; specifically, $a$ is the **lower limit** and $b$ is the **upper limit**.

To clarify, the word **limit** is used in two different ways in the context of the definite [[integral]]:

1. The **limit of a sum** as $n \to \infty$.
2. The **limits of integration**, which are the boundaries of the region we are working with.

The definite [[integral]] can be written as:

$\int_a^b f(x)\,dx = \int_a^b f(t)\,dt = \int_a^b f(u)\,du$

This equation shows that the variable of integration can be changed, and it doesn't affect the value of the [[integral]] as long as the [[function]] and the limits of integration remain the same.
### Continuous Functions are Integrable

If $f(x)$ is continuous on $[a,b]$, then $f$ is **integrable** on $[a,b]$. This means that the definite [[integral]] of $f(x)$ over the interval $[a,b]$ exists, and we can calculate it using the limit of Riemann sums or other integration techniques.

Functions that are not continuous on $[a,b]$ may still be integrable, depending on the nature of the discontinuities. For example, functions with a finite number of jump discontinuities on a closed interval are integrable.

It is also worth noting here that we have retained the use of a regular partition in the Riemann sums. This restriction is not strictly necessary. Any partition can be used to form a [[Riemann sum]]. However, if a nonregular partition is used to define the definite [[integral]], it is not sufficient to take the limit as the number of subintervals goes to infinity. Instead, we must take the limit as the width of the largest subinterval goes to zero. This introduces a little more complex notation in our limits and makes the calculations more difficult without really gaining much additional insight, so we stick with regular partitions for the Riemann sums.