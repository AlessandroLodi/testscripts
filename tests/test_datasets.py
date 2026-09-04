import re

from transport_analysis.datasets import build_filename_pattern, find_qtlab_dataset


def test_default_pattern_matches_qtlab_filename():
    match = re.match(
        build_filename_pattern(),
        "123456_Ale01_IVsVg_r31.dat",
    )

    assert match is not None
    assert match.groupdict() == {
        "exp": "Ale01",
        "type": "IVsVg",
        "device": "r31",
    }


def test_folder_pattern_escapes_regular_expression_characters():
    match = re.match(
        build_filename_pattern(["mol (1+2)"]),
        "/data/mol (1+2)/123456_Ale01_IVsVg_r31.dat",
    )

    assert match is not None
    assert match.group("folder") == "mol (1+2)"


def test_find_qtlab_dataset_discovers_nested_experiment(tmp_path):
    experiment = tmp_path / "mol (1+2)"
    experiment.mkdir()
    (experiment / "123456_Ale01_IVsVg_r31.dat").write_text(
        "0\t1\n",
        encoding="utf-8",
    )

    dataset = find_qtlab_dataset(tmp_path, folders=["mol (1+2)"])

    assert len(dataset) == 1
    assert dataset["type"] == "IVsVg"
    assert dataset["device"] == "r31"
