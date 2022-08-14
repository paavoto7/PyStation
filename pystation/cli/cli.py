import argparse
import sys

from tabulate import tabulate

from ..gui.station_gui import main_app

# from ..gui import Multi_display
from ..station import multi, single


def main():
    parser = argparse.ArgumentParser(description="Playstation Store price crawler")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-s",
        "--single",
        help="Get a single game price and information.",
        type=str,
        nargs="+",
    )
    group.add_argument(
        "-gs",
        "--gui_single",
        help="Same as single but with gui and picture",
        type=str,
        nargs="+",
    )
    group.add_argument(
        "-m", "--multi", help="Get all the sale prices and titles", action="store_true"
    )
    group.add_argument(
        "-gm",
        "--gui_multi",
        help="Same as multi but with gui and picture",
        action="store_true",
    )

    parser.add_argument(
        "-c,",
        "--currency",
        help="Set country to specify currency.",
        default="us",
    )

    args = parser.parse_args()

    if args.single:
        table = single(args.single, args.currency)

    elif args.gui_single:
        table = single(args.gui_single, args.currency, True)
        sys.exit(0)

    elif args.gui_multi:
        table = main_app(multi(args.currency, True))
        sys.exit(0)

    elif args.multi:
        table = multi(args.currency)

    else:
        sys.exit("Something went wrong. Refer to the help.")
    # Print using tabulate
    print(tabulate(table, headers=["Title", "Original price", "Discounted price"]))


if __name__ == "__main__":
    main()
