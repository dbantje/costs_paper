import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import colormaps as cm
from matplotlib.colors import to_rgba

import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches

from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

import string

import pandas as pd
import xarray as xr
import numpy as np

from common_definitions import *

import decimal

def round_down(value, decimals):
    with decimal.localcontext() as ctx:
        d = decimal.Decimal(value)
        ctx.rounding = decimal.ROUND_DOWN
        return round(d, decimals)
    
def get_df_ytick(df):
    value = df.sum(axis=1).max()
    decimals = -int(np.floor(np.log10(abs(value)))) + 1

    return round_down(value, decimals)

impact2color = {
    "acidification": cm["tab20"].colors[0],
    "climate change": cm["tab20"].colors[2],
    "ecotoxicity": cm["tab20"].colors[4],
    "eutrophication": cm["tab20"].colors[18],
    "fossil resources": cm["tab20"].colors[6],
    "human toxicity": cm["tab20"].colors[8],
    "ionizing radiation": cm["tab20"].colors[12],
    "land use": cm["tab20"].colors[16],
    "metal/mineral resources": cm["tab20"].colors[14],
    "ozone depletion": cm["tab20"].colors[3],
    "particulate matter formation": cm["tab20"].colors[10],
    "photochemical oxidant formation": cm["tab20"].colors[17],
    "water use": cm["tab20"].colors[1]
}

stage2color = {
    "monetization": cm["Dark2"].colors[2],
    "technosphere": cm["Dark2"].colors[1],
    "biosphere": cm["Dark2"].colors[0]
}

sector2color = {
    "electricity production": "C0",
    "district or industrial heat": "C1",
    "residential heating": "C3",
    "liquids": "C2",
    "hydrogen and gases": "C4"
}

study2color = {
    "NEEDS": '#e377c2',
    "Sovacool et al": '#7f7f7f'
}

extended_colors = impact2color.copy()
extended_colors.update({"total": "black"})

colors_splitCC = impact2color.copy()
del colors_splitCC["climate change"]
colors_splitCC.update({
    "climate change: biogenic": cm["tab20"].colors[5],
    "climate change: land use": cm["tab20"].colors[11],
    "climate change: fossil": "black"
})

if TAKE_OUT_FOSSIL_RESOURCES_MIDPOINT:
    del colors_splitCC["fossil resources"]

colors_noCC = colors_splitCC.copy()
del colors_noCC["climate change: biogenic"]
del colors_noCC["climate change: land use"]
del colors_noCC["climate change: fossil"]


colors_splitCC_nobio = colors_splitCC.copy()
del colors_splitCC_nobio["climate change: biogenic"]

colors_splitCC_total = colors_splitCC.copy()
colors_splitCC_total.update({"total": "black"})

sector2plotname = {
    "electricity production": "electricity production",
    "district or industrial heat": "district or industrial heat",
    "residential heating": "residential heating",
    "liquids": "liquid fuels",
    "hydrogen and gases": "hydrogen and gases"
}

perspective2plotname = {
    "damage costs": "damage costs",
    "prevention costs": "prevention costs",
    "taxation costs": "taxation costs",
    "budget constraint": "budget constraint",
    "low estimate": "low-end estimate",
    "mediatn": "median"
}

def plot_labels(ax, df, columns, **kwargs):
    plot_data = df.reset_index()
    labels = [string.ascii_lowercase[i] for i in range(len(df))]

    for i, row in plot_data.iterrows():
        position = [row[c] for c in columns]
        ax.text(*position, labels[i], **kwargs)
    

def separate_palette(color_palette, alpha=0.6, lighter_suffix=" (indirect)"):
    darker = {}
    lighter = {}
    for ic, c in color_palette.items():
        darker[ic] = to_rgba(c, alpha=1.0)
        lighter[ic+lighter_suffix] = to_rgba(c, alpha=alpha)

    return darker, lighter

def append_to_column_names(df, suffix):
    mapper = {c: c + suffix for c in df.columns}

    return df.rename(columns=mapper)


def add_missing_ics_legend(ax, ics, **kwargs):
    "Add a legend with missing impact categories."
    handles = []
    for ic in ics:
        color = impact2color[ic]
        handles.append(mpatches.Patch(color=color, label=ic))

    return ax.legend(handles=handles, title="missing values for:", **kwargs)

