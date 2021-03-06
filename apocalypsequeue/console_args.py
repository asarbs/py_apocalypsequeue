import argparse
import logging

def _parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fps", help="number of fps for model", dest="fps", nargs='?', default=60, type=int)
    parser.add_argument("--client", help="number of agents in simulation", dest="number_of_clients", nargs='?', default=40, type=int)
    parser.add_argument("--clients_mean_distribution", help="Parameter used in Poisson distribution", dest="clients_mean_distribution", nargs='?', default=50, type=int)
    parser.add_argument("--num_of_stops", help="Number of stop in front of shelves in store", dest="num_of_stops", nargs='?', default=50, type=int)
    parser.add_argument("--repetition", help="number of repetitions of simulation", dest="num_of_repeat_max", nargs='?', default=100, type=int)
    parser.add_argument("--infection_distance", help="Distance of infection area", dest="inf_distance", nargs='?', default=7, type=int)
    parser.add_argument("--init_infection", help="Rate of initial infected", dest="init_infec", nargs='?', default=0.2, type=float)
    parser.add_argument("--infection_threshold", help="threshold of particles which cause infection", dest="infection_threshold", nargs='?', default=0.9, type=float)
    parser.add_argument("--play", help="show simulation animation", dest="play_simulation", nargs='?', default=False, type=bool)
    parser.add_argument("--clean", help="remove old simulation files", dest="clean", nargs='?', default=False, type=bool)
    parser.add_argument('-d', '--debug', help="Print lots of debugging statements", action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.DEBUG)
    parser.add_argument('-v', '--verbose', help="Be verbose", action="store_const", dest="loglevel", const=logging.INFO)

    return parser.parse_args()

CONSOLE_ARGS  =  _parse_arguments()


# optional: delete function after use to prevent calling from other place
del _parse_arguments