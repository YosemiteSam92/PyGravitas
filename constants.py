# Unit convention
# time unit is seconds
# mass unit is kilograms
# distance unit is pixels

# PyGame environment constants
NUM_DIM = 2
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Physics constants
MASS_LOWER_BOUND = 1
MASS_UPPER_BOUND = 10

G_SCALED = 1000000  # Scaled gravitational constant
EPS = 0.0001  # Small value to avoid division by zero

# System constants
NUM_PARTICLES = 5
RADIUS = 10

# Logging constants
ENERGY_LOG_FILENAME = "logs/energy_log.csv" 
LOG_FREQUENCY_HZ = 10  # How many times per second to log data
LOG_INTERVAL = 1.0 / LOG_FREQUENCY_HZ 