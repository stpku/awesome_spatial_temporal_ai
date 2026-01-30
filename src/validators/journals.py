from typing import List
from ..core.config import Config
from .base import BaseValidator


class JournalsValidator(BaseValidator):
    """Validator for journals.json."""

    @property
    def filename(self) -> str:
        return "journals.json"

    @property
    def name(self) -> str:
        return "Journals"

    def validate(self, data: dict) -> List[str]:
        errors = []

        for section in ["international", "chinese"]:
            for i, journal in enumerate(data.get(section, [])):
                if "name" not in journal:
                    errors.append(f"{section}[{i}]: missing name")
                if "url" not in journal:
                    errors.append(f"{section}[{i}]: missing url")

        return errors
