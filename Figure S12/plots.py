import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def main():
    sns.set_style("darkgrid")
    sns.set_theme("talk")

    df = pd.read_csv("actions.csv", index_col=0, header=0)

    df = df[["C", "social_norm", "epsilon1", "p"]]
    df = df.melt(
        id_vars=["social_norm", "epsilon1", "p"],
        var_name="Action",
        value_vars="C",
        value_name="Proportion",
    )

    g = sns.relplot(
        data=df, x="epsilon1", y="Proportion", kind="line", col="p", hue="social_norm"
    )
    g.set(
        xscale="log",
        xlabel="Frequency of Mutation $\epsilon_1$",
        ylabel="Frequency of Cooperation",
    )

    g._legend.set(title="Social Norm")

    for ax in g.axes[0]:
        ax.axvline(x=0.1, color="gray", alpha=0.5)

    plt.savefig("epsilon_1.jpeg", dpi=300)


if __name__ == "__main__":
    main()