def get_impact_category_handles(palette=colors_splitCC):
    handles = []
    for ic in sorted(list(palette.keys())):
        color = palette[ic]
        handles.append(mpatches.Patch(color=color, label=ic))

    return handles

def add_size_comparisons(axs, color="gray", lw=0.8, ls="-"):
    ncols = axs.shape[1]

    for j in range(ncols):
        ylims= []
        for ax in axs[:,j]:
            bottom, top = ax.get_ylim()
            ylims.append(top)
        ylims = np.array(ylims)

        sort_idx = np.argsort(ylims)
        for i in range(len(sort_idx)-1):
            ax = axs[sort_idx[i+1], j]
            ax.axhline(y=ylims[sort_idx[i]], color=color, lw=lw, ls=ls)



def comparing_cost_perspectives_subplot(df, ax, plot_total=False, inset_techs=0, inset_ytop=None):
    sel = df[sorted(list(colors_splitCC.keys()))]
    sel[sorted(list(colors_splitCC.keys()))].plot.bar(stacked=True, ax=ax, color=colors_splitCC, legend=False)
    ax.axhline(y=0, color="gray", lw=0.8, zorder=0)

    if inset_techs > 0:
        inset_data = sel.iloc[-inset_techs:][sorted(list(colors_splitCC.keys()))]
        axins = inset_axes(
            ax,
            width="{}%".format(100*(inset_techs/len(sel.index))),
            height="40%",
            loc="upper right",
            borderpad=0
        )
        inset_data.plot.bar(stacked=True, ax=axins, color=colors_splitCC, legend=False)
        axins.set_xticks([])
        if inset_ytop:
            axins.set_yticks([0, inset_ytop], ["0", str(inset_ytop)])
        else:
            axins.locator_params(axis="y", nbins=2)
        axins.axhline(y=0, color="gray", lw=0.8, zorder=0)
        # axins.set_yticks([])
        axins.set_xlabel("")

        bottom, top = axins.get_ylim()
        ax.add_patch(plt.Rectangle((len(sel.index)-inset_techs-0.5, bottom), inset_techs, top-bottom,
                                   ls="-", lw=0.5, ec="k", fc="none"))

    if plot_total:
        y = sel.sum(axis=1)
        line = ax.plot(np.arange(len(y)), y, "d", color="C1",
                       label="total cost")
        return line
    
def comparing_cost_perspectives_subplot_noCC(df, ax, plot_total=False, inset_techs=0, inset_ytop=None):
    sel = df[sorted(list(colors_noCC.keys()))]
    sel[sorted(list(colors_noCC.keys()))].plot.bar(stacked=True, ax=ax, color=colors_noCC, legend=False)
    ax.axhline(y=0, color="gray", lw=0.8, zorder=0)

    if inset_techs > 0:
        inset_data = sel.iloc[-inset_techs:][sorted(list(colors_noCC.keys()))]
        axins = inset_axes(
            ax,
            width="{}%".format(100*(inset_techs/len(sel.index))),
            height="40%",
            loc="upper right",
            borderpad=0
        )
        inset_data.plot.bar(stacked=True, ax=axins, color=colors_noCC, legend=False)
        axins.set_xticks([])
        if inset_ytop:
            axins.set_yticks([0, inset_ytop], ["0", str(inset_ytop)])
        else:
            axins.locator_params(axis="y", nbins=2)
        axins.axhline(y=0, color="gray", lw=0.8, zorder=0)
        # axins.set_yticks([])
        axins.set_xlabel("")

        bottom, top = axins.get_ylim()
        ax.add_patch(plt.Rectangle((len(sel.index)-inset_techs-0.5, bottom), inset_techs, top-bottom,
                                   ls="-", lw=0.5, ec="k", fc="none"))

    if plot_total:
        y = sel.sum(axis=1)
        line = ax.plot(np.arange(len(y)), y, "d", color="C1",
                       label="total cost")
        return line

