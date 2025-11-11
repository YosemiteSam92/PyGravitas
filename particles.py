import pygame as pg
import numpy as np
from scipy.integrate import solve_ivp
from typing import Tuple

from constants import NUM_DIM, SCREEN_WIDTH, SCREEN_HEIGHT, MASS_LOWER_BOUND, MASS_UPPER_BOUND, EPS_SQUARED, G_SCALED

class Particles:
    """
    Handles the physics, state, and numerical integration for a system of N particles
    interacting via softened gravity in a 2D toroidal space.
    """

    def __init__(self, num_particles: int = 3, radius: float = 10) -> None:
        """
        Initializes the particle system with random masses, positions, and velocities.

        Args:
            num_particles (int): The number of bodies to simulate.
            radius (float): The display radius of the particles in pixels.
        """
        self.num_particles = num_particles
        self.unique_pair_indices: Tuple[np.ndarray, np.ndarray] = np.triu_indices(self.num_particles, k=1)
        self.num_pos_coords = NUM_DIM * self.num_particles
        self.radius = radius
        self.screen_dims = np.array((SCREEN_WIDTH, SCREEN_HEIGHT))

        # --- Generate random masses ---
        self.masses: np.ndarray = MASS_LOWER_BOUND + np.random.rand(self.num_particles) * (MASS_UPPER_BOUND - MASS_LOWER_BOUND)
        
        # --- Start at a random position within screen boundaries ---
        lower_bound = np.array([self.radius, self.radius])
        upper_bound = np.array([SCREEN_WIDTH - self.radius, SCREEN_HEIGHT - self.radius])
        self.pos: np.ndarray = lower_bound + np.random.rand(self.num_particles, NUM_DIM) * (upper_bound - lower_bound)

        # --- Start with random velocities (in pixels per second) ---
        lower_bound_vel = -150
        upper_bound_vel = 150
        self.vel: np.ndarray = lower_bound_vel + np.random.rand(self.num_particles, NUM_DIM) * (upper_bound_vel - lower_bound_vel)

        # Initialize force and energy containers
        self.forces: np.ndarray = np.zeros((self.num_particles, NUM_DIM))
        self.kinetic_energy: float = 0.0
        self.potential_energy: float = 0.0
        self.total_energy: float = 0.0

    def enforce_periodic_boundary_conditions(self) -> None:
        """
        Wraps particle positions around the screen edges to maintain a toroidal topology.
        """
        self.pos = np.mod(self.pos, self.screen_dims)

    def _calculate_forces_full_matrix(self) -> None:
        """
        DEPRECATED: Calculates forces using a full N x N matrix approach.
        Kept primarily for benchmarking or educational comparison against the
        optimized scatter-add approach in `calculate_forces`.
        """
        # entry (i,j) is the displacement vector from particle i to particle j, shape (num_particles, num_particles, 2)
        pairwise_disp = self.pos[np.newaxis, :, :] - self.pos[:, np.newaxis, :]

        # enforce minimum image convention (to work in concert with periodic boundary conditions)
        pairwise_disp -= self.screen_dims * np.round(pairwise_disp / self.screen_dims)

        # entry (i,j) is the squared distance between particles i and j, shape (num_particles, num_particles)
        # EPS must be summed to r_squared instead of pairwise_dist to avoid fictitous self-forces
        r_squared = np.sum(np.square(pairwise_disp), axis=2) + EPS_SQUARED
        
        # normalize array of displacements
        pairwise_disp /= np.sqrt(r_squared)[:, :, np.newaxis]

        # entry (i,j) is the product of the masses of particle i and particle j, shape (num_particles, num_particles)
        pairwise_mass_prod = self.masses[:, np.newaxis] * self.masses[np.newaxis, :]

        # entry (i,j) is the magnitude of the scaled gravitational force pointing from particle i to particle j
        force_magnitudes = G_SCALED * pairwise_mass_prod / r_squared

        # sum along the row to get the total force on particle i
        self.forces = np.sum(force_magnitudes[:, :, np.newaxis] * pairwise_disp, axis=1)

    def calculate_forces(self) -> None:
        """
        Calculates net gravitational forces on all particles.
        
        Uses a vectorized scatter-add approach to sum forces only between unique pairs,
        improving performance over the full matrix approach.
        """
        # reset forces to zero before accumulating
        self.forces = np.zeros((self.num_particles, NUM_DIM))

        # get indices for all unique pairs (i,j) where i < j
        i_indices, j_indices = self.unique_pair_indices

        # calculate displacement vector from particle i to particle j
        pairwise_disp = self.pos[j_indices] - self.pos[i_indices]

        # enforce minimum image convention (to work in concert with periodic boundary conditions)
        pairwise_disp -= self.screen_dims * np.round(pairwise_disp / self.screen_dims)
        
        # array of squared distances between any two particles forming a unique pair
        r_squared = np.sum(np.square(pairwise_disp), axis=1) + EPS_SQUARED

        # normalize array of displacements
        pairwise_disp /= np.sqrt(r_squared)[:, np.newaxis]

        # calculate mass products for unique pairs
        pairwise_mass_prod = self.masses[i_indices] * self.masses[j_indices]

        # array of force magnitudes between any two particles forming a unique pair
        force_magnitudes = G_SCALED * pairwise_mass_prod / r_squared

        # array of forces exerted by particle j on particle i in each pair (i,j)
        pair_forces = force_magnitudes[:, np.newaxis] * pairwise_disp

        # Aggregate forces (Newton's 3rd law: F_ij = -F_ji)
        np.add.at(self.forces, i_indices, pair_forces)
        np.add.at(self.forces, j_indices, -pair_forces)

    def calculate_accelerations(self) -> None:
        """
        Computes accelerations for all particles based on currently accumulated forces.
        """
        self.accelerations = self.forces / self.masses[:, np.newaxis]

    def step_forward(self, dt: float) -> None:
        """
        Advances the simulation by `dt` seconds using the RK45 integrator.

        Args:
            dt (float): The time step in seconds.
        """
        # flattened array of initial posiitons and velocities
        init_state = np.concatenate((self.pos.flatten(), self.vel.flatten()))

        # use robust Runge-Kutte 5(4) integrator
        sol = solve_ivp(
            fun=self.derivative,
            t_span=(0, dt),
            y0=init_state,
            t_eval=[dt],
            rtol=1e-6, # tighter relative tolerance
            atol=1e-9  # tighter absolute tolerance
        )

        # Extract final state from the solution
        final_state_flat = sol.y[:, 0]

        # slice and reshape to obtain final positions and velocities
        self.pos = final_state_flat[0 : self.num_pos_coords].reshape(self.num_particles, NUM_DIM)
        self.vel = final_state_flat[self.num_pos_coords :].reshape(self.num_particles, NUM_DIM) 

    def derivative(self, t: float, y_flat: np.ndarray) -> np.ndarray:
        """
        Calculates the state derivative (velocities and accelerations) for the N-body system.
        Required by `scipy.integrate.solve_ivp`.

        Args:
            t (float): Current simulation time (unused but required by signature).
            y_flat (np.ndarray): Flattened state vector [x1, y1, ... v1_x, v1_y, ...].

        Returns:
            np.ndarray: Flattened derivative vector [v1_x, v1_y, ... a1_x, a1_y, ...].
        """
        # --- Unpack the 1D state array y_flat ---
        current_pos = y_flat[0 : self.num_pos_coords].reshape(self.num_particles, NUM_DIM)
        current_vel = y_flat[self.num_pos_coords :].reshape(self.num_particles, NUM_DIM)

        # --- Calculate rates of change ---
        # We use current_pos from the integrator to calculate new forces/accelerations
        self.pos = current_pos
        self.calculate_forces()
        self.calculate_accelerations()

        return np.concatenate((current_vel.flatten(), self.accelerations.flatten()))

    def calculate_kinetic_energy(self) -> None:
        """Calculates the total kinetic energy of the system (KE = 0.5 * m * v^2)."""
        self.kinetic_energy = 0.5 * np.sum(self.masses * np.sum(np.square(self.vel), axis=1))

    def calculate_potential_energy(self) -> None:
        """
        Calculates the total gravitational potential energy of the system.
        Sums interactions only between unique pairs (i < j).
        """
        # get indices for all unique pairs (i,j) where i < j
        i_indices, j_indices = self.unique_pair_indices

        # calculate displacements for just these pairs
        pairwise_disp = self.pos[i_indices] - self.pos[j_indices]

        # enforce minimum image convention
        pairwise_disp -= self.screen_dims * np.round(pairwise_disp / self.screen_dims)

        # array of distances between any two particles forming a unique pair
        r = np.sqrt(np.sum(np.square(pairwise_disp), axis=1) + EPS_SQUARED)
        
        # calculate mass products for unique pairs
        pairwise_mass_prod = self.masses[i_indices] * self.masses[j_indices]
        
        # U = -G * m1 * m2 / r
        pair_potential = -G_SCALED * pairwise_mass_prod / r
        
        self.potential_energy = np.sum(pair_potential) 

    def calculate_total_energy(self) -> None:
        """
        Sums kinetic and potential energy to update self.total_energy.
        Should be called after a step_forward completes.
        """
        self.calculate_kinetic_energy()
        self.calculate_potential_energy()
        self.total_energy = self.potential_energy + self.kinetic_energy