from .rules import get_score_and_remainder, _get_score, combinations_with_remainder, CLASSIC, score_remainder
from .gen_rolls import roll_dice
from .types import Roll

DEFAULT_NUM_DICE = 6


def maximize_remainder() -> tuple[list[Roll], int]:
    """A Strategy that maximizes the number of dice rerolled (the remainder)

    Basically, it keeps as few dice as possible while getting a good score. So if there are three 1s and nothing else,
    it will keep the three 1s and reroll the other three

    If there are a 1 and a 5, then it will keep only the 5

    This is a very stupid strategy, but it's easy to implement, and actually sensible most of the time
    """
    rolls = []

    total_score = 0
    remainder = None
    while True:
        roll = tuple(roll_dice(len(remainder) if remainder is not None else DEFAULT_NUM_DICE))
        score, remainder = get_score_and_remainder(tuple(roll))
        rolls.append((roll, score))
        print(f"Scored {roll}: {score} (remainder {remainder})")
        if score == 0 or not remainder:
            print(f"Exiting; {score=}; {remainder=}")
            break

    return rolls, total_score


def _maximize_keep(roll: tuple[int, ...]) -> tuple[int, tuple[int]]:
    roll = tuple(sorted(roll))
    num_dice = len(roll)

    if num_dice > 6:
        raise NotImplementedError("Not supported yet, but maybe one day...")

    if num_dice == 6:
        if score := _get_score(roll):
            return score, tuple()

    if num_dice >= 5:
        for combination, remainder in combinations_with_remainder(roll, 5):
            if score := _get_score(tuple(combination)):
                remainder_score, remainder = score_remainder(tuple(remainder))
                return score + remainder_score, tuple(sorted(remainder))

    if num_dice >= 4:
        for combination, remainder in combinations_with_remainder(roll, 4):
            if score := _get_score(tuple(combination)):
                remainder_score, remainder = score_remainder(tuple(remainder))
                return score + remainder_score, tuple(sorted(remainder))

    if num_dice >= 3:
        for combination, remainder in combinations_with_remainder(roll, 3):
            if score := _get_score(tuple(combination)):
                remainder_score, remainder = score_remainder(tuple(remainder))
                return score + remainder_score, tuple(sorted(remainder))

    return score_remainder(roll)


def maximize_keep() -> tuple[list[Roll], int]:
    """Keep all dice that score points. This strategy will always lose"""
    rolls = []

    total_score = 0
    remainder = None
    while True:
        roll = tuple(roll_dice(len(remainder) if remainder else DEFAULT_NUM_DICE))
        score, remainder = _maximize_keep(tuple(roll))
        total_score += score
        rolls.append((roll, score))
        print(f"Scored {roll}: {score} (remainder {remainder})")
        if score == 0:
            print(f"Exiting; {score=}; {remainder=}")
            total_score = 0
            break

    return rolls, total_score


def maximize_keep_but_not_crazy(score_threshold: int, remainder_size_threshold: int) -> tuple[list[Roll], int]:
    """Keep all dice that score points. This strategy does try to quit eventually"""
    rolls = []

    total_score = 0
    remainder = None
    while True:
        roll = tuple(roll_dice(len(remainder) if remainder else DEFAULT_NUM_DICE))
        score, remainder = _maximize_keep(tuple(roll))
        total_score += score
        rolls.append((roll, score))
        print(f"Scored {roll}: {score} (remainder {remainder})")
        if score == 0:
            print(f"FARKLE")
            total_score = 0
            break

        if total_score >= score_threshold or 0 < len(remainder) <= remainder_size_threshold:
            break

    return rolls, total_score
