"""
Main script. This is what starts the server.

"""

from util.networking import init as network_init
from util.args_parser import parse_args

import threading
import sys

def main(args):
    args = parse_args(args)
    network_params = network_init(args["networking"])


if __name__ == '__main__':
    main(sys.argv)
