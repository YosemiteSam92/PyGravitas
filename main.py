import pygame as pg
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from particles import Particles

# --- units convention ---
# time unit is seconds
# distance unit is pixels

# --- Pygame setup ---

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()
running = True

# --- Create particle and screen variables ---

num_particles = 50
radius = 10
particles = Particles(num_particles,radius)

# --- Game loop ---

while running:

    # --- Poll for events ---

    # pg.QUIT event means the user clicked X to close the window
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # --- Retrieve time since last frame ---

    # clock.tick(fps) returns the number of milliseconds since the last frame
    # it pauses the game long enough to ensure the 
    # the loop does not run more than fps times per second
    # (hardware independent)
    dt = clock.tick(60)/1000 # delta time in seconds

    # --- Update particle's position ---

    particles.pos += particles.vel * dt

    # --- Collision logic ---

    # check for boundary collisions
    particles.enforce_boundary()

    # --- Render the game ---

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # draw the particle
    # this step connects the Particles class to PyGame
    for pos in particles.pos:
        pg.draw.circle(
            screen,
            "red",
            pos,
            particles.radius
        )

    # flip() the display to put your work on screen
    pg.display.flip()

# close the window and quit
pg.quit()