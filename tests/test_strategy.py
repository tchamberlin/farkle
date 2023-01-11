from farkle.strategy import maximize_keep_but_not_crazy, maximize_remainder, maximize_keep


def gen_dice_roller(rolls):
    """Generate a roll_dice() function that rolls the given set of rolls"""
    index = 0

    def roll_dice(*args):
        nonlocal index
        try:
            roll = rolls[index]
        except IndexError as error:
            raise ValueError("Ran out of rolls! You need to provide more rolls") from error
        index += 1
        return roll

    return roll_dice


def test_maximize_remainder(mocker):
    expected_rolls = [
        (4, 4, 1, 3, 5, 2),  # keep the 1, reroll the rest
        (1, 1, 1, 3, 4),  # keep the 3 1s, reroll the rest
        (1, 5),  # keep the 1, reroll the rest
        (3, 4, 4, 6, 6, 2),  # Farkle. Lose everything; turn ends. Score: 0
    ]
    expected_roll_scores = [100, 300, 100, 0]
    expected_total_score = 0
    mocker.patch("farkle.strategy.roll_dice", gen_dice_roller(expected_rolls))

    rolls, score = maximize_remainder()
    assert expected_total_score == score
    for expected_roll, expected_score, [actual_roll, actual_score] in zip(
        expected_rolls, expected_roll_scores, rolls, strict=True
    ):
        assert expected_score == actual_score
        assert expected_roll == actual_roll


def test_maximize_keep(mocker):
    expected_rolls = [
        (4, 4, 1, 3, 5, 2),  # keep the 1 and the 5, reroll the rest
        (1, 1, 1, 3, 4),  # keep the 3 1s, reroll the rest
        (1, 5),  # keep both. Hot dice; reroll everything
        (1, 1, 1, 1, 1, 1),  # 6 of a kind! Hot dice...
        (2, 2, 3, 3, 4, 6),  # Farkle
    ]
    expected_roll_scores = [150, 300, 150, 3000, 0]
    expected_total_score = 0
    mocker.patch("farkle.strategy.roll_dice", gen_dice_roller(expected_rolls))

    rolls, score = maximize_keep()
    assert expected_total_score == score
    for expected_roll, expected_score, [actual_roll, actual_score] in zip(
        expected_rolls, expected_roll_scores, rolls, strict=True
    ):
        assert expected_score == actual_score
        assert expected_roll == actual_roll


class TestMaximizer:
    def test_a(self, mocker):
        expected_rolls = [
            (4, 4, 1, 3, 5, 2),  # keep the 1 and the 5, reroll the rest
            (1, 1, 1, 3, 4),  # keep the 3 1s and stop
        ]
        expected_roll_scores = [150, 300]
        expected_total_score = sum(expected_roll_scores)
        mocker.patch("farkle.strategy.roll_dice", gen_dice_roller(expected_rolls))

        rolls, score = maximize_keep_but_not_crazy(score_threshold=300, remainder_size_threshold=3)
        assert expected_total_score == score
        for expected_roll, expected_score, [actual_roll, actual_score] in zip(
            expected_rolls, expected_roll_scores, rolls, strict=True
        ):
            assert expected_score == actual_score
            assert expected_roll == actual_roll

    def test_c(self, mocker):
        expected_rolls = [
            (4, 4, 1, 3, 5, 2),  # keep the 1 and the 5, reroll the rest
            (1, 1, 1, 3, 4),  # keep the 3 1s and stop
            (1, 5),  # keep both. Hot dice; reroll everything
            (1, 1, 1, 1, 1, 1),  # 6 of a kind! Hot dice...
            (1, 1, 1, 1, 1, 1),  # 6 of a kind! Hot dice...
            (1, 1, 1, 1, 1, 1),  # 6 of a kind! Hot dice...
            (1, 1, 1, 1, 1, 1),  # 6 of a kind! Hot dice...
            (1, 1, 1, 1, 1, 1),  # 6 of a kind! Hot dice...
            (1, 1, 1, 1, 1, 1),  # 6 of a kind! Hot dice...
            (4, 6, 3, 3, 2, 2),  # Farkle
        ]
        expected_roll_scores = [150, 300, 150, 3000, 3000, 3000, 3000, 3000, 3000, 0]
        expected_total_score = 0
        mocker.patch("farkle.strategy.roll_dice", gen_dice_roller(expected_rolls))

        rolls, score = maximize_keep_but_not_crazy(score_threshold=100_000, remainder_size_threshold=0)
        assert expected_total_score == score
        for expected_roll, expected_score, [actual_roll, actual_score] in zip(
            expected_rolls, expected_roll_scores, rolls, strict=True
        ):
            assert expected_score == actual_score
            assert expected_roll == actual_roll
