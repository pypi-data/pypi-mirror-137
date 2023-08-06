import sys
import argparse

from db_hj3415 import mongo2, dbpath


import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)


if __name__ == '__main__':
    # reference form https://docs.python.org/3.3/howto/argparse.html#id1
    parser = argparse.ArgumentParser(
        prog="db_manager",
        description="mongo database setting program",
        epilog="end."
    )
    parser.add_argument('cmd', help=f"format savepath loadpath")
    parser.add_argument('-addr', '--address', choices=, help='Set mongo db address')

    args = parser.parse_args()

    if args.cmd == 'format':
        addr = dbpath.load()
        print(f"DB address : {addr}")
        val = input("Do you really want to format database? (y/N)")
        if val == "y" or val == "Y":
            client = mongo2.connect_mongo(addr)
            mongo2.Atlas(client).initiate_db()
            print("Done.")
        else:
            print("Cancelled.")
        sys.exit()
    else:
        parser.print_help()
        sys.exit()
