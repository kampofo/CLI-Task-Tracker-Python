import argparse
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("args", nargs="+", help="1 to 3 positional arguments")

    parsed = parser.parse_args()
    args = parsed.args

    if not (1 <= len(args) <= 3):
        print("Error: Expected between 1 and 3 arguments.")
        parser.print_usage()
        sys.exit(1)
    else:
        print("1 - 3 arguments present!")


if __name__ == "__main__":
    main()
