import numpy as np

from imports.dataclass import generate_color_list
from imports.qtlab_data import QTLab_Data, QTLab_Dataset


def test_qtlab_text_loader_supports_current_pandas(tmp_path):
    path = tmp_path / "trace.dat"
    path.write_text("0\t1\n1\t3\n", encoding="utf-8")

    data = QTLab_Data.load_from_file(
        path,
        axes=("voltage", "current"),
        readheader=False,
    )

    np.testing.assert_allclose(data["voltage"].values, [0, 1])
    np.testing.assert_allclose(data["current"].values, [1, 3])


def test_empty_dataset_has_zero_length(tmp_path):
    assert len(QTLab_Dataset.find(tmp_path)) == 0


def test_generate_color_list_uses_requested_length():
    assert len(generate_color_list(cmap="viridis", length=4)) == 4
