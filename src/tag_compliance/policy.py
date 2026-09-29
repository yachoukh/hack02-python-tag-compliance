"""Policy loading helpers."""

from pathlib import Path

from tag_compliance.models import TagPolicy


def load_policy(path: str | Path) -> TagPolicy:
    """Load a YAML policy file into a TagPolicy."""
    raise NotImplementedError("Challenge 2: implement the YAML policy loader")
