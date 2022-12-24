from pathlib import Path
import concurrent.futures
import argparse
import logging
import random

# import numpy as np
# import matplotlib.pyplot as plt
from tqdm import tqdm

import json

from .rules import get_score
from .utils import Benchmark

LOGGER = logging.getLogger(__name__)

DEFAULT_NUM_DICE = 6
DEFAULT_NUM_SIDES = 6


def roll_die(sides=6) -> int:
    return random.randint(1, sides)


def roll(num_dice=DEFAULT_NUM_DICE) -> list[int]:
    return [roll_die() for _ in range(num_dice)]


# This is the "new way" of doing this
# https://numpy.org/doc/stable/reference/random/index.html#random-quick-start
# rng = np.random.default_rng()


# def gen_rolls(num_rolls: int, num_sides=DEFAULT_NUM_SIDES, num_dice=DEFAULT_NUM_DICE) -> np.ndarray:
#     return rng.integers(1, num_sides, (num_rolls, num_dice))


def gen_rolls(num_rolls: int, num_sides=DEFAULT_NUM_SIDES, num_dice=DEFAULT_NUM_DICE) -> np.ndarray:
    return rng.integers(1, num_sides, (num_rolls, num_dice))


def farkle_parallel(num_rolls: int, num_sides=DEFAULT_NUM_SIDES, num_dice=DEFAULT_NUM_DICE, max_workers=None):
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        rolls = gen_rolls(num_rolls=num_rolls, num_sides=num_sides, num_dice=num_dice)
        future_to_roll = {executor.submit(get_score, tuple(roll)): tuple(roll) for roll in rolls}
        results = []
        with tqdm(total=len(rolls), unit="trial") as progress:
            for future in concurrent.futures.as_completed(future_to_roll):
                roll = future_to_roll[future]
                try:
                    score = future.result()
                except Exception:
                    import traceback

                    traceback.print_exc()
                else:
                    results.append(score)
                #     tqdm.write(f"{roll}: {score}")
                finally:
                    progress.update(1)

    return results


def farkle(num_rolls: int, num_sides=DEFAULT_NUM_SIDES, num_dice=DEFAULT_NUM_DICE):
    rolls = gen_rolls(num_rolls=num_rolls, num_sides=num_sides, num_dice=num_dice)
    scores = [get_score(tuple(roll)) for roll in tqdm(rolls, unit="trial")]
    plt.hist(scores, bins="auto")
    plt.title(f"Farkle Score Distribution over {num_rolls} trials")
    plt.show()


def plot(scores: list[int], num_rolls: int):
    plt.hist(scores, bins="auto")
    plt.title(f"Farkle Score Distribution over {num_rolls} trials")
    plt.show()


def init_logging(verbosity):
    """Initialize logging based on requested verbosity"""
    if verbosity > 2:
        loglevel = logging.DEBUG
    elif verbosity == 2:
        loglevel = logging.INFO
    else:
        loglevel = logging.WARNING
    root_logger = logging.getLogger()
    root_logger.setLevel(loglevel)
    LOGGER.setLevel(loglevel)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(loglevel)
    # See: https://docs.python.org/3/library/logging.html#logrecord-attributes
    formatter = logging.Formatter("[%(asctime)s - %(levelname)s] %(message)s")
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("num_rolls", type=int, help="The number of trials")
    parser.add_argument(
        "-i", "--input", type=Path, help="Path to cached results file. Will be loaded; no trials will be run"
    )
    parser.add_argument("-v", "--verbosity", type=int, choices=range(0, 4), default=2)

    return parser.parse_args()


def main():
    args = parse_args()
    init_logging(args.verbosity)

    if args.input:
        with Benchmark("Loaded trials"):
            with open(args.input, "rb") as file:
                scores = json.loads(file.read())
    else:
        with Benchmark(f"Computed {args.num_rolls:,} trials"):
            scores = farkle_parallel(num_rolls=args.num_rolls, max_workers=None)
    output_path = f"scores_{args.num_rolls}.json"
    if not args.input:
        with Benchmark(f"Wrote {args.num_rolls:,} trials to {output_path}"):
            with open(output_path, "wb") as file:
                file.write(json.dumps(scores).encode("utf-8"))
    # plot(scores, args.num_rolls)


if __name__ == "__main__":
    main()
