from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot():

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
    g._legend.set_title("Social Norm")
    for ax in g.axes[0]:
        ax.axvline(x=3, color="gray", alpha=0.5)

    plt.savefig("r.png")


if __name__ == "__main__":
    plot()
