from typing import List, Tuple
from ..core.config import Config
from .base import BaseValidator


class PapersValidator(BaseValidator):
    """Validator for papers.json with data quality checks."""

    @property
    def filename(self) -> str:
        return "papers.json"

    @property
    def name(self) -> str:
        return "Papers"

    def validate(self, data: dict) -> Tuple[List[str], List[str]]:
        errors = []
        warnings = []

        for i, paper in enumerate(data.get("papers", [])):
            # Required fields check
            if "title" not in paper:
                errors.append(f"papers[{i}]: missing title")
            if "url" not in paper:
                errors.append(f"papers[{i}]: missing url")
            if "year" not in paper:
                errors.append(f"papers[{i}]: missing year")

            # Data quality checks
            if "authors" in paper:
                authors = paper["authors"]
                # Check for placeholder values
                if "unknown" in authors.lower() or "tbd" in authors.lower() or "todo" in authors.lower():
                    errors.append(f"papers[{i}]: invalid author placeholder")

            if "url" in paper:
                url = paper["url"]
                # Check for placeholder URLs
                if "11111111" in url or "example.com" in url or "placeholder" in url:
                    errors.append(f"papers[{i}]: invalid URL placeholder")

                # Validate URL format
                if not url.startswith(("http://", "https://")):
                    errors.append(f"papers[{i}]: invalid URL format")

            if "venue" in paper:
                venue = paper["venue"]
                if venue in ["TBD", "Unknown", "TBA"]:
                    errors.append(f"papers[{i}]: invalid venue placeholder")

        return errors, warnings
