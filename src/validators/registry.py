from typing import Dict, Optional, List
from .base import BaseValidator, ValidationResult


class ValidatorRegistry:
    """Registry for managing all validators."""

    def __init__(self):
        self._validators: Dict[str, BaseValidator] = {}
        self._register_builtin_validators()

    def _register_builtin_validators(self):
        """Register all built-in validators."""
        from .github_projects import GitHubProjectsValidator
        from .latest_projects import LatestProjectsValidator
        from .conferences import ConferencesValidator
        from .journals import JournalsValidator
        from .datasets import DatasetsValidator
        from .media_channels import MediaChannelsValidator
        from .papers import PapersValidator

        validators = [
            GitHubProjectsValidator(),
            LatestProjectsValidator(),
            ConferencesValidator(),
            JournalsValidator(),
            DatasetsValidator(),
            MediaChannelsValidator(),
            PapersValidator(),
        ]

        for validator in validators:
            self.register(validator)

    def register(self, validator: BaseValidator):
        """Register a validator."""
        self._validators[validator.filename] = validator

    def get_validator(self, filename: str) -> Optional[BaseValidator]:
        """Get validator by filename."""
        return self._validators.get(filename)

    def get_all_validators(self) -> List[BaseValidator]:
        """Get all registered validators."""
        return list(self._validators.values())

    def validate_all(self, data_dir) -> Dict[str, ValidationResult]:
        """Validate all files and return results."""
        from ..core.io import load_json
        from ..core.config import Config

        results = {}
        for filename, validator in self._validators.items():
            filepath = Config.get_data_file(filename)
            data = load_json(filepath)
            if data is None:
                results[filename] = [f"Failed to load {filepath}"]
            else:
                results[filename] = validator.validate(data)

        return results
