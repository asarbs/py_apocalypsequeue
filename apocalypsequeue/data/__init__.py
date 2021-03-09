from datetime import datetime
import matplotlib.pyplot as plt
import pprint
import pandas as pd
import pygame
import argparse
import os
from console_args import CONSOLE_ARGS


class Data:
    now = datetime.now() # current date and time
    date_time = now.strftime("%Y%m%d_%H%M%S")
    filename = 'simulation_{}'.format(date_time)

    def __init__(self):
        self.outdata = {}
        self.contact_time = {}
        for i in range (0, CONSOLE_ARGS.inf_distance+1):
            self.contact_time[i] = 0
        self.infectionPos = []

        if CONSOLE_ARGS.clean == True:
            for fname in os.listdir("."):
                if fname.startswith('simulation_'):
                    os.remove(os.path.join(".", fname))

    def addTimeData(self, time_step):
        if time_step not in self.outdata:
            self.outdata[time_step] = {"time_step": 0, "number_of_infected": 0, "number_of_new_infected": 0, "number_of_infection": 0, 'number_of_clients':0}

    def addStats(self, clients_lists, time_step):
        self.outdata[time_step]["time_step"] += 1
        self.outdata[time_step]['number_of_clients'] += len(clients_lists)
        for c in clients_lists:
            if c.isInfected():
                self.outdata[time_step]["number_of_infected"] += 1
                if not c.canInfect():
                    self.outdata[time_step]["number_of_new_infected"] += 1

    def add_infection_params(self, pos, time):
        self.infectionPos.append(pos)
        self.outdata[time]["number_of_infection"] += 1

    def addContactTime(self, distance):
        self.contact_time[round(distance)] += 1

    def dump(self, screen, map_elements):
        self.__save_time_data()
        self.__save_pos_data(screen, map_elements)
        self.__save_time_data_plot()

    def __save_pos_data(self, screen, map_elements):
        posfile = open('{}_pos.csv'.format(Data.filename), "w+")
        for map_element in map_elements:
            map_element.draw(screen, (0, 0))
        for p in self.infectionPos:
            posfile.write('{},{}\n'.format(p[0], p[1]))
            pygame.draw.circle(screen, (255,0,0), p, radius=5)
        posfile.close()
        pygame.image.save(screen, '{}.jpeg'.format(Data.filename))

    def __save_time_data(self):
        csvfile = open('{}_time.csv'.format(Data.filename), "w+")
        csvfile.write(
            "time step; num_of_timesteps;number of infected; number of new infected;number of healthy; number of clients in queue; number_of_infections\n")
        for time_step in self.outdata:
            if self.outdata[time_step]["time_step"] > 0:
                line = '{}|{}|{:.2f}|{:.2f}|{:.2f}\n'.format(time_step,
                                                                (self.outdata[time_step]["number_of_clients"]           / self.outdata[time_step]["time_step"]),
                                                                (self.outdata[time_step]["number_of_infected"]          / self.outdata[time_step]["time_step"]),
                                                                (self.outdata[time_step]["number_of_new_infected"]      / self.outdata[time_step]["time_step"]),
                                                                (self.outdata[time_step]["number_of_infection"]         / self.outdata[time_step]["time_step"])
                                                                )
            csvfile.write(line.replace(".", ","))
        csvfile.close()

    def __save_time_data_plot(self):
        df_dic = {
            'time_step': self.outdata.keys(),
            'number_of_clients': [],
            'number_of_infected': [],
            'number_of_new_infected': [],
            'number_of_infection': []
        }
        for time_step in self.outdata:
            if self.outdata[time_step]["time_step"] > 0:
                df_dic['number_of_clients'].append         (self.outdata[time_step]['number_of_clients'] / self.outdata[time_step]["time_step"])
                df_dic['number_of_infected'].append        (self.outdata[time_step]["number_of_infected"] / self.outdata[time_step]["time_step"])
                df_dic['number_of_new_infected'].append    (self.outdata[time_step]["number_of_new_infected"] / self.outdata[time_step]["time_step"])
                df_dic['number_of_infection'].append       (self.outdata[time_step]["number_of_infection"] / self.outdata[time_step]["time_step"])
            else:
                df_dic['number_of_clients'].append         (0)
                df_dic['number_of_infected'].append        (0)
                df_dic['number_of_new_infected'].append    (0)
                df_dic['number_of_infection'].append       (0)

        df = pd.DataFrame(df_dic)
        fig, axs = plt.subplots(3)
        fig.suptitle("Simulation params: infection_distance {}m; infection_threshold={}".format(CONSOLE_ARGS.inf_distance, CONSOLE_ARGS.infection_threshold ))
        fig.set_figheight(21)
        fig.set_figwidth(15)

        number_of_clients, =  axs[0].plot('time_step', 'number_of_clients', data=df, marker='', color='#a10c06', linewidth=1)
        number_of_infected, = axs[0].plot('time_step', 'number_of_infected', data=df, marker='', color='#1f77b4', linewidth=1)
        number_of_new_infected, = axs[0].plot('time_step', 'number_of_new_infected', data=df, marker='', color='#ff7f0e', linewidth=1)
        axs[1].bar('time_step', 'number_of_infection', data=df, color='#6f1787')

        contact_time_values = (x / CONSOLE_ARGS.num_of_repeat_max for x in self.contact_time.values())
        axs[2].bar(range(len(self.contact_time)), list(contact_time_values), color='#6f1787')

        axs[0].set_xlabel("Czas [krok symulacji]")
        axs[0].set_ylabel("Liczba klientów")
        axs[0].set_title("Statysyki klientów w czasie")
        axs[0].legend([number_of_clients, number_of_infected, number_of_new_infected],
                   ['Liczba wszystkich klientów', 'Liczba wszystkich zainfekowanych', 'Liczba zainfekowanych w trakcie symulacji'])

        axs[1].set_xlabel("Czas [krok symulacji]")
        axs[1].set_ylabel("Liczba infeksji")
        axs[1].set_title("Liczba infekcji w kroku symulacji")

        axs[2].set_xlabel("Dystans")
        axs[2].set_ylabel("Czas [krok symulacji]")
        axs[2].set_title("Średni czas spędzony w zagrożonej stefie.")

        plt.savefig('{}_time.png'.format(Data.filename), dpi=100)
