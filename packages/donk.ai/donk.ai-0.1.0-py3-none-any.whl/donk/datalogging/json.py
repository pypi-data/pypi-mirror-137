import json
from typing import List

from donk.datalogging.datalogging import DataLogger

TODO!!!!!
Converty types to python primites o the fly


class JSONDataLogger(DataLogger):
    """Log data as single JSON file."""

    def __init__(self, file) -> None:
        super().__init__()

        self.file = file
        self.data = {}

    def log(self, key: List[str], data):
        """Log one data.

        Args:
            key: Path-like, hierarchical name associated with the data
            data: Data to log, should be python primitives
        """
        # Find/create nested dict
        d = self.data
        for key_part in key[:-1]:
            if key_part not in d:
                d[key_part] = {}
            d = d[key_part]

        # Store data
        d[key[-1]] = data

    def flush(self):
        """Write data to the file."""
        with open(self.file, "w") as f:
            json.dump(self.data, f, separators=(',', ':'))