def cost_trends_subplot(df, ax, scenarios, annotate_scenarios=False, annotation_names=None,
                        plot_total=False, arrow_positions=[0.055, 0.035], arrow_size=0.02):
    bwidth = 0.3
    spacing = 0.1

    for pos, scen, i in zip([1+spacing, -spacing], scenarios, [0, 1]):
        plot_data = df.loc[scen][sorted(list(colors_splitCC.keys()))]
        plot_data.plot.bar(stacked=True, color=colors_splitCC, 
                                    position=pos, ax=ax, width=bwidth, legend=False)
        
        if plot_total:
            y = plot_data.sum(axis=1)
            dx = (spacing + bwidth)
            x = np.arange(len(y)) + dx * (-0.5 + i)
            ax.plot(x, y, "d", color="C1", label="total cost")
        
        ax.axhline(y=0, color="gray", lw=0.8, zorder=0)
        ax.set_xlabel("")
        ax.set_xlim([-0.5, 3.5])

    if annotate_scenarios:
        names = scenarios if annotation_names is None else annotation_names
        ax.annotate(names[0], xy=(1-(spacing+bwidth)/2, arrow_positions[0]), xytext=(1-(spacing+bwidth)/2, arrow_positions[0]+arrow_size),
                    arrowprops=dict(facecolor='black', shrink=0.05), rotation=90, ha="center", va="bottom"
                    )
        ax.annotate(names[1], xy=(1+(spacing+bwidth)/2, arrow_positions[1]), xytext=(1+(spacing+bwidth)/2, arrow_positions[0]+arrow_size),
                    arrowprops=dict(facecolor='black', shrink=0.05), rotation=90, ha="center", va="bottom"
                    )
        
def cost_trends_subplot_stages(df_direct, df_indirect, ax, scenarios, annotate_scenarios=False, 
                        plot_total=False, no_bio=False, spacing=0.1, bwidth=0.3, hatch=None):
    palette = colors_splitCC
    if no_bio:
        palette = colors_splitCC_nobio

    if hatch:
        colors_direct, colors_indirect = separate_palette(palette, alpha=1.0)
    else:
        colors_direct, colors_indirect = separate_palette(palette)

    df_combined = df_direct + df_indirect

    for pos, scen, i in zip([1+spacing, -spacing], scenarios, [0, 1]):
        plot_data1 = df_direct.loc[scen][sorted(list(palette.keys()))]
        plot_data2 = append_to_column_names(
            df_indirect.loc[scen][sorted(list(palette.keys()))],
            " (indirect)"
        )
        plot_data = pd.concat((plot_data1, plot_data2), axis=1)
        plot_data.plot.bar(stacked=True, color=colors_direct | colors_indirect, 
                                    position=pos, ax=ax, width=bwidth, legend=False)
        
        if plot_total:
            y = df_combined.loc[scen][sorted(list(palette.keys()))].sum(axis=1)
            dx = (spacing + bwidth)
            x = np.arange(len(y)) + dx * (-0.5 + i)
            ax.plot(x, y, "d", color="C1", label="total cost")
        
        ax.axhline(y=0, color="gray", lw=0.8, zorder=0)
        ax.set_xlabel("")
        ax.set_xlim([-0.5, 3.5])

    if hatch:
        chunksize = len(plot_data.index) * len(palette.keys())
        for i, bar in enumerate(ax.patches):
            if i//chunksize in [1, 3]:
                bar.set_hatch(hatch)
                bar.set_edgecolor("C1")
                bar.set_linewidth(0.4)
            # else:
            #     bar.set_hatch("\\")
            #     bar.set_edgecolor("C3")

    if annotate_scenarios:
        ax.annotate(scenarios[0], xy=(1-(spacing+bwidth)/2, 0.055), xytext=(1-(spacing+bwidth)/2, 0.055+0.02),
                    arrowprops=dict(facecolor='black', shrink=0.05), rotation=90, ha="center", va="bottom"
                    )
        ax.annotate(scenarios[1], xy=(1+(spacing+bwidth)/2, 0.035), xytext=(1+(spacing+bwidth)/2, 0.035+0.02),
                    arrowprops=dict(facecolor='black', shrink=0.05), rotation=90, ha="center", va="bottom"
                    )
        
def region_subplot(df, ax):
    sel = df[sorted(list(colors_splitCC.keys()))]
    sel[sorted(list(colors_splitCC.keys()))].plot.bar(stacked=True, ax=ax, color=colors_splitCC, legend=False)
    ax.axhline(y=0, color="gray", lw=0.8, zorder=0)