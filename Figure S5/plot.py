import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def main(df):
    sns.set_style("darkgrid")
    sns.set_theme("talk")

    g = sns.relplot(
        data=df,
        x="c",
        hue="social_norm",
        hue_order=["Defector", "Loner", "Neither", "Both"],
        y="Proportion",
        col="p",
        kind="line",
    )
    g._legend.set(title="Social Norm")

    for ax in g.axes[0]:
        ax.axvline(x=1, color="grey", alpha=0.5)

    plt.savefig("c.png")


def group():
    df_p2_a = pd.read_csv("actions_p2.csv", header=0, index_col=0)
    df_p2_b = pd.read_csv("actions_p2b.csv", header=0, index_col=0)
    df_p8_a = pd.read_csv("actions_p8.csv", header=0, index_col=0)
    df_p8_b = pd.read_csv("actions_p8b.csv", header=0, index_col=0)

    df = pd.concat([df_p2_a, df_p2_b, df_p8_a, df_p8_b])

    df = df.melt(
        id_vars=["p", "social_norm", "c"],
        var_name="Action",
        value_vars="C",
        value_name="Proportion",
    )

    df = df[df["c"] <= 2.5]
    final_df = []
    for key, tmpdf in df.groupby(["social_norm", "p", "c"]):
        final_df.append(tmpdf.sample(n=20))

    df = pd.concat(final_df)
    return df


if __name__ == "__main__":
    df = group()
    main(df)
