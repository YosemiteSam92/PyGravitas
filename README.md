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

## Built With

* [Python 3.10](https://www.python.org/)
* [Pygame](https://www.pygame.org/)
* [NumPy](https://numpy.org/)
* [SciPy](https://scipy.org/)

## License

Distributed under the MIT License. See `LICENSE` for more information.