# PyGravitas

> An interactive 2D N-body physics sandbox built with Python, Pygame, NumPy, and SciPy.

---

[IMAGE PLACEHOLDER: A GIF of the final simulation will go here once the project is complete.]

## About The Project

`PyGravitas` is a portfolio project that simulates the gravitational interaction of N bodies in a 2D "sandbox" environment.

The project's key features include:
* **Vectorized Physics:** All physics calculations are vectorized using `NumPy` for high performance, allowing for thousands of interacting particles.
* **Accurate Integration:** The simulation uses `scipy.integrate.solve_ivp` to solve the system of ordinary differential equations, providing a stable and accurate solution (as opposed to a simpler, less stable Euler integrator).
* **Interactive GUI:** Built with `Pygame`, the simulation is fully interactive. Users can add particles, create "attractors," and reset the environment.

### Physics Implementation: Unit Normalization

A critical design choice was made to handle the physical constants. Since the simulation uses **pixels** for distance and abstract values (e.g., 1-10) for mass, using the standard SI Gravitational Constant ($G_{SI} \approx 6.674 \times 10^{-11} \frac{\text{m}^3}{\text{kg} \cdot \text{s}^2}$) would result in forces and accelerations that are effectively zero.

To achieve visible, dynamic movement, we employ **Unit Normalization**. This means we define a custom unit system where:

* **1 unit of distance** = 1 pixel
* **1 unit of mass** = 1 abstract unit (from `MASS_LOWER_BOUND` to `MASS_UPPER_BOUND`)
* **1 unit of time** = 1 second

#### Deriving a "Designer G"

We must define a **scaled gravitational constant, $G_{scaled}$**, that produces a visually compelling acceleration. We can find a reasonable starting value by working backward from a *desired acceleration*.

1.  **The Goal:** We want a noticeable acceleration, e.g., **$a = 100$ pixels/$s^2$**.
2.  **The Formulas:** We start with Newton's second law and our scaled law of gravitation:
    * $a = F / m_1$
    * $F = G_{scaled} \frac{m_1 m_2}{r^2}$
3.  **Combine & Solve:** By substituting $F$, we can solve for $G_{scaled}$:
    * $a = (G_{scaled} \frac{m_1 m_2}{r^2}) / m_1$
    * $a = G_{scaled} \frac{m_2}{r^2}$
    * **$G_{scaled} = a \frac{r^2}{m_2}$**
4.  **Calculate:** We plug in our *desired* and *typical* values:
    * Desired acceleration $a = 100$ pixels/$s^2$
    * A typical mass $m_2 = 1$ unit
    * A typical distance $r = 100$ pixels

$$G_{scaled} = 100 \frac{(100)^2}{1} = 1,000,000$$

This value (e.g., `G_SCALED = 1_000_000.0` in `constants.py`) provides a strong starting point. It is tuned experimentally to ensure the resulting acceleration ($a = G_{scaled} \cdot m/r^2$) produces immediate, observable changes in velocity on the screen, making the simulation interactive and dynamic.

## Physics & Numerical Stability

Creating a stable N-body simulation requires addressing inherent numerical challenges. `PyGravitas` implements standard scientific computing techniques to ensure physical accuracy and energy conservation.

### Periodic Boundary Conditions (PBCs)
To avoid the energy discontinuities caused by particles bouncing off "hard" screen edges, the simulation employs a toroidal topology.

1.  **Coordinate Wrapping:** Particles that exit one side of the simulation domain $L$ instantly re-enter from the opposite side, maintaining continuous velocity.
    $$x_{wrapped} = x \pmod L$$
2.  **Minimum Image Convention:** To ensure energy conservation, particles must always interact via the shortest path on the torus. The distance vector $\Delta \vec{x}$ between two particles $i$ and $j$ is adjusted so that no component exceeds $L/2$:
    $$\Delta x_{mic} = \Delta x - L \cdot \text{nint}\left(\frac{\Delta x}{L}\right)$$
    *(Where $\text{nint}$ is the nearest integer function)*. This ensures a particle near the right edge correctly feels a strong force from a particle near the left edge, as they are topologically adjacent.

### Gravitational Softening
In a pure Newtonian model, the force $F \propto 1/r^2$ approaches infinity as the distance $r \to 0$. In a discrete-time simulation, these close encounters cause massive, unphysical force spikes that break energy conservation (the "slingshot" effect).

To prevent this, we employ a softened gravitational force. By adding a softening parameter $\epsilon^2$ to the denominator, we effectively treat particles as having a finite size, capping the maximum force during overlaps:

$$\vec{F} = -G_{scaled} \frac{m_1 m_2}{r^2 + \epsilon^2} \hat{r}$$

Where:
* $r$ is the distance between particles.
* $\hat{r}$ is the unit vector pointing from particle 1 to particle 2.
* $\epsilon$ is the softening length (tuned to approx. $1/2$ particle radius).

## Built With

* [Python 3.10](https://www.python.org/)
* [Pygame](https://www.pygame.org/)
* [NumPy](https://numpy.org/)
* [SciPy](https://scipy.org/)

## License

Distributed under the MIT License. See `LICENSE` for more information.