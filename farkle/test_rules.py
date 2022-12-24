from .rules import get_score


def test_remainder():
    expectations = {
        (1, 2, 3, 4, 5, 2): 150,
        (1, 1, 5, 5, 6, 4): 300,
    }

    for roll, expected_score in expectations.items():
        assert get_score(roll) == expected_score


def test_3_of_a_kind():
    expectations = {
        (1, 1, 1, 4, 2, 6): 300,
        (2, 2, 2, 4, 3, 6): 200,
        (2, 2, 2, 4, 3, 5): 250,
        (3, 3, 3, 4, 2, 5): 350,
        (4, 4, 4, 6, 2, 5): 450,
        (5, 5, 5, 4, 3, 2): 500,
        (6, 6, 6, 4, 3, 2): 600,
    }
    for roll, expected_score in expectations.items():
        assert get_score(roll) == expected_score


def test_4_of_a_kind():
    expectations = {
        (1, 1, 1, 1, 2, 6): 1_000,
    }
    for roll, expected_score in expectations.items():
        assert get_score(roll) == expected_score


def test_5_of_a_kind():
    expectations = {
        (1, 1, 1, 1, 1, 6): 2_000,
    }
    for roll, expected_score in expectations.items():
        assert get_score(roll) == expected_score


def test_6_of_a_kind():
    expectations = {
        (1, 1, 1, 1, 1, 1): 3_000,
    }
    for roll, expected_score in expectations.items():
        assert get_score(roll) == expected_score


def test_straight():
    expectations = {
        (1, 2, 3, 4, 5, 6): 1_500,
        (5, 2, 3, 4, 1, 6): 1_500,
        (6, 5, 4, 3, 2, 1): 1_500,
    }
    for roll, expected_score in expectations.items():
        assert get_score(roll) == expected_score


def test_4_of_a_kind_with_pair():
    expectations = {
        (1, 1, 1, 1, 5, 5): 1_500,
        (5, 1, 1, 1, 5, 1): 1_500,
    }
    for roll, expected_score in expectations.items():
        assert get_score(roll) == expected_score


def test_two_triplets():
    expectations = {
        (1, 1, 1, 2, 2, 2): 2_500,
        (6, 5, 6, 5, 6, 5): 2_500,
    }
    for roll, expected_score in expectations.items():
        assert get_score(roll) == expected_score
