import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot():
    df = pd.read_csv("actions.csv", header=0, index_col=0)
    df = df.melt(
        id_vars=["social_norm", "sigma", "p"],
        var_name="Action",
        value_vars="C",
        value_name="Proportion",
    )
    df = df[df["Action"] == "C"]

    sns.set_style("darkgrid")
    sns.set_theme("talk")

    g = sns.relplot(
        data=df, x="sigma", hue="social_norm", y="Proportion", col="p", kind="line"
    )
    g.set(xlabel="Loner's Payoff $\sigma$", ylabel="Frequency of Cooperation")
    g._legend.set_title("Social Norm")

    for ax in g.axes[0]:
        ax.axvline(x=1, color="gray", alpha=0.5)

    plt.savefig("sigma.jpeg", dpi=300)


if __name__ == "__main__":
    plot()
