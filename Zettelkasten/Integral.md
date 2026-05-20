Integration is a fundamental concept in [[calculus]] that allows us to find the accumulated value of a [[function]], such as area under a curve or total distance traveled. Integration essentially reverses the process of [[differentiation]], helping us find the original [[function]], or _[[antiderivative]]_, from a rate of change.

To perform integration, we first seek the [[antiderivative]] of a [[function]], which requires [[differentiation]]. By finding this, we obtain a [[function]] whose [[derivative]] gives us the original [[function]]. Integration, therefore, allows us to solve for unknowns that describe cumulative effects, like area or volume, from the rate-based functions we encounter.
### Applications in [[Calculus]] and Modern Uses

Integration is widely used in [[calculus]] for applications such as calculating areas, volumes, displacement, and work done by a force. Here are some specific examples of modern applications:

- **Physics**: Integration allows physicists to calculate the area under force-displacement graphs to determine work, or to find electric and magnetic fields over surfaces and volumes.
    
- **Engineering**: Engineers use integrals to analyze signals in electrical circuits, model systems in control theory, and calculate structural loads in civil engineering.
    
- **Economics**: In economics, integration helps to find consumer and producer surplus by determining the area between supply and demand curves.
### [[Definite And Indefinite Integral]]

1. **Indefinite Integral**: This represents a family of antiderivatives without specific bounds, denoted as: $$\int f(x) dx=F(x)+C$$
    where $F(x)$ is the [[antiderivative]] of $f(x)$, and $C$ is the constant of integration.
    
2. **Definite Integral**: This integral calculates the exact accumulated value between specific limits $a $and $b$, denoted as: $$\int_a^b f(x) dx=F(b)−F(a)$$
    where $F(x)$ is the [[antiderivative]] of $f(x)$, and $a$ and $b$ are the integration limits. Definite integrals are commonly used to find areas under curves and volumes of solids.

### Rules for Finding Antiderivatives

To find an [[antiderivative]], we apply the rules of [[differentiation]] in reverse. Here are some key integration rules used in [[calculus]]:

- **[[Power Rule]]**: For $f(x)=xn$ where $n≠−1$, $$\int_x^n x^n dx= \frac{x^{n+1}}{n+1}+C$$
- **[[Sum And Difference Rule]]**: The integral of a sum/difference is the sum/difference of the integrals, $$\int [f(x)±g(x)] dx=\int f(x) dx±∫g(x) dx$$
- **Constant Multiple Rule**: Constants can be factored out of the integral,
$$k \times f(x) dx=k \times \int f(x) dx$$
- **Exponential Rule**: For $f(x)=e^x$, $$\int e^x dx = e^x + C$$
- **Trigonometric Functions**: Common integrals for trigonometric functions include:
$$ \int sin⁡(x) dx=−cos⁡(x)+C$$
$$ \int cos(x) dx=sin(x)+C$$