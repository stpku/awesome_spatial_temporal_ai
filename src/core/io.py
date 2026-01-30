"""JSON I/O utilities."""

import json
from pathlib import Path
from typing import Optional

from .logger import Logger
from .config import Config

logger = Logger()


def load_json(filepath: Path) -> Optional[dict]:
    """Safely load JSON file with error handling.

    Args:
        filepath: Path to JSON file

    Returns:
        Parsed JSON data or None if failed
    """
    try:
        with open(filepath, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {filepath}: {e}")
        return None
    except UnicodeDecodeError as e:
        logger.error(f"Encoding error in {filepath}: {e}")
        return None


def save_json(filepath: Path, data: dict, indent: int = 2) -> bool:
    """Safely save JSON file with error handling.

    Args:
        filepath: Path to save JSON file
        data: Data to save
        indent: JSON indentation level

    Returns:
        True if successful, False otherwise
    """
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"Failed to save {filepath}: {e}")
        return False


def load_all_data_files() -> dict[str, Optional[dict]]:
    """Load all data files.

    Returns:
        Dictionary mapping filename to data (or None if failed)
    """
    files = [
        "github_projects.json",
        "latest_projects.json",
        "conferences.json",
        "journals.json",
        "datasets.json",
        "media_channels.json",
        "papers.json",
    ]

    return {f: load_json(Config.get_data_file(f)) for f in files}
