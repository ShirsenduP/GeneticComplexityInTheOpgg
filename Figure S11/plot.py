import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

RESULTS_FOR_P2 = "actions_p2.csv"
RESULTS_FOR_P8 = "actions_p8.csv"


def plot():
    df2 = pd.read_csv(RESULTS_FOR_P2, index_col=0, header=0)
    df8 = pd.read_csv(RESULTS_FOR_P8, index_col=0, header=0)
    df = pd.concat([df2, df8])
    df = df.drop(["D", "L"], axis=1)
    df = df.melt(
        id_vars=["social_norm", "beta", "p"],
        value_vars="C",
        var_name="action",
        value_name="proportion",
    )

    sns.set_style("darkgrid")
    sns.set_context("poster", font_scale=0.7)

    g = sns.relplot(
        data=df, x="beta", y="proportion", hue="social_norm", kind="line", col="p"
    )
    g.set_titles("$p={col_name}$")
    g.set_axis_labels(
        r"Reputation Assignment Error $\beta$", "Frequency of Cooperation"
    )
    g._legend.set_title("Social Norm")

    for ax in g.axes[0]:
        ax.axvline(x=0, color="gray", alpha=0.5)

    plt.savefig("beta.png")


if __name__ == "__main__":

    plot()
