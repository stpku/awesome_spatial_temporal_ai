"""Configuration management for the project."""

from pathlib import Path


class Config:
    """Centralized configuration management."""

    # Data directories
    DATA_DIR: Path = Path("awesomelist")
    SCHEMA_DIR: Path = Path("schemas")

    # Report directories
    REPORTS_DIR: Path = Path("docs") / "reports"
    BADGES_DIR: Path = REPORTS_DIR / "badges"

    # Timeout settings
    LINK_CHECK_TIMEOUT: int = 6
    MAX_WORKERS: int = 16

    # Soft-fail domains for link checking
    SOFT_FAIL_DOMAINS: set = {
        "ieeexplore.ieee.org",
        "mdpi.com",
        "elsevier.com",
        "springer.com",
    }

    @classmethod
    def get_data_file(cls, filename: str) -> Path:
        """Get data file path."""
        return cls.DATA_DIR / filename

    @classmethod
    def get_schema_file(cls, filename: str) -> Path:
        """Get schema file path."""
        return cls.SCHEMA_DIR / f"{filename.replace('.json', '.schema.json')}"

    @classmethod
    def ensure_report_dirs(cls):
        """Ensure report directories exist."""
        cls.BADGES_DIR.mkdir(parents=True, exist_ok=True)
        cls.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
