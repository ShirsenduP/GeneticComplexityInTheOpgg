import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

NUM_JOBS = 1920


def plot_constant():

    sns.set_style("darkgrid")
    sns.set_context("talk")

    df = pd.read_csv("tmp_constant.csv", index_col=0, header=0)
    df = df.query("p == 1 or p % 2 == 0")
    g = sns.catplot(
        data=df,
        x="n",
        y="C",
        hue="p",
        col="social_norm",
        kind="bar",
        col_wrap=2,
        # palette="viridis",
        height=3,
        aspect=2,
    )
    g.set_titles("{col_name}")
    g.set(
        xlabel="Group size $n$",
        ylabel="Freq. of\nCooperation",
        xticklabels=[
            "$n=2$" + "\n" + "$N=100$",
            "$n=3$" + "\n" + "$N=99$",
            "$n=4$" + "\n" + "$N=100$",
            "$n=5$" + "\n" + "$N=100$",
        ],
    )
    g.fig.suptitle("Population size fixed $N=100$", y=1)
    g.legend.set(title="$p$")
    plt.savefig("constant.jpeg")


def plot_variable():

    sns.set_style("darkgrid")
    sns.set_context("talk")

    df = pd.read_csv("tmp_variable.csv", index_col=0, header=0)
    df = df.query("p == 1 or p % 2 == 0")
    g = sns.catplot(
        data=df,
        x="n",
        y="C",
        hue="p",
        col="social_norm",
        kind="bar",
        col_wrap=2,
        # palette="viridis",
        height=3,
        aspect=2,
    )
    g.set_titles("{col_name}")
    g.set(
        xlabel="Group size $n$",
        ylabel="Freq. of\nCooperation",
        xticklabels=[
            "$n=2$" + "\n" + "$N=40$",
            "$n=3$" + "\n" + "$N=60$",
            "$n=4$" + "\n" + "$N=80$",
            "$n=5$" + "\n" + "$N=100$",
        ],
    )
    g.fig.suptitle("Population size variable $N=20n$", y=1)
    g.legend.set(title="$p$")
    plt.savefig("variable.jpeg")


if __name__ == "__main__":
    plot_constant()
    plot_variable()
