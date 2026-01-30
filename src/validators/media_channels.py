from typing import List
from ..core.config import Config
from .base import BaseValidator


class MediaChannelsValidator(BaseValidator):
    """Validator for media_channels.json."""

    @property
    def filename(self) -> str:
        return "media_channels.json"

    @property
    def name(self) -> str:
        return "Media Channels"

    def validate(self, data: dict) -> List[str]:
        errors = []

        # Validate wechat publications
        for i, pub in enumerate(data.get("wechat_publications", [])):
            if "name" not in pub:
                errors.append(f"wechat_publications[{i}]: missing name")

        # Validate newsletters
        for i, news in enumerate(data.get("newsletters", [])):
            if "name" not in news:
                errors.append(f"newsletters[{i}]: missing name")
            if "url" not in news:
                errors.append(f"newsletters[{i}]: missing url")

        return errors
