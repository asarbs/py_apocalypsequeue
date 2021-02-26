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
            self.outdata[time_step] = {"time_step": 0, "number_of_infected": 0, "number_of_new_infected": 0,
                                       "number_of_clients_in_queue": 0, "number_of_healthy": 0, "number_of_infection": 0}

    def addStats(self, clients_lists, time_step):

        # if time_step not in self.outdata:
        #     self.outdata[time_step] = {"time_step": 0, "number_of_infected": 0, "number_of_new_infected": 0,
        #                           "number_of_clients_in_queue": 0, "number_of_healthy": 0}
        self.outdata[time_step]["time_step"] += 1
        for c in clients_lists:
            if c.isInfected():
                self.outdata[time_step]["number_of_infected"] += 1
                if not c.canInfect():
                    self.outdata[time_step]["number_of_new_infected"] += 1
            else:
                self.outdata[time_step]["number_of_healthy"] += 1
            if c.standingInQueue():
                self.outdata[time_step]["number_of_clients_in_queue"] += 1

    def add_infection_params(self, pos, time):
        self.infectionPos.append(pos)
        self.outdata[time]["number_of_infection"] += 1

    def addContactTime(self, distance):
        self.contact_time[round(distance)] += 1

    def dump(self, screen):
        self.__save_time_data()
        self.__save_pos_data(screen)
        self.__save_time_data_plot()

    def __save_pos_data(self, screen):
        posfile = open('{}_pos.csv'.format(Data.filename), "w+")
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
            # {"number_of_infected": 0, "number_of_new_infected": 0, "number_of_clients_in_queue": 0, "number_of_healthy": 0}
            line = '{}|{}|{:.2f}|{:.2f}|{:.2f}|{:.2f}|{:.2f}\n'.format(time_step,
                                                                self.outdata[time_step]["time_step"],
                                                                (self.outdata[time_step]["number_of_infected"]          / self.outdata[time_step]["time_step"]),
                                                                (self.outdata[time_step]["number_of_new_infected"]      / self.outdata[time_step]["time_step"]),
                                                                (self.outdata[time_step]["number_of_healthy"]           / self.outdata[time_step]["time_step"]),
                                                                (self.outdata[time_step]["number_of_clients_in_queue"]  / self.outdata[time_step]["time_step"]),
                                                                (self.outdata[time_step]["number_of_infection"]         / self.outdata[time_step]["time_step"])
                                                                )
            csvfile.write(line.replace(".", ","))
        csvfile.close()

    def __save_time_data_plot(self):
        df_dic = {
            'time_step': self.outdata.keys(),
            'number_of_infected': [],
            'number_of_new_infected': [],
            'number_of_healthy': [],
            'number_of_clients_in_queue': [],
            'number_of_infection': []
        }
        for time_step in self.outdata:
            df_dic['number_of_infected'].append        (self.outdata[time_step]["number_of_infected"] / self.outdata[time_step]["time_step"])
            df_dic['number_of_new_infected'].append    (self.outdata[time_step]["number_of_new_infected"] / self.outdata[time_step]["time_step"])
            df_dic['number_of_healthy'].append         (self.outdata[time_step]["number_of_healthy"] / self.outdata[time_step]["time_step"])
            df_dic['number_of_clients_in_queue'].append(self.outdata[time_step]["number_of_clients_in_queue"] / self.outdata[time_step]["time_step"])
            df_dic['number_of_infection'].append       (self.outdata[time_step]["number_of_infection"] / self.outdata[time_step]["time_step"])


        df = pd.DataFrame(df_dic)
        fig, axs = plt.subplots(3)
        fig.suptitle("Simulation params: infection_distance {}[j] = {}m; infection_threshold={}".format(CONSOLE_ARGS.inf_distance, round((CONSOLE_ARGS.inf_distance/3.3),2), CONSOLE_ARGS.infection_threshold ))
        fig.set_figheight(21)
        fig.set_figwidth(15)

        number_of_infected, = axs[0].plot('time_step', 'number_of_infected', data=df, marker='', color='#1f77b4', linewidth=1)
        number_of_new_infected, = axs[0].plot('time_step', 'number_of_new_infected', data=df, marker='', color='#ff7f0e', linewidth=1)
        number_of_healthy, = axs[0].plot('time_step', 'number_of_healthy', data=df, marker='', color='#2ca02c', linewidth=1)
        number_of_clients_in_queue, = axs[0].plot('time_step', 'number_of_clients_in_queue', data=df, marker='', color='#d62728', linewidth=1)
        axs[1].bar('time_step', 'number_of_infection', data=df, color='#6f1787')

        contact_time_values = (x / CONSOLE_ARGS.num_of_repeat_max for x in self.contact_time.values())
        axs[2].bar(range(len(self.contact_time)), list(contact_time_values), color='#6f1787')

        axs[0].set_xlabel("Czas [krok symulacji]")
        axs[0].set_ylabel("Liczba klientów")
        axs[0].set_title("Statysyki klientów w czasie")
        axs[0].legend([number_of_infected, number_of_new_infected, number_of_healthy, number_of_clients_in_queue],
                   ['Liczba wszystkich zainfekowanych', 'Liczba zainfekowanych w trakcie symulacji', 'Liczba zdrowych', 'Liczba klientów w kolejce'])

        axs[1].set_xlabel("Czas [krok symulacji]")
        axs[1].set_ylabel("Liczba infeksji")
        axs[1].set_title("Liczba infekcji w kroku symulacji")

        axs[2].set_xlabel("Dystans")
        axs[2].set_ylabel("Czas [krok symulacji]")
        axs[2].set_title("Średni czas spędzony w zagrożonej stefie.")

        plt.savefig('{}_time.png'.format(Data.filename), dpi=100)
