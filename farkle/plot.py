import csv
from pathlib import Path
import argparse
import logging

import matplotlib.pyplot as plt
from tqdm import tqdm

LOGGER = logging.getLogger(__name__)


def plot(results: list[tuple[tuple[int, int, int, int, int, int], int]]):
    scores = [r[-1] for r in tqdm(results)]
    plt.hist(scores, bins=[0, 49, 150, 1000, 2000, 2500, 3000])
    plt.title(f"Farkle Score Distribution over {len(scores)} trials")
    plt.show()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", type=Path, nargs="?", default="scores.csv")
    parser.add_argument("-v", "--verbosity", type=int, choices=range(0, 4), default=2)

    return parser.parse_args()


def main():
    args = parse_args()
    with open(args.input_path) as file:
        reader = csv.reader(file)
        results = [(tuple([int(n) for n in row[:6]]), int(row[-1])) for row in tqdm(reader)]

    plot(results)


if __name__ == "__main__":
    main()
