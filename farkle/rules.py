import argparse

from typing import Sized
from itertools import combinations, product


_CLASSIC = {
    # Ones
    tuple(sorted([1])): 100,
    # Fives
    tuple(sorted([5])): 50,
    # Three ones (special case)
    tuple(sorted([1, 1, 1])): 300,
    # Three of a kind
    **{tuple(sorted([n] * 3)): n * 100 for n in range(2, 7)},
    # Four of a kind
    **{tuple(sorted([n] * 4)): 1_000 for n in range(1, 7)},
    # Five of a kind
    **{tuple(sorted([n] * 5)): 2_000 for n in range(1, 7)},
    # Six of a kind
    **{tuple(sorted([n] * 6)): 3_000 for n in range(1, 7)},
    # 1-6 Straight
    tuple(sorted(range(1, 7))): 1_500,
    # Three pairs
    **{tuple(sorted(x)): 1_500 for x in [[i] * 2 + [j] * 2 + [k] * 2 for i, j, k in combinations(range(1, 7), 3)]},
    # Four of any number with a pair
    **{tuple(sorted(x)): 1_500 for x in [[n] * 4 + [m] * 2 for n in range(1, 7) for m in range(1, 7) if n != m]},
    # Two triplets
    **{tuple(sorted(x)): 2_500 for x in [[i] * 3 + [j] * 3 for i, j in combinations(range(1, 7), 2)]},
}

# Sort by value, descending
CLASSIC = {key: value for key, value in sorted(_CLASSIC.items(), key=lambda x: x[1], reverse=True)}


def _get_score(roll: tuple[int]):
    for category, score in CLASSIC.items():
        if category == roll:
            return score

    return None


# Modified from: https://stackoverflow.com/a/39547832/1883424
def combinations_with_remainder(iterable: Sized, size: int):
    def mask(lst, p, v):
        return [lst[i] for i, e in enumerate(p) if e == v]

    if size < 0:
        raise ValueError(f"Illegal {size} value {size}")

    if size > len(iterable):
        raise ValueError(f"Requested size {size} is greater than length of given iterable ({len(iterable)})")

    return [
        (mask(iterable, p, 1), mask(iterable, p, 0)) for p in product([1, 0], repeat=len(iterable)) if sum(p) == size
    ]


def score_remainder(remainder: tuple[int, ...]):
    # individual 1s
    one_score = remainder.count(1) * CLASSIC[tuple([1])]
    # individual 5s
    five_score = remainder.count(5) * CLASSIC[tuple([5])]
    return one_score + five_score


def get_score(roll: tuple[int, ...]):
    roll = tuple(sorted(roll))
    # 6
    if result := _get_score(roll):
        return result

    # 5 and remainder
    for combination, remainder in combinations_with_remainder(roll, 5):
        result = _get_score(tuple(combination))
        if result is not None:
            return result + score_remainder(tuple(remainder))
    # 4 and remainder
    for combination, remainder in combinations_with_remainder(roll, 4):
        result = _get_score(tuple(combination))
        if result is not None:
            return result + score_remainder(tuple(remainder))
    # 3 and remainder
    for combination, remainder in combinations_with_remainder(roll, 3):
        result = _get_score(tuple(combination))
        if result is not None:
            return result + score_remainder(tuple(remainder))

    return score_remainder(tuple(roll))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("roll", type=int, nargs="+", help="The roll")
    return parser.parse_args()


def main():
    args = parse_args()
    score = get_score(args.roll)
    print(f"Score: {score}")


if __name__ == "__main__":
    main()
