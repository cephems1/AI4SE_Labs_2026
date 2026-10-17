# Run with: python -m unittest test_prism_metric.py
import unittest

from prism_metric import prism_score


class PrismScoreTest(unittest.TestCase):
    def test_identical_result_scores_one(self):
        gold = [[3, "portola park"], [7, "cafe"]]
        self.assertEqual(prism_score(gold, [(3, "portola park"), (7, "cafe")], 2)["prism"], 1.0)

    def test_column_order_does_not_matter(self):
        gold = [[3, "portola park"]]
        self.assertEqual(prism_score(gold, [("portola park", 3)], 2)["prism"], 1.0)

    def test_wrong_numeric_column_gets_half_column_credit(self):
        # Gold selects HOUSE_NUMBER, NAME; prediction selects ID, NAME.
        score = prism_score([[3, "portola park"]], [(1457, "portola park")], 2)
        self.assertEqual(score["row_f1"], 1.0)
        self.assertEqual(score["col_f1"], 0.5)
        self.assertEqual(score["prism"], 0.5)

    def test_both_empty_scores_one(self):
        self.assertEqual(prism_score([], [], 2)["prism"], 1.0)

    def test_one_side_empty_scores_zero(self):
        self.assertEqual(prism_score([], [(1, "x")], 2)["prism"], 0.0)
        self.assertEqual(prism_score([[1, "x"]], [], 2)["prism"], 0.0)

    def test_partial_overlap_gets_partial_credit(self):
        # Gold has two tied "best" rows, prediction used LIMIT 1.
        score = prism_score([[1, "a"], [2, "b"]], [(1, "a")], 2)
        self.assertAlmostEqual(score["row_f1"], 2 / 3)
        self.assertAlmostEqual(score["prism"], 2 / 3)

    def test_select_star_is_penalised_by_column_f1(self):
        gold = [[3, "portola park"]]
        score = prism_score(gold, [(3, "portola park", "x", "y", 4.0)], 5)
        self.assertEqual(score["row_f1"], 1.0)
        self.assertAlmostEqual(score["prism"], 4 / 7)

    def test_duplicates_are_ignored(self):
        gold = [[3, "a"], [3, "a"]]
        self.assertEqual(prism_score(gold, [(3, "a")], 2)["prism"], 1.0)


if __name__ == "__main__":
    unittest.main()
