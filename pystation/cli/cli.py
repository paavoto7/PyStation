import argparse
import sys

from tabulate import tabulate

from ..funcs.currency import store
from ..gui.station_gui import main_app
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
        "--country",
        help="Set country to specify currency.",
        default="United States",
    )

    args = parser.parse_args()

    store_code = store(args.country)

    if args.single:
        table = single(args.single, store_code)

    elif args.gui_single:
        table = single(args.gui_single, store_code, True)
        sys.exit(0)

    elif args.gui_multi:
        table = main_app(multi(store_code, True))
        sys.exit(0)

    elif args.multi:
        table = multi(store_code)

    else:
        sys.exit("Something went wrong. Refer to the help.")
    # Print using tabulate
    print(tabulate(table, headers=["Title", "Original price", "Discounted price"]))


if __name__ == "__main__":
    main()
