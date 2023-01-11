from farkle.rules import get_score, get_score_and_remainder


class TestGetScore:
    def test_remainder(self):
        expectations = {
            (1, 2, 3, 4, 5, 2): 150,
            (1, 1, 5, 5, 6, 4): 300,
        }

        for roll, expected_score in expectations.items():
            assert get_score(roll) == expected_score

    def test_3_of_a_kind(self):
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

    def test_4_of_a_kind(self):
        expectations = {
            (1, 1, 1, 1, 2, 6): 1_000,
        }
        for roll, expected_score in expectations.items():
            assert get_score(roll) == expected_score

    def test_5_of_a_kind(self):
        expectations = {
            (1, 1, 1, 1, 1, 6): 2_000,
        }
        for roll, expected_score in expectations.items():
            assert get_score(roll) == expected_score

    def test_6_of_a_kind(self):
        expectations = {
            (1, 1, 1, 1, 1, 1): 3_000,
        }
        for roll, expected_score in expectations.items():
            assert get_score(roll) == expected_score

    def test_straight(self):
        expectations = {
            (1, 2, 3, 4, 5, 6): 1_500,
            (5, 2, 3, 4, 1, 6): 1_500,
            (6, 5, 4, 3, 2, 1): 1_500,
        }
        for roll, expected_score in expectations.items():
            assert get_score(roll) == expected_score

    def test_4_of_a_kind_with_pair(self):
        expectations = {
            (1, 1, 1, 1, 5, 5): 1_500,
            (5, 1, 1, 1, 5, 1): 1_500,
        }
        for roll, expected_score in expectations.items():
            assert get_score(roll) == expected_score

    def test_two_triplets(self):
        expectations = {
            (1, 1, 1, 2, 2, 2): 2_500,
            (6, 5, 6, 5, 6, 5): 2_500,
        }
        for roll, expected_score in expectations.items():
            assert get_score(roll) == expected_score


class TestGetScoreAndRemainder:
    def test_shortsighted(self):
        expectations = {
            (1, 2, 3, 4, 4, 6): (100, (2, 3, 4, 4, 6)),
            (1, 5, 3, 4, 4, 6): (150, (3, 4, 4, 6)),
            (1, 5, 3, 6, 4, 5): (200, (3, 4, 6)),
            (1, 1, 1, 3, 3): (300, (3, 3)),
            (1,): (100, ()),
            (5,): (50, ()),
            (1, 5): (150, ()),
            (1, 1, 1): (300, ()),
            (1, 1, 1, 4): (300, (4,)),
        }
        for roll, expected_result in expectations.items():
            assert get_score_and_remainder(roll) == expected_result

    def test_barbarian(self):
        expectations = {
            (1, 2, 3, 4, 4, 6): (100, (2, 3, 4, 4, 6)),
            (3, 2, 3, 4, 4, 6): (0, (2, 3, 3, 4, 4, 6)),
            (1, 5, 3, 4, 4, 6): (100, (3, 4, 4, 5, 6)),
            (1, 5, 3, 6, 4, 5): (100, (3, 4, 5, 5, 6)),
            (1, 1, 1, 3, 3): (300, (3, 3)),
            (1,): (100, ()),
            (5,): (50, ()),
            (1, 5): (100, (5,)),
            (1, 1, 1): (300, ()),
            (1, 1, 1, 4): (300, (4,)),
            (2,): (0, (2,)),
        }
        for roll, expected_result in expectations.items():
            assert get_score_and_remainder(roll) == expected_result
