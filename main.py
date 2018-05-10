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
    network_thread = threading.Thread(target=network_handle.loop)
    network_thread.start()

    engine = Master_engine(network_handle, args)
    engine_thread = threading.Thread(target=engine.loop)
    engine_thread.start()

    while True:
        user_input = input(">").strip().lower()
        if user_input == "stop":
            # To gracefully shut down the thread, use this approach.
            # After the loops in loop methods, implement everything required for a graceful shutdown.
            engine.running = False
            network_handle.running = False
            break

if __name__ == '__main__':
    main(sys.argv)
