from argparse import ArgumentParser

from . import __version__
from .say import say

__all__ = ["main"]


def main(args=None) -> None:
    parser = ArgumentParser(description="Prints a talking skeleton")
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("text", help="What to make the skeleton say")
    args = parser.parse_args(args)
    print(say(args.text))


# test with: pipenv run python -m skeleton_says
if __name__ == "__main__":
    main()
