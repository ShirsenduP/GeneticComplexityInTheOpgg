import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot():
    fig, ax = plt.subplots(1, 2, sharey=True, figsize=(6, 3))
    fig.subplots_adjust(bottom=0.23, right=0.875, wspace=0.1)

    sns.set_context("notebook")

    CONSTANT = "actions_Nconstant.csv"
    df_constant = pd.read_csv(CONSTANT, header=0, index_col=0)
    df_constant = df_constant[df_constant["social_norm"] == "Defector"]
    g1 = sns.barplot(data=df_constant, x="n", y="C", hue="p", ax=ax[0])
    g1.set(xlabel="Group size $n$", ylabel="Frequency of Cooperation")
    g1.set_title("$N=100$ constant, AD", fontdict={"fontsize": 9})
    g1.legend().remove()

    VARIABLE = "actions_Nvariable.csv"
    df_variable = pd.read_csv(VARIABLE, header=0, index_col=0)
    df_variable = df_variable[df_variable["social_norm"] == "Defector"]
    g2 = sns.barplot(data=df_variable, x="n", y="C", hue="p", ax=ax[1])
    g2.set(xlabel="Group size $n$", ylabel="")
    g2.set_title("$N=20n$ variable, AD", fontdict={"fontsize": 9})
    g2.legend(
        title="$p$",
        fontsize=8,
        title_fontsize=9,
        bbox_to_anchor=(1, 0.5),
        loc="center left",
        frameon=False,
    )

    plt.savefig("overall.png")


if __name__ == "__main__":
    plot()
