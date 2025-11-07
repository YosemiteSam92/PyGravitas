import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# --- Configuration ---
LOG_FILE = '../logs/energy_log.csv'

def main():
    # 1. Check if log file exists
    if not os.path.exists(LOG_FILE):
        print(f"Error: Log file not found at '{LOG_FILE}'")
        print("Please run the simulation first to generate data.")
        sys.exit(1)

    print(f"Reading data from {LOG_FILE}...")
    try:
        df = pd.read_csv(LOG_FILE)
    except Exception as e:
        print(f"Failed to read CSV file: {e}")
        sys.exit(1)

    # 2. Setup Plot Style
    # generally 'seaborn-v0_8-darkgrid' or 'bmh' look nice out of the box.
    # trying to use a style if available, falling back if not.
    try:
        plt.style.use('seaborn-v0_8-darkgrid')
    except OSError:
        # Fallback for older matplotlib versions
        plt.style.use('ggplot')

    fig, ax = plt.subplots(figsize=(10, 6))

    # 3. Plot Data
    # We plot KE and PE first with slight transparency (alpha) so they don't dominate.
    ax.plot(
        df['time'], 
        df['kinetic_energy'], 
        label='Kinetic Energy', 
        color='#4cc9f0', # Vivid light blue
        alpha=0.8, 
        linewidth=2
    )
    ax.plot(
        df['time'], 
        df['potential_energy'], 
        label='Potential Energy', 
        color='#f72585', # Vivid pink/magenta
        alpha=0.8, 
        linewidth=2
    )

    # "Exalt" the Total Energy:
    # - Plotted last (appears on top)
    # - Thicker line (linewidth=4)
    # - distinct, bright color (Gold/Orange)
    # - slightly different style (solid, maybe with a subtle shadow effect if we wanted to get fancy, but simple bold is best)
    ax.plot(
        df['time'], 
        df['total_energy'], 
        label='Total Energy', 
        color='black',
        linewidth=4,
        linestyle='-'
    )

    # 4. Labeling and Polish
    ax.set_title("System Energy Over Time", fontsize=16, pad=20, fontweight='bold')
    ax.set_xlabel("Simulation Time (seconds)", fontsize=12)
    ax.set_ylabel("Energy (scaled units)", fontsize=12)
    
    # Add a grid that isn't too intrusive
    ax.grid(True, which='both', linestyle='--', alpha=0.6)
    
    # Nice legend
    ax.legend(fontsize=12, frameon=True, facecolor='white', framealpha=0.9, loc='best')

    # Ensure layout is tight so labels don't get cut off
    plt.tight_layout()

    # 5. Show (and optionally save)
    print("Displaying plot...")
    plt.show()
    
    # Uncomment the next line if you want to auto-save images
    # fig.savefig("logs/energy_plot.png", dpi=300)

if __name__ == '__main__':
    main()