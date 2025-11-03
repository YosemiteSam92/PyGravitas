import pygame as pg
import random

class Particle:
    def __init__(self, screen_width, screen_height, radius):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.radius = radius

        # start at a random position within screen boundaries
        # coordinate system has its origin (0,0) in the top left corner
        # so, generate a random x position between self.radius and screen_width/height - radius
        # (this leaves a buffer of self.radius on each side)
        self.pos = pg.Vector2(
            random.uniform(self.radius, self.screen_width - self.radius),
            random.uniform(self.radius, self.screen_height - self.radius)
        )

        # start with a random velocity
        self.vel = pg.Vector2(
            random.uniform(-150, 150), # pixels per second
            random.uniform(-150, 150)
        )