"""Logging utilities with backward-compatible print support."""

import logging
import sys
from typing import Optional


class Logger:
    """Logger with print compatibility."""

    def __init__(self, name: str = "awesome_stai"):
        self._logger = logging.getLogger(name)
        if not self._logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(logging.Formatter("%(message)s"))
            self._logger.addHandler(handler)
            self._logger.setLevel(logging.INFO)

    def info(self, msg: str):
        """Log info message."""
        self._logger.info(msg)

    def error(self, msg: str):
        """Log error message."""
        self._logger.error(msg)

    def warning(self, msg: str):
        """Log warning message."""
        self._logger.warning(msg)

    def print(self, msg: str):
        """Direct print for backward compatibility."""
        print(msg)
