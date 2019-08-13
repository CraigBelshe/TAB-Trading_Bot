from TAB_linear_inter.interpolation import best_fit_line
from unittest import main
from unittest import TestCase


class TestBestFit(TestCase):
    def test_best_fit_line(self):
        x = [0, 1, 2]
        y = [0, 5, 10]
        x1 = [1, 3, 4, 5, 7, 10, 11]
        y1 = [100, 120, 130, 125, 130, 150, 145]
        x2 = [1, 2]
        y2 = [10, 20]
        x3 = [-5, 0, 10]
        y3 = [-10, 0, 20]

        self.assertTupleEqual(best_fit_line(x, y), ([0, 1.5, 3], [0, 7.5, 15]))
        self.assertTupleEqual(best_fit_line(x1, y1), ([1.0, 6.5, 12.0], [108.23321554770318, 131.26325088339223, 154.29328621908127]))
        self.assertTupleEqual(best_fit_line(x2, y2), ([1, 2, 3], [10, 20, 30]))
        self.assertTupleEqual(best_fit_line(x3, y3), ([-5, 3, 11], [-10, 6, 22]))


if __name__ == '__main__':
    main()
