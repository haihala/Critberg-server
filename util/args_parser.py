"""
Module for the method for parsing command line arguments to a more usable format.

Assuming the following:
* We only have keyword args.
* Keyword parameters are ordered properly.

This holy shite turned out barely readable, but it should work.

"""

import copy

DEFAULT_ARGS = {
    "ruleset": {

    }, "networking": {
        "port": 6969
    }
}

ACCEPTED_ARGS = {
    # 'path' of arg: (amount of arguments [mandatory, optional], acceptable aliases)
    # mandatory arguments must come first
    "networking/port": ((1, 0), ("-p", "-port"))
}


def parse_args(argv):
    args = copy.deepcopy(DEFAULT_ARGS)
    # One could just args = DEFAULT_ARGS, but if we want to display differences somewhere this is probably better.
    argv = [i.strip().lower() for i in argv]

    for i in range(len(argv)):
        if i != len(argv) - 1:
            # Argument at i is followed by a value.
            for arg in ACCEPTED_ARGS:
                template = ACCEPTED_ARGS[arg]
                if argv[i] in template[1]:
                    mandatories = argv[i+1:i+1+template[0][0]]
                    optionals = []

                    for optional in argv[i+1+template[0][0]:min(i+1+template[0][0]+template[0][1], len(argv))]:
                        if optional[0] == "-":  # Dumb assumption for optimization reasons.
                            break
                        optionals.append(optional)

                    category, argument = arg.split("/")
                    args[category][argument] = [*mandatories, *optionals]

    return args