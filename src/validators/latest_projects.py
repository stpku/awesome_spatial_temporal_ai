from typing import List
from ..core.config import Config
from .base import BaseValidator


class LatestProjectsValidator(BaseValidator):
    """Validator for latest_projects.json."""

    @property
    def filename(self) -> str:
        return "latest_projects.json"

    @property
    def name(self) -> str:
        return "Latest Projects"

    def validate(self, data: dict) -> List[str]:
        errors = []

        for section in ["spatial_intelligence", "world_models"]:
            for i, project in enumerate(data.get(section, [])):
                if "name" not in project:
                    errors.append(f"{section}[{i}]: missing name")
                if "url" not in project:
                    errors.append(f"{section}[{i}]: missing url")
                if "description" not in project:
                    errors.append(f"{section}[{i}]: missing description")

        return errors
