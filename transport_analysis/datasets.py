"""QTLab filename conventions and dataset discovery helpers."""

from __future__ import annotations

import re
from collections.abc import Iterable
from pathlib import Path


_FILENAME_BODY = (
    r".*?\d{6}_(?P<exp>[A-Za-z0-9_]+)_"
    r"(?P<type>[A-Za-z0-9_-]+?)_(?P<device>[A-Za-z]+[0-9]+)"
    r"\.(?:dat|csv|txt)$"
)
DEFAULT_FILENAME_PATTERN = _FILENAME_BODY


def build_filename_pattern(folders: Iterable[str] = ()) -> str:
    """Build the regular expression used to identify QTLab data files.

    Folder names are escaped so names containing ``+``, ``(``, or other
    regular-expression characters are matched literally.
    """

    names = tuple(folders)
    if not names:
        return DEFAULT_FILENAME_PATTERN
    if any(not name for name in names):
        raise ValueError("folder names must not be empty")

    folder_pattern = "|".join(re.escape(name) for name in names)
    return rf".*?(?P<folder>{folder_pattern})[\\/]{_FILENAME_BODY}"


def find_qtlab_dataset(directory: str | Path, folders: Iterable[str] = ()):
    """Find QTLab files using the repository's established dataset class.

    The import is intentionally local: filename utilities remain usable in
    lightweight environments that do not have the plotting stack installed.
    """

    from imports.qtlab_data import QTLab_Dataset

    path = Path(directory).expanduser()
    if not path.is_dir():
        raise NotADirectoryError(path)
    return QTLab_Dataset.find(str(path), pattern=build_filename_pattern(folders))
