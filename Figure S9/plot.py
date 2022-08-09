import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def main():
    df_p2 = pd.read_csv("actions_p2.csv", header=0, index_col=0)
    df_p8 = pd.read_csv("actions_p8.csv", header=0, index_col=0)

    df = pd.concat([df_p2, df_p8])

    df = df[["C", "social_norm", "omega", "p"]]
    df = df.melt(
        id_vars=["social_norm", "omega", "p"],
        var_name="Action",
        value_vars="C",
        value_name="Proportion",
    )

    sns.set_style("darkgrid")
    sns.set_theme("talk")

    g = sns.relplot(
        data=df, x="omega", hue="social_norm", y="Proportion", col="p", kind="line"
    )
    g._legend.set(title="Social Norm")
    g.set(xlabel="$\Omega$", ylabel="Frequency of Cooperation")

    for ax in g.axes[0]:
        ax.axvline(x=10 / 11, color="gray", alpha=0.5)

    plt.savefig("omega.png")


if __name__ == "__main__":
    main()
