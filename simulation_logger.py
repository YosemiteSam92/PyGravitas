import csv
from typing import Optional, TextIO
from constants import ENERGY_LOG_FILENAME

class SimulationLogger:
    """
    Handles logging of simulation data (time and energy metrics) to a CSV file.
    """

    def __init__(self) -> None:
        """
        Initializes the logger, attempts to open the log file for writing,
        and writes the CSV header row.
        
        Sets self.writer to None if the file cannot be opened, ensuring
        subsequent log calls do not crash the simulation.
        """
        self.file: Optional[TextIO] = None
        self.writer: Optional[csv.writer] = None

        try:
            # newline='' is recommended for csv module to let it handle line endings
            self.file = open(ENERGY_LOG_FILENAME, 'w', newline='')
            self.writer = csv.writer(self.file)
            self.writer.writerow(('time', 'kinetic_energy', 'potential_energy', 'total_energy'))

        except IOError as e:
            print(f'Unable to open log file {ENERGY_LOG_FILENAME} for writing: {e}')
            # Ensure writer is None so log() calls can safely skip
            self.writer = None

    def log(self, time: float, kinetic_energy: float, potential_energy: float, total_energy: float) -> None:
        """
        Writes a single row of energy data to the log file if the writer is active.

        Args:
            time (float): Current simulation time in seconds.
            kinetic_energy (float): Total system kinetic energy.
            potential_energy (float): Total system potential energy.
            total_energy (float): Sum of kinetic and potential energy.
        """
        if self.writer:
            self.writer.writerow((time, kinetic_energy, potential_energy, total_energy))

    def close(self) -> None:
        """
        Safely closes the log file if it is open.
        """
        if self.file:
            self.file.close()
            self.file = None