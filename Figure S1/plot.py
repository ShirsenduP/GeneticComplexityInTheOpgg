"""
Create a plot for the following simulations from C_p

jobid p norm
==============
0001 1 Defector
0005 2 Defector
0013 4 Defector
0021 6 Defector
0029 8 Defector
0037 10 Defector
0045 12 Defector
0053 14 Defector

"""


import seaborn as sns
from gopgar import load_config, load_df
from matplotlib import pyplot as plt
from matplotlib.patches import Patch
from rich.progress import track

JOBS = [1, 5, 13, 21, 29, 37, 45, 53]
NUM_JOBS = len(JOBS)
DATA_DIR = "data"


def main():

    # GET DATA
    df = {}
    for job in JOBS:
        config = load_config(job_id=job, directory=DATA_DIR)
        p = int(config["p"])
        df[p] = load_df(
            job_id=job, category="actions", batches=True, directory=DATA_DIR
        )

    # PLOT DATA
    sns.set_context("paper")
    sns.set_style("darkgrid")
    fig, axes = plt.subplots(NUM_JOBS, 1, sharex="all", sharey="all", figsize=(8, 8))
    fig.subplots_adjust(top=0.93)

    for ax, (p, data) in track(zip(axes, df.items())):
        tmp = data.fillna(0)
        tmp = tmp.rolling(window=1000).mean()  # THIS IS SLOW!
        # tmp = tmp.iloc[::100, :]  # FOR QUICK DEBUGGING

        sns.lineplot(data=tmp, ax=ax, legend=False, dashes=False)
        ax.text(1.04, 0.5, f"${p=}$", transform=ax.transAxes)

    # OVERALL TITLE
    fig.suptitle(
        "Example simulations with Anti-Defector social norm"
        "\n(Simple Rolling Average of 1000 timesteps)"
    )

    # Y AXIS LABELS
    # Turn off axis lines and ticks of the big subplot
    ax0 = fig.add_subplot(111, frameon=False)
    ax0.spines["top"].set_color("none")
    ax0.spines["bottom"].set_color("none")
    ax0.spines["left"].set_color("none")
    ax0.spines["right"].set_color("none")
    ax0.tick_params(labelcolor="none", top=False, bottom=False, left=False, right=False)
    ax0.grid(False)
    ax0.set_ylabel("Proportion of Action")

    # OVERALL LEGEND
    lines = [
        Patch([0], [0], color="tab:blue"),
        Patch([0], [0], color="tab:orange"),
        Patch([0], [0], color="tab:green"),
    ]
    labels = ["C", "D", "L"]
    axes[-1].legend(
        lines, labels, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.7)
    )

    plt.savefig("example_simulations.jpeg", dpi=300)


if __name__ == "__main__":
    main()
