
import argparse
import logging

def _parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fps", help="number of fps for model", dest="fps", nargs='?', default=60, type=int)
    parser.add_argument("--client", help="number of agents in simulation", dest="number_of_clients", nargs='?', default=40, type=int)
    parser.add_argument("--repetition", help="number of repetitions of simulation", dest="num_of_repeat_max", nargs='?', default=100, type=int)
    parser.add_argument("--time", help="number of simulation steps", dest="time_step_max", nargs='?', default=400, type=int)
    parser.add_argument("--play", help="show simulation animation", dest="play_simulation", nargs='?', default=False, type=bool)
    parser.add_argument("--clean", help="remove old simulation files", dest="clean", nargs='?', default=False, type=bool)
    parser.add_argument('-d', '--debug', help="Print lots of debugging statements", action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.INFO)
    parser.add_argument('-v', '--verbose', help="Be verbose", action="store_const", dest="loglevel", const=logging.INFO)
    return parser.parse_args()

CONSOLE_ARGS =  _parse_arguments()

# optional: delete function after use to prevent calling from other place
del _parse_arguments