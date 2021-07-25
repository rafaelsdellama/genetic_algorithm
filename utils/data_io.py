import os
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt


def create_dir(path):
    """
        Create target Directory if don't exist
        Parameters
        ----------
        path : str
            Directory path
        Returns
        -------
    """
    if not os.path.exists(path):
        os.makedirs(path)


def save_statistic(out_dir, statistic):
    """
        Save statistic from GA
        Parameters
        ----------
        out_dir : str
            Directory path
        statistic: DataFrame
            List of dict
        Returns
        -------
    """
    create_dir(out_dir)

    statistic_dir = Path(out_dir, "results.csv").as_posix()
    plot_dir = Path(out_dir, "Generations.png").as_posix()

    df = pd.DataFrame(
        statistic, columns=["mean_fitness", "best_fitness", "best_indiv"]
    )
    df.to_csv(statistic_dir, index=False, header=True)

    plt.plot(list(df["mean_fitness"]), "r")
    plt.plot(list(df["best_fitness"]), "g")
    plt.xlabel("Generations")
    plt.ylabel("Fitness")
    plt.title("Generations GA")
    plt.legend(["Mean Fitness", "Best Fitness"])

    plt.savefig(plot_dir)
    plt.clf()  # Clear the current figure.
    plt.cla()  # Clear the current axes.
    plt.close()
