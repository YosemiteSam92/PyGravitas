import sys
from pathlib import Path
from typing import Optional

try:
    import pandas as pd
    import matplotlib.pyplot as plt
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure
except ImportError as e:
    print(f"Dependency missing: {e}")
    print("Please ensure pandas and matplotlib are installed: pip install pandas matplotlib")
    sys.exit(1)

# --- Configuration ---
# Use pathlib to reliably locate the logs folder relative to this script
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = BASE_DIR / 'logs' / 'energy_log.csv'
PLOT_OUTPUT = BASE_DIR / 'logs' / 'energy_plot.png'

def setup_plot_style() -> None:
    """
    Attempts to set a clean plotting style, falling back gracefully if
    specific styles are not available in the user's matplotlib version.
    """
    try:
        plt.style.use('seaborn-v0_8-darkgrid')
    except OSError:
        # Fallback for older matplotlib versions or if style is missing
        try:
            plt.style.use('ggplot')
        except OSError:
            pass # rely on default style if all else fails

def main() -> None:
    """
    Reads simulation energy data from CSV and generates a time-series plot.
    Displays the plot to the user and optionally saves it to the logs directory.
    """
    # 1. Check if log file exists
    if not LOG_FILE.exists():
        print(f"Error: Log file not found at '{LOG_FILE}'")
        print("Please run the main simulation first to generate data.")
        sys.exit(1)

    print(f"Reading data from {LOG_FILE}...")
    try:
        df = pd.read_csv(LOG_FILE)
    except Exception as e:
        print(f"Failed to read CSV file: {e}")
        sys.exit(1)

    # 2. Setup Plot
    setup_plot_style()
    fig: Figure
    ax: Axes
    fig, ax = plt.subplots(figsize=(10, 6))

    # 3. Plot Data
    # Plot KE and PE with transparency to highlight Total Energy
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

    # Plot Total Energy prominently on top
    ax.plot(
        df['time'], 
        df['total_energy'], 
        label='Total Energy', 
        color='black',
        linewidth=3,
        linestyle='-'
    )

    # 4. Labeling and Polish
    ax.set_title("System Energy Over Time", fontsize=16, pad=20, fontweight='bold')
    ax.set_xlabel("Simulation Time (seconds)", fontsize=12)
    ax.set_ylabel("Energy (scaled units)", fontsize=12)
    
    ax.grid(True, which='both', linestyle='--', alpha=0.6)
    ax.legend(fontsize=12, frameon=True, facecolor='white', framealpha=0.9, loc='best')

    plt.tight_layout()

    # 5. Show and Save
    print("Displaying plot...")
    # Optional: Save the plot automatically before showing
    # fig.savefig(PLOT_OUTPUT, dpi=300)
    # print(f"Plot saved to {PLOT_OUTPUT}")
    
    plt.show()

if __name__ == '__main__':
    main()