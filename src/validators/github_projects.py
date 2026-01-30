from typing import List
from ..core.config import Config
from .base import BaseValidator


class GitHubProjectsValidator(BaseValidator):
    """Validator for github_projects.json."""

    @property
    def filename(self) -> str:
        return "github_projects.json"

    @property
    def name(self) -> str:
        return "GitHub Projects"

    def validate(self, data: dict) -> List[str]:
        errors = []
        required_fields = ["name", "url", "description"]

        for i, category in enumerate(data.get("categories", [])):
            for j, project in enumerate(category.get("projects", [])):
                for field in required_fields:
                    if field not in project:
                        errors.append(f"Category[{i}][{j}]: missing {field}")

                # Validate URL
                if "url" in project and not project["url"].startswith(("http://", "https://")):
                    errors.append(f"Project[{i}][{j}]: invalid URL format")

        return errors
