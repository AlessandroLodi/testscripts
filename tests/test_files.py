from pathlib import Path

import pytest

from transport_analysis import CopyCollisionError, copy_files, rename_files


def test_copy_files_filters_extensions_and_preserves_metadata(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "nested").mkdir()
    (source / "trace.dat").write_text("data")
    (source / "nested" / "notes.txt").write_text("notes")
    destination = tmp_path / "destination"

    copied = copy_files(source, destination, extensions=["dat"])

    assert copied == [destination / "trace.dat"]
    assert copied[0].read_text() == "data"


def test_copy_files_rejects_flattening_collisions(tmp_path):
    source = tmp_path / "source"
    (source / "a").mkdir(parents=True)
    (source / "b").mkdir()
    (source / "a" / "trace.dat").write_text("one")
    (source / "b" / "trace.dat").write_text("two")

    with pytest.raises(CopyCollisionError, match="trace.dat"):
        copy_files(source, tmp_path / "destination")


def test_rename_files_does_not_change_process_directory(tmp_path):
    original_directory = Path.cwd()
    (tmp_path / "old_trace.dat").write_text("data")

    changes = rename_files(tmp_path, "old", "new")

    assert Path.cwd() == original_directory
    assert changes == [(tmp_path / "old_trace.dat", tmp_path / "new_trace.dat")]
    assert (tmp_path / "new_trace.dat").is_file()
