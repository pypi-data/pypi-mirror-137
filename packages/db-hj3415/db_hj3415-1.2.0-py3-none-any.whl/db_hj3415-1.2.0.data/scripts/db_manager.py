import sys
import argparse
import pprint

from db_hj3415 import mongo2, dbpath

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

if __name__ == '__main__':
    present_addr = dbpath.load()

    # reference form https://docs.python.org/3.3/howto/argparse.html#id1
    # create the top-level parser
    parser = argparse.ArgumentParser(
        prog="db_manager",
        description="Mongo database setting program",
    )
    subparsers = parser.add_subparsers(
        title='Subcommands',
        description='valid subcommands',
        help='Additional help',
        dest="subcommand"
    )

    # create the parser for the "format" command
    format_parser = subparsers.add_parser(
        'format',
        description=f"Initialize database - {present_addr}",
        help='Format whole database')

    # create the parser for the "address" command
    address_parser = subparsers.add_parser(
        'address',
        description=f"Help to set the mongo database address",
        help='Help to set the mongo database address',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"{pprint.pformat(dbpath.make_path(('<ID>','<PASS>')))}"
    )
    address_parser.add_argument('cmd', choices=['set', 'print'])
    address_parser.add_argument('-t', choices=['ATLAS', 'INNER', 'LOCAL', 'OUTER'])
    address_parser.add_argument('-i', help='Set id with address')
    address_parser.add_argument('-p', help='Set password with address')

    args = parser.parse_args()
    logger.debug(args)

    if args.subcommand == 'format':
        print(f"DB address : {present_addr}")
        val = input("Do you really want to format database? (y/N)")
        if val == "y" or val == "Y":
            client = mongo2.connect_mongo(present_addr)
            mongo2.Atlas(client).initiate_db()
            print("Done.")
        else:
            print("Cancelled.")
        sys.exit()
    elif args.subcommand == 'address':
        if args.cmd == 'print':
            print(present_addr)
        elif args.cmd == 'set':
            path = dbpath.make_path((args.i, args.p))[args.t]
            # print(path)
            # mongo2.connect_mongo(path)
            dbpath.save(path)
    else:
        parser.print_help()
        sys.exit()
