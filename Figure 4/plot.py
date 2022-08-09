import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

P_VALS = [*range(2, 15, 2)]
NORMS = ["Defector", "Loner", "Neither", "Both"]
COLOR_MAP = {
    "Defector": "tab:blue",
    "Loner": "tab:orange",
    "Neither": "tab:green",
    "Both": "tab:red",
}


def get_gini_index(series):
    """
    Calculate the gini index.

    The definition is:

    G = 1/(2 * n * n * x_bar) * sum_{i=1}^{n} sum_{j=1}^{n} | x_i - x_j |

    where |.| is the modulus and x_bar = 1 / n * sum_{i=1}^{n} x_i
    """
    # Remove any zero values from the series
    series = list(series[series > 0])
    mean = sum(series) / len(series)
    numerator = 0
    n = len(series)
    for i in range(n):
        for j in range(n):
            numerator += abs(series[i] - series[j])

    denominator = 2 * n**2 * mean
    return numerator / denominator


def plot_gini_index():
    fig, ax = plt.subplots(1, 2, figsize=(8, 3))
    fig.subplots_adjust(bottom=0.2, right=0.85, wspace=0.35)

    gini_axis = ax[1]
    allele_axis = ax[0]

    ####################################################################################
    # LEFT Allele use
    df_allele = pd.read_csv(
        "avg_chromosome_use.csv",
        index_col=0,
        header=0,
    )
    df_allele = df_allele[df_allele["p"] < 15]
    g = sns.lineplot(
        data=df_allele, x="p", y="Value", hue="Norm", legend=False, ax=allele_axis
    )
    g.set_xticks(P_VALS)
    g.set_xticklabels(P_VALS)
    ylim = g.get_ylim()
    allele_axis.plot(ylim, ylim, "-.", label="y=x", lw=1.5, color="gray")
    allele_axis.set_ylabel("Average Allele Use")

    ####################################################################################
    # Calculate gini index

    df = pd.read_csv(
        "avg_chromosome_use_derrida.csv",
        index_col=0,
        header=0,
    )
    gini = []
    for i, series in df.iterrows():
        norm = series.iloc[0]
        p = series.iloc[1]
        gini.append((norm, p, get_gini_index(series.iloc[2 : 2 + p])))
    df = pd.DataFrame(gini, columns=["Norm", "p", "Gini"])
    df = df[df["p"] <= 14]

    ####################################################################################
    # RIGHT AXIS Gini Index
    g = sns.lineplot(
        data=df, x="p", y="Gini", hue="Norm", ax=gini_axis, legend=False, dashes=True
    )
    g.set(xticks=P_VALS, xticklabels=P_VALS)
    g.set()

    ####################################################################################
    # RIGHT AXIS Cooperation Levels
    df_C = pd.read_csv(
        "../Figure 2 & S2/average_actions.csv",
        index_col=0,
        header=0,
    )
    df_C.drop(["D", "L"], axis=1, inplace=True)
    df_C = df_C[df_C["p"] % 2 == 0]
    df_C = df_C.groupby(["norm", "p"]).mean()

    for norm, color in COLOR_MAP.items():
        series = df_C.loc[norm, :]
        g.plot(series.index, series, color=color, linestyle="dotted")

    ####################################################################################
    # GINI VS COOPERATION LEGEND
    legend_lines = [
        Line2D([0], [0], color="gray", lw=2, label="Gini Index", linestyle="solid"),
        Line2D(
            [0],
            [0],
            color="gray",
            lw=1.5,
            label="Freq. of \nCoop.",
            linestyle="dotted",
        ),
    ]
    l2 = gini_axis.legend(
        handles=legend_lines,
        title="",
        title_fontsize=8,
        frameon=False,
        fontsize=7,
        bbox_to_anchor=(1, 0.15),
        loc="center right",
    )

    ####################################################################################
    # SOCIAL NORM LEGEND
    legend_norms = [
        Patch([0], [0], color="tab:blue", label="Defector"),
        Patch([0], [0], color="tab:orange", label="Loner"),
        Patch([0], [0], color="tab:green", label="Neither"),
        Patch([0], [0], color="tab:red", label="Both"),
    ]
    g.legend(
        handles=legend_norms,
        fontsize=7,
        frameon=False,
        title="Norm",
        title_fontsize=8,
        bbox_to_anchor=(1, 0.5),
        loc="center left",
    )
    gini_axis.add_artist(l2)

    ####################################################################################
    # Save
    sns.set_style("darkgrid")
    sns.set_context("talk")

    plt.savefig("allele_and_gini.png")


if __name__ == "__main__":
    plot_gini_index()
