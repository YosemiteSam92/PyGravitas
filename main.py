import pygame as pg
import argparse
import sys

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, NUM_PARTICLES, RADIUS, LOG_INTERVAL
from particles import Particles
from simulation_logger import SimulationLogger

def main(profile_enabled):

    # --- Profiler setup ---
    profiler = None
    if profile_enabled:
        import cProfile
        print('--- PROFILING ENABLED ---')
        profiler = cProfile.Profile()
        profiler.enable()


    # --- Pygame setup ---
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pg.time.Clock()
    running = True

    # --- Simulation logger setup ---
    logger = SimulationLogger()

    # --- Timing variables for logging ---
    log_accumulator = 0.0
    simulation_time = 0.0

    # --- Create particle and screen variables ---
    particles = Particles(NUM_PARTICLES, RADIUS)

    # --- Game loop ---
    try:
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

            # update simulation time
            simulation_time += dt
            log_accumulator += dt

            # --- Update particle positions ---
            particles.step_forward(dt)

            # --- Check for boundary collisions ---
            particles.enforce_boundary()

            # --- Log data ---
            if log_accumulator > LOG_INTERVAL:

                # log system's energy
                particles.calculate_total_energy()
                logger.log(
                    simulation_time,
                    particles.kinetic_energy,
                    particles.potential_energy,
                    particles.total_energy
                )
                log_accumulator = 0.0

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

    except KeyboardInterrupt:
        # Allow quitting via Ctrl+C in the terminal
        print('\n--- Simulation stopped by user ---')
        running = False

    finally:
        if profiler:
            # disable profiler and dump statistics
            profiler.disable()
            stats_filename = 'particle_sim.prof'
            profiler.dump_stats(stats_filename)
            print(f'--- PROFILING COMPLETE. Stats saved to {stats_filename} ---')
            print(f'--- To analyze, run python profile_analyzer.py {stats_filename} ---')

        # --- Clean up ---
        # close the window and quit
        pg.quit()

if __name__ == '__main__':
    
    # --- Parse command line arguments ---
    # setup argument parser
    parser = argparse.ArgumentParser(
        description='Run a 2D n-body gravitational simulation.'
    )
    parser.add_argument(
        "--profile",
        action="store_true",  # make it a Boolean flag
        help="Run the simulation with cProfile enabled and save stats"
    )

    # parse the arguments
    args = parser.parse_args()

    # --- Call the main function with the flags ---
    main(profile_enabled=args.profile)
