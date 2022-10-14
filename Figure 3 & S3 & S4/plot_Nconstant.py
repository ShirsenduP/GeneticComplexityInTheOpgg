import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot():
    df = pd.read_csv("actions_Nconstant.csv", index_col=0, header=0)
    print(df.columns)
    df = df.melt(
        id_vars=["uid", "social_norm", "n", "p"],
        value_vars=["C", "D", "L"],
        value_name="Frequency",
        var_name="Action",
    )
    df = df[df["Action"] == "C"]

    sns.set_style("darkgrid")
    sns.set_context("talk")

    g = sns.catplot(
        data=df,
        x="n",
        y="Frequency",
        hue="p",
        col="social_norm",
        kind="bar",
        col_wrap=2,
    )
    g.set_titles("Anti-{col_name}")
    g.set_axis_labels("Group size n", "Frequency of Cooperation")
    g.fig.subplots_adjust(top=0.9)
    g.fig.suptitle("Fixed population size $N=100$")

    plt.savefig("n_v_p_Nconstant.jpeg", dpi=300)


if __name__ == "__main__":
    plot()
