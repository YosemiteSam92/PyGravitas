import pygame as pg
import numpy as np
from scipy.integrate import solve_ivp

from constants import NUM_DIM, SCREEN_WIDTH, SCREEN_HEIGHT, MASS_LOWER_BOUND, MASS_UPPER_BOUND, EPS, G_SCALED

class Particles:
    def __init__(self, num_particles=3, radius=10):

        self.num_particles = num_particles
        self.num_pos_coords = NUM_DIM * self.num_particles
        self.radius = radius  # all particles have the same radius
        self.screen_dims = np.array((SCREEN_WIDTH, SCREEN_HEIGHT))

        # --- Generate random masses ---

        self.masses = MASS_LOWER_BOUND + np.random.rand(self.num_particles) * (MASS_UPPER_BOUND - MASS_LOWER_BOUND)
        
        # --- Start at a random position within screen boundaries ---

        # coordinate system has its origin (0,0) in the top left corner
        # so, generate random (x,y) positions uniformly between self.radius and 
        # screen_width/height - radius, leaving a buffer of self.radius on each side
        lower_bound = np.array([self.radius, self.radius])
        upper_bound = np.array([SCREEN_WIDTH - self.radius, SCREEN_HEIGHT - self.radius])
        self.pos = lower_bound + np.random.rand(self.num_particles, NUM_DIM) * (upper_bound - lower_bound)

        # --- Start with random velocities (in pixels per second) ---
        
        lower_bound_vel = -150
        upper_bound_vel = 150
        self.vel = lower_bound_vel + np.random.rand(self.num_particles, NUM_DIM) * (upper_bound_vel - lower_bound_vel)

    def enforce_boundary(self):

        # save indices of particles whose positions will be clipped due to boundary collisions
        clipped_indices = np.where((self.pos < self.radius) | (self.pos > self.screen_dims - self.radius))
        # clip position to keep particles within screen boundaries
        self.pos = np.clip(self.pos, self.radius, self.screen_dims - self.radius)
        # reverse velocity if position was clipped
        self.vel[clipped_indices] *= -1

    def calculate_forces(self):

        # entry (i,j) is the displacement vector from particle i to particle j, shape (num_particles, num_particles, 2)
        pairwise_disp = self.pos[np.newaxis, :, :] - self.pos[:, np.newaxis, :]

        # entry (i,j) is the squared distance between particles i and j, shape (num_particles, num_particles)
        # since pairwise_disp is 0 along the main diagonal, sum small EPS to prevent division by zero when computing force magnitudes
        # EPS must be summed to r_squared instead of pairwise_dist to avoid fictitous self-forces that would drive the system
        # to high coordinates very quickly
        r_squared = np.sum(np.square(pairwise_disp), axis=2) + EPS
        
        # normalize array of displacements
        # entry (i,j) is the unit vector pointing from particle i to particle j, shape (num_particles, num_particles, 2)
        pairwise_disp /= np.sqrt(r_squared)[:, :, np.newaxis]

        # entry (i,j) is the product of the masses of particle i and particle j, shape (num_particles, num_particles)
        pairwise_mass_prod = self.masses[:, np.newaxis] * self.masses[np.newaxis, :]

        # entry (i,j) is the magnitude of the scaled gravitational force pointing from particle i to particle j, shape (num_particles, num_particles)
        force_magnitudes = G_SCALED * pairwise_mass_prod / r_squared

        # matrix of pairwise force vectors is force_magnitudes[:, :, np.newaxis] * pairwise_disp, of shape (num_particles, num_particles, 2)
        # its entry (i,j) is the force vector on particle i due to particle j (directed from i to j)
        # thus, sum along the row to get the total force on particle i
        # final shape is (num_particles, 2)
        self.forces = np.sum(force_magnitudes[:, :, np.newaxis] * pairwise_disp, axis=1)

    def calculate_accelerations(self):

        # self.accelerations has shape (num_particles, 2)
        self.accelerations = self.forces / self.masses[:, np.newaxis]

    def step_forward(self, dt):

        # flattened array of initial posiitons and velocities
        init_state = np.concatenate((self.pos.flatten(), self.vel.flatten()))

        # use robust Runge-Kutte 5(4) integrator
        sol = solve_ivp(
            fun=self.derivative,
            t_span=(0, dt),
            y0=init_state,
            t_eval=[dt]
        )

        # Let num_coords = num_position_coords + num_velocity_coords
        #                = NUM_DIM * num_particles + NUM_DIM * num_particles
        #                = 2 * NUM_DIM * num_particles

        # sol.y has shape (num_coords, len(t_eval)) = (2 * NUM_DIM * num_particles, 1)
        # it is a column array and we select its only column to get 
        # a flattened 1D array of shape (num_coords,) carrying information
        # in the exact same order as init_state
        final_state_flat = sol.y[:, 0]

        # slice and reshape to obtain final positions and velocities
        self.pos = final_state_flat[0 : self.num_pos_coords].reshape(self.num_particles, NUM_DIM)
        self.vel = final_state_flat[self.num_pos_coords :].reshape(self.num_particles, NUM_DIM) 

        
    def derivative(self, t, y_flat):
        """
        Calculates the position and velocity derivatives for the N-body system.
        This is the "fun" that solve_ivp requires.
        
        t: current time (required by solve_ivp, but unused by us)
        y_flat: 1D array of state [pos1_x, pos1_y, ..., vel1_x, vel1_y, ...] of shape (2 * NUM_DIM * num_particles,)

        """

        # --- Unpack the 1D state array y_flat ---
        # This is the state that solve_ivp is currently testing
        current_pos = y_flat[0 : self.num_pos_coords].reshape(self.num_particles, NUM_DIM)
        current_vel = y_flat[self.num_pos_coords :].reshape(self.num_particles, NUM_DIM)

        # --- Calculate rates of change ---
        # We already have velocities, so compute accelerations
        self.pos = current_pos  # no need to save current self.pos, as self.step_forward will overwrite it
        self.calculate_forces()
        self.calculate_accelerations()

        return np.concatenate((current_vel.flatten(), self.accelerations.flatten()))

            
        
        



            