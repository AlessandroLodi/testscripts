"""Explicit, path-safe operations for collections of research data files."""

from __future__ import annotations

import shutil
from collections import Counter
from collections.abc import Iterable
from pathlib import Path


class CopyCollisionError(FileExistsError):
    """Raised when flattening a directory would overwrite a copied file."""


def copy_files(
    source: str | Path,
    destination: str | Path,
    *,
    extensions: Iterable[str] | None = None,
) -> list[Path]:
    """Copy files recursively into one destination directory.

    Existing files and duplicate basenames are rejected rather than silently
    overwritten. ``extensions`` is case-insensitive and accepts values with or
    without a leading dot.
    """

    source_path = Path(source).expanduser()
    destination_path = Path(destination).expanduser()
    if not source_path.is_dir():
        raise NotADirectoryError(source_path)

    suffixes = None
    if extensions is not None:
        suffixes = {
            extension.lower()
            if extension.startswith(".")
            else f".{extension.lower()}"
            for extension in extensions
        }

    files = sorted(path for path in source_path.rglob("*") if path.is_file())
    if suffixes is not None:
        files = [path for path in files if path.suffix.lower() in suffixes]

    destination_path.mkdir(parents=True, exist_ok=True)
    targets = [destination_path / path.name for path in files]
    target_counts = Counter(target.name for target in targets)
    duplicate_names = {name for name, count in target_counts.items() if count > 1}
    collisions = duplicate_names | {target.name for target in targets if target.exists()}
    if collisions:
        names = ", ".join(sorted(collisions))
        raise CopyCollisionError(f"copy would overwrite: {names}")

    for source_file, target in zip(files, targets, strict=True):
        shutil.copy2(source_file, target)
    return targets


def rename_files(
    directory: str | Path,
    old: str,
    new: str,
    *,
    recursive: bool = False,
) -> list[tuple[Path, Path]]:
    """Replace text in matching filenames and return the performed renames."""

    path = Path(directory).expanduser()
    if not path.is_dir():
        raise NotADirectoryError(path)
    if not old:
        raise ValueError("old must not be empty")

    candidates = path.rglob("*") if recursive else path.iterdir()
    changes = [
        (candidate, candidate.with_name(candidate.name.replace(old, new)))
        for candidate in candidates
        if candidate.is_file() and old in candidate.name
    ]
    collisions = [target for _, target in changes if target.exists()]
    if collisions:
        names = ", ".join(str(target) for target in collisions)
        raise FileExistsError(f"rename would overwrite: {names}")

    for source_file, target in changes:
        source_file.rename(target)
    return changes
