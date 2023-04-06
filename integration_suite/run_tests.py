import os
import sys
import unittest


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    auth_service_dir = os.path.join(current_dir, "auth")
    auth_methods_dir = os.path.join(auth_service_dir, "endpoints")
    tests_path = os.path.join(auth_methods_dir, "tests")
    sys.path.insert(0, auth_service_dir)

    loader = unittest.TestLoader()
    suite = loader.discover(tests_path)

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)


if __name__ == "__main__":
    main()
