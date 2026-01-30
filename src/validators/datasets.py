from typing import List
from ..core.config import Config
from .base import BaseValidator


class DatasetsValidator(BaseValidator):
    """Validator for datasets.json."""

    @property
    def filename(self) -> str:
        return "datasets.json"

    @property
    def name(self) -> str:
        return "Datasets"

    def validate(self, data: dict) -> List[str]:
        errors = []

        for i, dataset in enumerate(data.get("datasets", [])):
            if "name" not in dataset:
                errors.append(f"datasets[{i}]: missing name")
            if "url" not in dataset:
                errors.append(f"datasets[{i}]: missing url")
            if "description" not in dataset:
                errors.append(f"datasets[{i}]: missing description")

            # Validate URL
            if "url" in dataset:
                url = dataset["url"]
                if not url.startswith(("http://", "https://")):
                    errors.append(f"datasets[{i}]: invalid URL format")

        return errors
