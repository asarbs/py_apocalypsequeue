from apocalypse import Client
from console_args import CONSOLE_ARGS
from system.MapElements.MapElementType import MapElementType
from system.pathfinding import dijkstras_algorithm
import logging
import random
import threading
from datetime import datetime



class AgentBuilder(threading.Thread):
    def __init__(self, agents_wait_list, type_nav_graph_nodes, nav_graph_node_dic):
        super(AgentBuilder, self).__init__()
        self.__agents_count = 0
        self.__agents_wait_list = agents_wait_list
        self.__nav_graph_node_dic = nav_graph_node_dic
        self.type_nav_graph_nodes = type_nav_graph_nodes

    def run(self):
        while self.__agents_count < CONSOLE_ARGS.number_of_clients:
            start_time = datetime.now()
            self.__agents_count += 1
            start_node = random.choice(self.type_nav_graph_nodes[MapElementType.ENTRANCE])
            target_cash_register = random.choice(self.type_nav_graph_nodes[MapElementType.CASH_REGISTER])
            middle_steps = random.sample(self.type_nav_graph_nodes[MapElementType.SHELF], CONSOLE_ARGS.num_of_stops)
            infected = random.random() < CONSOLE_ARGS.init_infec
            canInfect = infected
            nodes_to_visit = [start_node] + middle_steps + [target_cash_register]
            path = self.__build_agent_path(nodes_to_visit)
            client = Client(start_node=start_node, path=path, infected=infected, canInfect=canInfect,
                target_cash_register=target_cash_register)
            self.__agents_wait_list.append(client)
            end_time = datetime.now()
            logging.debug('AgentBuilder new client={} delta={}[s]'.format(client, (end_time-start_time).total_seconds()))

    def __build_agent_path(self, nodes_to_visit):
        path = []
        for i in range(0, len(nodes_to_visit) - 1 , 1):
            start_node = nodes_to_visit[i]
            end_node = nodes_to_visit[i+1]
            path += dijkstras_algorithm(self.__nav_graph_node_dic, start_node, end_node)
        return path