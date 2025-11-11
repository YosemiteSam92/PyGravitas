import pygame as pg
import argparse
import sys
from typing import Optional

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, NUM_PARTICLES, RADIUS, LOG_INTERVAL
from particles import Particles
from simulation_logger import SimulationLogger

def main(profile_enabled: bool) -> None:
    """
    Main entry point for the PyGravitas simulation.

    Initializes Pygame, sets up the simulation environment (particles, logger),
    and runs the main game loop which handles events, updates physics,
    and renders the scene.

    Args:
        profile_enabled (bool): If True, runs the simulation under cProfile
                                and dumps stats to 'particle_sim.prof' on exit.
    """

    # --- Profiler setup ---
    profiler: Optional[object] = None  # Type hint as generic object or specific cProfile.Profile if imported top-level
    if profile_enabled:
        import cProfile
        print('--- PROFILING ENABLED ---')
        profiler = cProfile.Profile()
        profiler.enable()

    # --- Pygame setup ---
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pg.time.Clock()
    running: bool = True

    # --- Simulation logger setup ---
    logger = SimulationLogger()

    # --- Timing variables for logging ---
    log_accumulator: float = 0.0
    simulation_time: float = 0.0

    # --- Create particle and screen variables ---
    particles = Particles(NUM_PARTICLES, RADIUS)

    # --- Game loop ---
    try:
        while running:

            # --- Poll for events ---
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            # --- Retrieve time since last frame ---
            # dt is in seconds. 60 FPS target.
            dt: float = clock.tick(60) / 1000.0

            # update simulation time
            simulation_time += dt
            log_accumulator += dt

            # --- Update particle positions ---
            particles.step_forward(dt)

            # --- Check for boundary collisions ---
            particles.enforce_periodic_boundary_conditions()

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
            screen.fill("purple")

            # draw particles
            for pos in particles.pos:
                pg.draw.circle(
                    screen,
                    "red",
                    # Pygame requires integer coordinates for drawing, though it often handles floats gracefully.
                    # Casting to int tuple here is explicit and safe.
                    (int(pos[0]), int(pos[1])),
                    particles.radius
                )

            pg.display.flip()

    except KeyboardInterrupt:
        print('\n--- Simulation stopped by user ---')
        running = False

    finally:
        # --- Clean up resources ---
        if logger:
             logger.close()

        if profiler:
            profiler.disable()
            stats_filename = 'particle_sim.prof'
            profiler.dump_stats(stats_filename)
            print(f'--- PROFILING COMPLETE. Stats saved to {stats_filename} ---')
            print(f'--- To analyze, run python profile_analyzer.py {stats_filename} ---')

        pg.quit()

if __name__ == '__main__':
    
    # --- Parse command line arguments ---
    parser = argparse.ArgumentParser(
        description='Run a 2D n-body gravitational simulation.'
    )
    parser.add_argument(
        "--profile",
        action="store_true",
        help="Run the simulation with cProfile enabled and save stats"
    )

    args = parser.parse_args()

    main(profile_enabled=args.profile)