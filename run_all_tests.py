import unittest
import os

def run_all_tests():
    """Discover and run all the tests in the 'tests' directory."""
    # Define the path to the 'tests' directory
    test_dir = 'tests'

    # Discover all test cases in the 'tests' directory
    loader = unittest.TestLoader()
    suite = loader.discover(test_dir)

    # Create a test runner that outputs the results
    runner = unittest.TextTestRunner(verbosity=2)

    # Run the test suite
    result = runner.run(suite)

    # Check if any tests failed
    if result.wasSuccessful():
        print("\nAll tests passed successfully.")
    else:
        print("\nSome tests failed. Please review the output above.")

if __name__ == '__main__':
    run_all_tests()
