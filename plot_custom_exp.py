import argparse
import os

import matplotlib.pyplot as plt
import numpy as np


parser = argparse.ArgumentParser()

parser.add_argument("--dir", default="custom_exp", help="Directory name for loss histories generated by custom experiments", type=str)
parser.add_argument("--legends", default ="top rand qsgd tope", help="Legends for the plot you want to display", type=str)

args = parser.parse_args()

directory = args.dir
criteria = args.dir
legends = args.legends.split(" ")

colors = ["black", "blue", "red", "pink", "green", "yellow", "orange", "brown"]
if __name__ == "__main__":

    tree = os.walk(directory)
    next(tree)
    for k, (root, _, files) in enumerate(tree):
        iterations = len(files)
        # take the length information
        length = len(np.load(root + '/' + files[0]))
        losses = np.zeros((iterations, length))

        for i, file in enumerate(files):
            losses[i, :] = np.load(root + '/' + file)

        std_dev = np.std(losses, axis=0)
        mean_loss = np.mean(losses, axis=0)
        # lower and upper bound for %95 Confidence Interval
        lower, upper = mean_loss - 1.96 * std_dev / iterations ** 0.5, mean_loss + 1.96 * std_dev / iterations ** 0.5

        if root.find("Coll") != -1:
            loss_type = "Collision"
        else:
            loss_type = "Loss"

        plt.title(f"{loss_type} vs. time without error factor")
        plt.xlabel("Steps")
        plt.ylabel("Loss")
        plt.plot(np.arange(length), mean_loss, color=colors[k], lw=0.5)
        plt.fill_between(np.arange(length), lower, upper, color=colors[k], alpha=0.1)

    plt.legend(legends)
    plt.savefig(directory + "/Figure.png")
    plt.show()
