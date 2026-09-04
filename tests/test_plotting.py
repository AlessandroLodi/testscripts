import matplotlib

matplotlib.use("Agg")

from transport_analysis.plotting import plot_trace, save_figure


def test_plot_and_save_figure(tmp_path):
    figure, axes = plot_trace([0, 1], [1, 2], title="Trace")

    output_paths = save_figure(
        figure,
        tmp_path / "figures" / "trace",
        formats=("png",),
    )

    assert axes.get_title() == "Trace"
    assert output_paths == [tmp_path / "figures" / "trace.png"]
    assert output_paths[0].stat().st_size > 0
