import argparse
import os

import matplotlib.pyplot as plt
import numpy as np

def bool_converter(value):
    if value == "False" or value == "false" or value == "FALSE":
        return False
    elif value == "True" or value == "TRUE" or value == "true":
        return True
    else :
        print("Invalid Valu")
        return None


parser = argparse.ArgumentParser()

parser.add_argument("--dir", default="custom_exp", help="Directory name for loss histories generated by custom experiments", type=str)
parser.add_argument("--legends", default ="top rand qsgd tope", help="Legends for the plot you want to display", type=str)
parser.add_argument("--plot_collisions", default="False", type=str)

args = parser.parse_args()

directory = args.dir
criteria = args.dir
plot_collisions = bool_converter(args.plot_collisions)
legends = args.legends.split(" ")

colors = ["black", "blue", "red", "green", "orange", "brown", "pink", "yellow"]
if __name__ == "__main__":

    tree = os.walk(directory)
    next(tree)
    for k, (root, _, files) in enumerate(sorted(tree)):
        if plot_collisions:
            loss_type = "Collision"
            if root.find("Coll") == -1:
                continue
        else:
            loss_type = "Loss"
            if root.find("Coll") != -1:
                continue

        iterations = int(len(files)) # Collision + Loss plots
        print(k)
        # take the length information
        length = len(np.load(root + '/' + files[0]))
        losses = np.zeros((iterations, length))

        for i, file in enumerate(files):
            losses[i, :] = np.load(root + '/' + file)

        std_dev = np.std(losses, axis=0)
        mean_loss = np.mean(losses, axis=0)
        # lower and upper bound for %95 Confidence Interval
        lower, upper = mean_loss - 1.96 * std_dev / iterations ** 0.5, mean_loss + 1.96 * std_dev / iterations ** 0.5

        plt.title(f"{loss_type} vs. Steps ")
        plt.xlabel("Steps")
        plt.ylabel("Loss")
        color_idx = k//2 if k % 2 == 0 else (k-1)//2
        plt.plot(np.arange(length), mean_loss, color=colors[color_idx], lw=0.5)
        plt.fill_between(np.arange(length), lower, upper, color=colors[color_idx], alpha=0.2)

    plt.legend(legends)
    plt.savefig(directory + "/Figure.png")
    plt.show()
