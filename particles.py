import pygame as pg
import numpy as np
from constants import NUM_DIM, SCREEN_DIMS, SCREEN_WIDTH, SCREEN_HEIGHT

class Particles:
    def __init__(self, num_particles=3, radius=10):
        self.num_particles = num_particles
        self.radius = radius  # all particles have the same radius
        
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
        for dim in range(NUM_DIM):

            # save indices of particles whose positions will be clipped due to boundary collisions
            clipped_indices = np.where((self.pos[:, dim] < self.radius) | (self.pos[:, dim] > SCREEN_DIMS[dim] - self.radius))
            # clip position to keep particles within screen boundaries
            self.pos[:, dim] = np.clip(self.pos[:, dim], self.radius, SCREEN_DIMS[dim] - self.radius)
            # reverse velocity if position was clipped
            self.vel[clipped_indices, dim] *= -1



            