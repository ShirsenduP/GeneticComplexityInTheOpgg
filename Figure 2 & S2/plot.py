import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def make_plot_evens():

    sns.set_style("darkgrid")
    sns.set_context("talk")

    df = pd.read_csv("average_actions.csv", header=0, index_col=0)
    df = df.reset_index().melt(
        ["norm", "p", "index"], var_name="Action", value_name="Proportion"
    )

    for plot_only_evens in [True, False]:
        tmp = df
        if plot_only_evens:
            tmp = df[df["p"] % 2 == 0]
            tmp = df.query("p == 1 or p % 2 == 0")

        g = sns.relplot(
            data=tmp,
            x="p",
            y="Proportion",
            hue="Action",
            kind="line",
            col="norm",
            col_wrap=2,
            height=4,
            aspect=1.5,
        )
        g.set_xlabels("$p$")
        g.set(xticks=[2, 4, 6, 8, 10, 12, 14])

        for ax in g.axes.flatten():
            d = ax.get_title().split()[-1]
            ax.set_title("Anti-" + d)
        if plot_only_evens:
            plt.savefig("p_evens.jpeg", dpi=300)
        else:
            plt.savefig("p_all.jpeg", dpi=300)


def make_single_plot():

    sns.set_style("darkgrid")
    sns.set_context("paper", font_scale=1.6)

    df = pd.read_csv("summary_data/average_actions.csv", header=0, index_col=0)
    df = df.reset_index().melt(
        ["norm", "p", "index"], var_name="Action", value_name="Proportion"
    )
    df = df[df["p"] % 2 == 0]
    df = df[df["norm"] == "Defector"]
    print(df)
    g = sns.lineplot(
        x="p",
        y="Proportion",
        hue="Action",
        data=df,
        err_style="band",
        ci="sd",
        legend="full",
    )
    g.set_xlabel("$p$")
    plt.subplots_adjust(bottom=0.15)
    # for ax in g.axes.flatten():
    #     d = ax.get_title().split()[-1]
    g.set_title("Anti-Defector")

    plt.savefig(
        r"C:\Users\spodd\project_genetic-opgar-experiments\C_p\figures\p_ad_only.eps"
    )
    plt.savefig(r"C:\Users\spodd\Dropbox\Gopgar\Latex\figs\C_p\p_ad_only.eps")


if __name__ == "__main__":
    make_plot_evens()
