""" Some functions used in multiple test functions """
import numpy as np
import unittest


def assert_two_parameters(true_value, test_value):
    """
        **Assert two parameters - accepts multiple types**
    """
    # TODO: improve robustness and readability
    test_case = unittest.TestCase()

    if isinstance(true_value, np.ndarray) or isinstance(true_value, list):
        if len(true_value) == 1:
            true_value = float(true_value)

    if isinstance(test_value, np.ndarray) or isinstance(test_value, list):
        if len(test_value) == 1:
            test_value = float(test_value)

    # Comparison
    if isinstance(test_value, np.ndarray) or isinstance(test_value, list):
        if np.array(true_value).ndim == 2:
            for i, test_row in enumerate(test_value):
                if isinstance(test_row[0], np.floating):
                    test_row = np.array(test_row).round(10)
                    true_value[i] = np.array(true_value[i]).round(10)

                test_case.assertListEqual(list(test_row), list(true_value[i]))
        else:
            if isinstance(test_value[0], np.floating):
                test_value = np.array(test_value).round(10)
                true_value = np.array(true_value).round(10)

            test_case.assertListEqual(list(test_value), list(true_value))
    else:
        test_case.assertEqual(test_value, true_value)