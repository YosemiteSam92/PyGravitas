import csv

from constants import ENERGY_LOG_FILENAME

class SimulationLogger:

    def __init__ (self):
        """
        Initializes the logger, opens the file for writing and writes the header.
        """
        self.file = None
        self.writer = None

        try:
            self.file = open(ENERGY_LOG_FILENAME, 'w', newline='')
            self.writer = csv.writer(self.file)
            self.writer.writerow(('time', 'kinetic_energy', 'potential_energy', 'total_energy'))

        except IOError as e:
            print(f'Unable to open log file {ENERGY_LOG_FILENAME} for writing: {e}')
            self.writer = None

    def log(self, time, kinetic_energy, potential_energy, total_energy):
        """
        Writes a single row of data to the log file.
        """
        if self.writer:
            self.writer.writerow((time, kinetic_energy, potential_energy, total_energy))

    def close(self):
        """
        Closes the log file.
        """
        if self.file:
            self.file.close()