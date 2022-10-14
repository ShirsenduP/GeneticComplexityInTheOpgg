from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot():
    plt.clf()
    sns.set_style("darkgrid")
    sns.set_context("talk")

    df = pd.read_csv("actions.csv", index_col=0, header=0)
    df = df.melt(
        id_vars=["social_norm", "r", "p"],
        value_vars="C",
        var_name="Action",
        value_name="Frequency of Cooperation",
    )

    g = sns.relplot(
        data=df,
        x="r",
        y="Frequency of Cooperation",
        hue="social_norm",
        col="p",
        kind="line",
    )
    g.set(xlabel="$r$")
    g.set_titles("$p={col_name}$")
    g._legend.set_title("Social Norm")
    for ax in g.axes[0]:
        ax.axvline(x=3, color="gray", alpha=0.5)

    plt.savefig("r.jpeg", dpi=300)


def plot_delta():
    plt.clf()
    sns.set_style("darkgrid")
    sns.set_context("talk")

    df = pd.read_csv("actions.csv", index_col=0, header=0)
    df = df.melt(
        id_vars=["social_norm", "r", "p"],
        value_vars="C",
        var_name="Action",
        value_name="Frequency of Cooperation",
    )
    df.drop("Action", axis=1, inplace=True)

    df_p8 = df.query("p == 8").groupby(["social_norm", "r"]).mean()
    df_p2 = df.query("p == 2").groupby(["social_norm", "r"]).mean()
    delta = df_p8 - df_p2

    g = sns.lineplot(
        data=delta,
        x="r",
        y="Frequency of Cooperation",
        hue="social_norm",
        hue_order=["Defector", "Loner", "Neither", "Both"],
        legend=False,
    )
    g.set(xlabel="$r$", title="Excess cooperation\n$p=8$ over $p=2$")
    plt.gcf().subplots_adjust(left=0.2, bottom=0.2, top=0.87)
    plt.savefig("r_delta.jpeg", dpi=300)


if __name__ == "__main__":
    plot()
    plot_delta()
