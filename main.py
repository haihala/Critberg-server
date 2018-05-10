"""
Main script. This is what starts the server.

"""

from engine.master_engine import Master_engine

from util.networking import Network
from util.args_parser import parse_args

import threading
import sys

def main(args):
    args = parse_args(args)
    network_handle = Network(args["networking"])
    engine = Master_engine(network_handle, args)

    engine_thread = threading.Thread(target=engine.loop)
    engine_thread.start()

    while True:
        user_input = input(">").strip().lower()
        if user_input == "stop":
            engine.running = False
            break

if __name__ == '__main__':
    main(sys.argv)
