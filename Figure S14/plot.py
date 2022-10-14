import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def main():
    """Output figure."""
    df = pd.read_csv(
        "actions.csv",
        index_col=0,
        header=0,
    )

    df = df[["social_norm", "epsilon2", "p", "C"]]
    df = df.melt(
        id_vars=["social_norm", "epsilon2", "p"],
        value_vars="C",
        var_name="Action",
        value_name="Proportion",
    )
    print(df)

    sns.set_style("darkgrid")
    sns.set_theme("talk")

    g = sns.relplot(
        data=df,
        x="epsilon2",
        y="Proportion",
        hue="social_norm",
        kind="line",
        col="p",
    )

    g.set(xlabel="$\epsilon_2$", ylabel="Frequency of Action", xscale="log")
    g._legend.set(title="Social Norm")

    for ax in g.axes[0]:
        ax.axvline(x=1, color="gray", alpha=0.5)

    plt.savefig("epsilon_2.jpeg", dpi=300)


if __name__ == "__main__":
    main()
