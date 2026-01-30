from typing import List
from ..core.config import Config
from .base import BaseValidator


class ConferencesValidator(BaseValidator):
    """Validator for conferences.json."""

    @property
    def filename(self) -> str:
        return "conferences.json"

    @property
    def name(self) -> str:
        return "Conferences"

    def validate(self, data: dict) -> List[str]:
        errors = []

        for i, conf in enumerate(data.get("conferences", [])):
            if "name" not in conf:
                errors.append(f"Conference[{i}]: missing name")
            if "url" not in conf:
                errors.append(f"Conference[{i}]: missing url")

        return errors
