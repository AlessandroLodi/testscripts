class Figure:
    def __init__(
        self,
        aspect_ratio=1.0,
        rows=1,
        font=None,
        dpi=150,
        title="",
        labels=[],
        size=1.0,
        sharex=False,
        sharey=False,
        pad=0.2,
    ):
        self._subplots = []
        self._aspect_ratio = aspect_ratio
        self._rows = rows
        self._title = title
        self._dpi = dpi
        self._pad = pad
        self._font = font if font else {"font.size": 8}
        self._labels = labels
        self._size = size
        self._share = (sharex, sharey)
        Figure.cf = self

    def __bool__(self):
        return bool(len(self._subplots))

    def add_subplot(self, subplot, subplot_twin=None):
        if not subplot_twin:
            self._subplots.append(subplot)
        else:
            subplot["twin"] = subplot_twin
            self._subplots.append(subplot)

    def transpose(self):
        self._subplots = list(
            np.reshape(self._subplots, (self._rows, -1), order="F").flatten()
        )

    def _get_axis_metric_prefix(self, dec, lim, reverse=False):
        decades = [1e-15, 1e-12, 1e-9, 1e-6, 1e-3, 1, 1e3, 1e6, 1e9, 1e12]
        prefix = ["f", "p", "n", "\mu ", "m", "", "k", "M", "G", "T"]
        if reverse:
            decades = [1e15, 1e12, 1e-9, 1e6, 1e3, 1, 1e-3, 1e-6, 1e-9, 1e-12]
        scale = 1
        # print('before: dec: {}, lim: {}'.format(dec,lim))
        while lim > 100:
            lim /= 1e3
            scale *= 1e3
            dec *= 1e3
        while lim <= 0.1:
            lim *= 1e3
            scale /= 1e3
            dec /= 1e3
        if dec < 1e-15:
            dec = 1
            scale = 1
        if reverse:
            for i, d in enumerate(decades):
                if int(np.log10(dec)) > int(np.log10(d)):
                    # print('after: dec: {}, lim: {}, scale: {}, prefix: {}'.format(dec, lim, scale, prefix[i-1]))
                    return prefix[i - 1], scale
        else:
            for i, d in enumerate(decades):
                if int(np.log10(dec)) < int(np.log10(d)):
                    # print('after: dec: {}, lim: {}, scale: {}, prefix: {}'.format(dec, lim, scale, prefix[i-1]))
                    return prefix[i - 1], scale
        return "", 1

    def plot_subplot(self, subplot):
        # plt.rcParams["font.family"] = subplot['font']
        plt.sca(subplot["ax"])
        subplot["ax"].cla()
        if subplot["type"] == "image":
            for dataset in subplot.datasets:
                subplot["ax"].imshow(dataset)
                subplot["ax"].spines["top"].set_visible(False)
                subplot["ax"].spines["left"].set_visible(False)
                subplot["ax"].spines["bottom"].set_visible(False)
                subplot["ax"].spines["right"].set_visible(False)
                subplot["ax"].xaxis.set_visible(False)
                subplot["ax"].yaxis.set_visible(False)
                return
        if subplot["type"] == "2d":
            handles = []
            for i, dataset in enumerate(subplot.datasets):
                if dataset:
                    dataset.plot_2d(handles, index=i, **subplot.settings("cmap"))
            if subplot["legend"] == True:
                tdct = subplot.settings("legend_loc")
                if "legend_loc" in tdct:
                    tdct = {"loc": tdct["legend_loc"]}
                plt.legend(handles=handles, frameon=subplot["legend_border"], **tdct)
        if subplot["type"] == "scatter":
            handles = []
            for i, dataset in enumerate(subplot.datasets):
                if dataset:
                    dataset.plot_scatter(handles)
            subplot["lines"] = handles
            if subplot["legend"] == True:
                plt.legend(handles=handles, frameon=subplot["legend_border"])
        if subplot["type"] == "hist2d":
            for dataset in subplot.datasets:
                if dataset:
                    dataset.plot_hist2d(**subplot.settings("cmap", "bins"))
        if subplot["type"] == "hist":
            for i, dataset in enumerate(subplot.datasets):
                if dataset:
                    dataset.plot_hist(
                        index=i, **subplot.settings("bins", "color", "normed")
                    )
            if subplot["legend"] == True:
                plt.legend(frameon=subplot["legend_border"])
        if subplot["type"] == "color":
            for dataset in subplot.datasets:
                if subplot["cbar"] and subplot["cbar"] != "None":
                    subplot["cbar"].remove()
                if dataset:
                    dataset.plot_color(**subplot.settings("crange", "cmap", "calpha"))
                if subplot["cbar"] != "None":
                    # divider = make_axes_locatable(subplot['ax'])
                    # cax1 = divider.append_axes("right", size="10%", pad=0.05)
                    # subplot['cbar'] = plt.colorbar(format='%.2g', cax=cax1)
                    subplot["cbar"] = plt.colorbar(shrink=0.9)
                    subplot["cbar"].set_label(subplot["axis_labels"][2])
        if subplot["type"] == "3d":
            for dataset in subplot.datasets:
                if subplot["cbar"]:
                    subplot["cbar"].remove()
                if dataset:
                    p = dataset.plot_3d(**subplot.settings("zrange", "cmap"))
                subplot["cbar"] = plt.colorbar(p)
                subplot["cbar"].set_clim(*subplot["crange"])
                subplot["cbar"].set_label(subplot["axis_labels"][2])
                tick_locator = ticker.MaxNLocator(nbins=5)
                subplot["cbar"].locator = tick_locator
                subplot["cbar"].update_ticks()
        plt.gca().set_facecolor(subplot["background"])
        if subplot["invert_xaxis"]:
            plt.gca().invert_xaxis()
        if subplot["invert_yaxis"]:
            plt.gca().invert_yaxis()
        plt.xscale(subplot["axis_scales"][0])
        plt.yscale(subplot["axis_scales"][1])
        plt.xlabel(subplot["axis_labels"][0])
        plt.ylabel(subplot["axis_labels"][1])
        if subplot["xrange"]:
            xlim = plt.xlim()
            x0, x1 = subplot["xrange"]
            if x0 == -np.inf or x0 == np.inf:
                x0 = xlim[0]
            if x1 == -np.inf or x1 == np.inf:
                x1 = xlim[1]
            plt.xlim(x0, x1)
        if subplot["yrange"]:
            ylim = plt.ylim()
            y0, y1 = subplot["yrange"]
            if y0 == -np.inf or y0 == np.inf:
                y0 = ylim[0]
            if y1 == -np.inf or y1 == np.inf:
                y1 = ylim[1]
            plt.ylim(y0, y1)
        if subplot["yticks"]:
            plt.locator_params(axis="y", nticks=subplot["yticks"])
        if subplot["xticks"]:
            plt.locator_params(axis="x", nticks=subplot["xticks"])
        plt.gca().ticklabel_format(axis="x", useOffset=False)
        if subplot["hide_border"]:
            ax = plt.gca()
            if subplot["hide_xlabels"]:
                ax.spines["bottom"].set_visible(False)
            if subplot["hide_ylabels"]:
                ax.spines["left"].set_visible(False)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
        if subplot["hide_ylabels"]:
            plt.gca().yaxis.set_visible(False)
        if subplot["hide_xlabels"]:
            plt.gca().xaxis.set_visible(False)
        plt.title(subplot["title"], loc=subplot["title_align"])

        if subplot["twin"]:
            self.plot_subplot(subplot["twin"])
        plt.gcf().canvas.draw()

    def _change_ticks(self, subplot):
        # change labels
        if (
            "{metric_prefix}" in subplot["axis_labels"][1]
            or "{metric_prefix_reverse}" in subplot["axis_labels"][1]
        ):
            pf_y, scale_y = self._get_axis_metric_prefix(
                subplot.settings().get("scale_factor_y", 1),
                np.max(np.abs(subplot["ax"].get_ylim())),
                reverse="{metric_prefix_reverse}" in subplot["axis_labels"][1],
            )
            ticks = subplot["ax"].get_yticks() / scale_y
            subplot["ax"].set_yticklabels(["${0:g}$".format(s) for s in ticks])
            if subplot["ax"].get_ylabel():
                subplot["ax"].set_ylabel(
                    subplot["axis_labels"][1]
                    .replace("{metric_prefix}", pf_y)
                    .replace("{metric_prefix_reverse}", pf_y)
                )
        if (
            "{metric_prefix}" in subplot["axis_labels"][0]
            or "{metric_prefix_reverse}" in subplot["axis_labels"][0]
        ):
            pf_x, scale_x = self._get_axis_metric_prefix(
                subplot.settings().get("scale_factor_x", 1),
                np.max(np.abs(subplot["ax"].get_xlim())),
                reverse="{metric_prefix_reverse}" in subplot["axis_labels"][0],
            )
            ticks = subplot["ax"].get_xticks() / scale_x
            subplot["ax"].set_xticklabels(["${0:g}$".format(s) for s in ticks])
            if subplot["ax"].get_xlabel():
                subplot["ax"].set_xlabel(
                    subplot["axis_labels"][0]
                    .replace("{metric_prefix}", pf_x)
                    .replace("{metric_prefix_reverse}", pf_x)
                )
        if (
            len(subplot["axis_labels"]) > 2
            and (
                "{metric_prefix}" in subplot["axis_labels"][2]
                or "{metric_prefix_reverse}" in subplot["axis_labels"][2]
            )
            and subplot["cbar"] != "None"
        ):

            pf_z, scale_z = self._get_axis_metric_prefix(
                subplot.settings().get("scale_factor_z", 1),
                np.max(np.abs(subplot["cbar"].get_clim())),
                reverse="{metric_prefix_reverse}" in subplot["axis_labels"][2],
            )
            ticks = np.array(
                [
                    float(t.get_text().replace("−", "-").replace("$", ""))
                    for t in subplot["cbar"].ax.get_yticklabels()
                ]
            )
            try:
                ticks *= (
                    float(
                        subplot["cbar"]
                        .ax.yaxis.get_major_formatter()
                        .get_offset()
                        .replace("−", "-")
                    )
                    / scale_z
                )
            except:
                ticks /= scale_z
            ticklabels = np.array(["${0:g}$".format(s) for s in ticks], dtype=str)
            # set the in between values to 0 (we don't generally need to see em)
            ticklabels[1 : (len(ticklabels) // 2)] = " "
            ticklabels[(len(ticklabels) // 2 + 1) : -1] = " "
            subplot["cbar"].ax.set_yticklabels(ticklabels)
            subplot["cbar"].set_label(
                subplot["axis_labels"][2]
                .replace("{metric_prefix}", pf_z)
                .replace("{metric_prefix_reverse}", pf_z)
            )

    def _keydown(self, event):
        if event.key == "control":
            self._ctrl = True

    def _keyup(self, event):
        if event.key == "control":
            self._ctrl = False

    def _onpick(self, event):
        pc = event.artist
        cont = False
        for subplot in self._subplots:
            if pc in subplot["lines"]:
                cont = True
                break
        if not cont:
            return True
        N = len(event.ind)
        if not N:
            return True
        func = subplot["onpick"]
        # the click locations
        mx = event.mouseevent.xdata
        my = event.mouseevent.ydata

        # pc.set_offset_position('data')
        try:
            xy = pc.get_data()
        except:
            xy = pc.get_offsets()
        # xy = line.get_data()
        distances = np.hypot(mx - xy[event.ind][:, 0], my - xy[event.ind][:, 1])
        indmin = distances.argmin()
        dataind = event.ind[indmin]

        highlighter = subplot["highlighter"]
        if not highlighter:
            (subplot["highlighter"],) = subplot["ax"].plot(
                xy[dataind][0], xy[dataind][1], "o", ms=12, alpha=0.4, color="yellow"
            )
        else:
            if self._ctrl:
                d = subplot["highlighter"].get_data()
                subplot["highlighter"].set_data(
                    np.append(d[0], xy[dataind][0]), np.append(d[1], xy[dataind][1])
                )
            else:
                subplot["highlighter"].set_data(xy[dataind][0], xy[dataind][1])
        plt.gcf().canvas.draw()
        if func:
            func(subplot, dataind, self._ctrl)

    def _onclick(self, event):
        for spl in self._subplots:
            if spl["ax"] == event.inaxes:
                if spl["onclick"]:
                    spl["onclick"](spl, event)
                    plt.gcf().canvas.draw()

    def visualise(
        self,
        save_as="",
        block=True,
        position=None,
        name="Figure",
        change_func=None,
        tight=True,
        labels=[],
        show=True,
    ):
        Figure.cf = self
        if self._font:
            plt.rcParams.update(self._font)
        plt.close()

        fig = plt.figure(
            name,
            figsize=(
                3.3
                * self._aspect_ratio
                * self._size
                * int((len(self._subplots)) / self._rows),
                self._rows * 3.3 * self._size,
            ),
            dpi=self._dpi,
        )
        self._fig = fig
        # get the events
        fig.canvas.mpl_connect("pick_event", self._onpick)
        fig.canvas.mpl_connect("key_press_event", self._keydown)
        fig.canvas.mpl_connect("key_release_event", self._keyup)
        fig.canvas.mpl_connect("button_press_event", self._onclick)
        self._ctrl = False

        subplots = np.empty(
            (int((len(self._subplots)) / self._rows), self._rows),
            dtype=matplotlib.cm.ScalarMappable,
        )
        print(type(subplots))

        for index, subplot in enumerate(self._subplots):
            i, j = divmod(index, self._rows)

            if subplot["type"] == "3d":
                subplot["ax"] = fig.add_subplot(
                    self._rows,
                    int((len(self._subplots)) / self._rows),
                    index + 1,
                    projection="3d",
                )
                subplots[i, j] = subplot["ax"]
            else:
                subplot["ax"] = fig.add_subplot(
                    self._rows, int((len(self._subplots)) / self._rows), index + 1
                )
                subplots[i, j] = subplot["ax"]
                if subplot["twin"]:
                    subplot["twin"]["ax"] = subplot["ax"].twinx()

            self.plot_subplot(subplot)
            subplot["id"] = index
            if subplot["onload"]:
                subplot["onload"](subplot)

            if labels:
                self._labels = labels
            if self._labels:
                tot = len(self._subplots)
                maxx, b = divmod(tot, self._rows)
                a, b = divmod(index, maxx)
                x = b / maxx
                y = 1 - (a / self._rows)
                plt.gcf().text(
                    x,
                    y,
                    self._labels[index],
                    weight="bold",
                    fontsize=14,
                    horizontalalignment="left",
                    verticalalignment="top",
                )
            # subplot['ax'].ticklabel_format(style='sci',scilimits=subplot['scilimits'])
            subplot["ax"].ticklabel_format(style="plain", useOffset=False)

        if self._title:
            fig.suptitle(self._title)
        if tight:
            plt.tight_layout(pad=self._pad)

        if self._share[0]:
            fig.subplots_adjust(hspace=0)
        if self._share[1]:
            fig.subplots_adjust(wspace=0)
        for i in range(subplots.shape[0]):
            for j in range(subplots.shape[1]):
                # i is x direction
                # j is y direction
                if i < subplots.shape[0] - 1 and self._share[1]:
                    index = i + j * subplots.shape[0]
                    cbar = self._subplots[index]["cbar"]
                    if cbar:
                        cbar.remove()
                if i > 0 and self._share[1]:
                    index = i + j * subplots.shape[0]
                    subplot = self._subplots[index]["ax"]
                    subplot.tick_params(
                        axis="y", which="both", left=False, labelleft=False
                    )
                    subplot.set_ylabel("")

                if j < subplots.shape[1] - 1 and self._share[0]:
                    index = i + j * subplots.shape[0]
                    subplot = self._subplots[index]["ax"]
                    subplot.tick_params(
                        axis="x", which="both", bottom=False, labelbottom=False
                    )
                    subplot.set_xlabel("")
        # if self._share[0]:
        #     fig.subplots_adjust(hspace=0)
        # if self._share[1]:
        #     fig.subplots_adjust(wspace=0)
        for subplot in self._subplots:
            self._change_ticks(subplot)
            if subplot["twin"]:
                self._change_ticks(subplot["twin"])

        if change_func:
            change_func(self)
        if position:
            mngr = plt.get_current_fig_manager()
            # get the QTCore PyRect object
            # geom = mngr.window.geometry()
            # print(get_backend())
            # mngr.window.Move(0,0)
            mngr.window.wm_geometry("+%d+%d" % position)
            # thismanager.window.SetPosition(position)
        if show:
            if not save_as:
                plt.show(block=block)
            else:
                file_path = save_as
                directory = os.path.dirname(file_path)
                if not os.path.exists(directory):
                    try:
                        os.makedirs(directory)
                    except:
                        pass
                plt.savefig(file_path)
                plt.close()


if __name__ == "__main__":
    import os
    import matplotlib.axes
    import matplotlib.mlab as mlab
    import matplotlib.pylab as pl
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    import matplotlib.cm
    import numpy as np
    import pandas as pd
    import scipy.interpolate
    import scipy.io as sio
    from matplotlib.cm import get_cmap
    from matplotlib.colors import to_rgba
    from matplotlib.ticker import FormatStrFormatter, ScalarFormatter
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib as mpl

    f = Figure()
    os.chdir(r"G:\2021")
    f.visualise(f"porcamadonna/1.png")
