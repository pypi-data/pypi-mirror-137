import sys
import argparse

from db_hj3415 import mongo2


import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)


if __name__ == '__main__':
    # reference form https://docs.python.org/3.3/howto/argparse.html#id1
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', help=f"format")

    args = parser.parse_args()

    if args.cmd == 'format':
        val = input("Really?(y/N)")
        if val == "y" or val == "Y":
            client = mongo2.connect_mongo(mongo2.ATLAS_ADDR)
            mongo2.Atlas(client).initiate_db()
            print("Done.")
        else:
            print("Cancelled.")
        sys.exit()
    else:
        parser.print_help()
        sys.exit()
