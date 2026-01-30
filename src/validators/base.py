from abc import ABC, abstractmethod
from typing import List, Tuple, Union
from pathlib import Path

ValidationResult = Union[List[str], Tuple[List[str], List[str]]]


class BaseValidator(ABC):
    """Abstract base class for all validators."""

    @property
    @abstractmethod
    def filename(self) -> str:
        """Target JSON filename."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable validator name."""
        pass

    @abstractmethod
    def validate(self, data: dict) -> ValidationResult:
        """
        Validate data.

        Returns:
            - List[str]: List of error messages
            - Tuple[List[str], List[str]]: (errors, warnings)
        """
        pass

    def validate_file(self, filepath: Path) -> ValidationResult:
        """Load and validate from file."""
        from ..core.io import load_json

        data = load_json(filepath)
        if data is None:
            return [f"Failed to load {filepath}"]

        return self.validate(data)
