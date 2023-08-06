import argparse


def command_line_arg() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-q",
        "--query",
        required=True,
        help="Query to show."

    )
    parser.add_argument(
        "-l",
        "--lang",
        help="Preferred News Based On Language",
        default="en"
    )
    parser.add_argument(
        "-s",
        "--size",
        help="How many documents to show.",
        default=10
    )
    args = parser.parse_args()
    return args
