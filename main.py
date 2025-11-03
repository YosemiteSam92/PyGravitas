import pygame as pg
from particle import Particle

# --- units convention ---
# time unit is seconds
# distance unit is pixels

# --- Pygame setup ---
pg.init()
screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()
running = True

# --- Create particle and screen variables ---

SCREEN_WIDTH = screen.get_width()
SCREEN_HEIGHT = screen.get_height()
radius = 10
particle = Particle(SCREEN_WIDTH, SCREEN_HEIGHT, radius)

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

    particle.pos += particle.vel * dt

    # --- Collision logic ---

    # check horizontal boundaries
    if particle.pos.x - particle.radius < 0:
        particle.pos.x = particle.radius # snap to edge
        particle.vel.x *= -1 # reverse x-velocity
    elif particle.pos.x + particle.radius > SCREEN_WIDTH:
        particle.pos.x = SCREEN_WIDTH - particle.radius # snap to edge
        particle.vel.x *= -1 # reverse x-velocity

    # check vertical boundaries
    if particle.pos.y - particle.radius < 0:
        particle.pos.y = particle.radius # snap to edge
        particle.vel.y *= -1 # reverse y-velocity
    elif particle.pos.y + particle.radius > SCREEN_HEIGHT:
        particle.pos.y = SCREEN_HEIGHT - particle.radius # snap to edge
        particle.vel.y *= -1 # reverse y-velocity

    # --- Render the game ---

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # draw the particle
    # this step connects the Particle class to PyGame
    pg.draw.circle(
        screen,
        "red",
        particle.pos,
        particle.radius
    )

    # flip() the display to put your work on screen
    pg.display.flip()

# close the window and quit
pg.quit()