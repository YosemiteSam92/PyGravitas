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

## Built With

* [Python 3.10](https://www.python.org/)
* [Pygame](https://www.pygame.org/)
* [NumPy](https://numpy.org/)
* [SciPy](https://scipy.org/)

## License

Distributed under the MIT License. See `LICENSE` for more information.