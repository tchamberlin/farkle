import csv
import multiprocessing
from pathlib import Path
import argparse
import logging
import random
from typing import Union

from tqdm import tqdm

from .rules import get_score
from .utils import Benchmark

LOGGER = logging.getLogger(__name__)

DEFAULT_NUM_DICE = 6
DEFAULT_NUM_SIDES = 6
MAX_CHUNK_SIZE = 10_000


def roll_die(sides=6) -> int:
    return random.randint(1, sides)


def roll_dice(num_dice=DEFAULT_NUM_DICE) -> list[int]:
    return [roll_die() for _ in range(num_dice)]


def roll_and_score(num_dice=DEFAULT_NUM_DICE):
    dice = roll_dice(num_dice=num_dice)
    score = get_score(tuple(dice))
    return dice, score


def roll_and_score_helper(*args):
    """Wrapper around roll_and_score that throws away all its arguments"""
    return roll_and_score()


def farkle_multiprocess(
    num_rolls: int,
    num_sides_per_die=DEFAULT_NUM_SIDES,
    num_dice_per_roll=DEFAULT_NUM_DICE,
    chunk_size: Union[int, None] = None,
):
    if chunk_size is None:
        # Max chunk size is 10,000. If there are fewer than 10,000 rolls, do everything in a single chunk
        chunk_size = MAX_CHUNK_SIZE if MAX_CHUNK_SIZE < num_rolls else num_rolls

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.imap_unordered(roll_and_score_helper, (_ for _ in range(num_rolls)), chunksize=chunk_size)

        for result in tqdm(results, total=num_rolls, smoothing=0.0):
            yield result


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

    with Benchmark(f"Computed {args.num_rolls:,} trials"):
        with open("scores.csv", "a") as file:
            writer = csv.writer(file)
            for roll, score in farkle_multiprocess(num_rolls=args.num_rolls):
                writer.writerow([*roll, score])


if __name__ == "__main__":
    main()
