from datetime import datetime
import matplotlib.pyplot as plt
import pprint
import pandas as pd
import pygame

class Data:
    now = datetime.now() # current date and time
    date_time = now.strftime("%Y%m%d_%H%M%S")
    filename = '{}'.format(date_time)

    def __init__(self):
        self.outdata = {}
        self.infectionPos = []

    def addStats(self, clients_lists, time_step):

        if time_step not in self.outdata:
            self.outdata[time_step] = {"time_step": 0, "number_of_infected": 0, "number_of_new_infected": 0,
                                  "number_of_clients_in_queue": 0, "number_of_healthy": 0}
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

    def add_infection_params(self, pos):
        self.infectionPos.append(pos)

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
            "time step; num_of_timesteps;number of infected; number of new infected;number of healthy; number of clients in queue\n")
        for time_step in self.outdata:
            # {"number_of_infected": 0, "number_of_new_infected": 0, "number_of_clients_in_queue": 0, "number_of_healthy": 0}
            line = '{}|{}|{:.2f}|{:.2f}|{:.2f}|{:.2f}\n'.format(time_step,
                                                                self.outdata[time_step]["time_step"],
                                                                (self.outdata[time_step]["number_of_infected"] /
                                                                 self.outdata[time_step]["time_step"]),
                                                                (self.outdata[time_step]["number_of_new_infected"] /
                                                                 self.outdata[time_step]["time_step"]),
                                                                (self.outdata[time_step]["number_of_healthy"] /
                                                                 self.outdata[time_step]["time_step"]),
                                                                (self.outdata[time_step]["number_of_clients_in_queue"] /
                                                                 self.outdata[time_step]["time_step"])
                                                                )
            csvfile.write(line.replace(".", ","))
        csvfile.close()

    def __save_time_data_plot(self):
        df_dic = {
            'time_step': self.outdata.keys(),
            'number_of_infected': [],
            'number_of_new_infected': [],
            'number_of_healthy': [],
            'number_of_clients_in_queue': []
        }
        for time_step in self.outdata:
            df_dic['number_of_infected'].append        (self.outdata[time_step]["number_of_infected"] / self.outdata[time_step]["time_step"])
            df_dic['number_of_new_infected'].append    (self.outdata[time_step]["number_of_new_infected"] / self.outdata[time_step]["time_step"])
            df_dic['number_of_healthy'].append         (self.outdata[time_step]["number_of_healthy"] / self.outdata[time_step]["time_step"])
            df_dic['number_of_clients_in_queue'].append(self.outdata[time_step]["number_of_clients_in_queue"] / self.outdata[time_step]["time_step"])


        df = pd.DataFrame(df_dic)
        number_of_infected, = plt.plot('time_step', 'number_of_infected', data=df, marker='', color='#1f77b4', linewidth=1)
        number_of_new_infected, = plt.plot('time_step', 'number_of_new_infected', data=df, marker='', color='#ff7f0e', linewidth=1)
        number_of_healthy, = plt.plot('time_step', 'number_of_healthy', data=df, marker='', color='#2ca02c', linewidth=1)
        number_of_clients_in_queue, = plt.plot('time_step', 'number_of_clients_in_queue', data=df, marker='', color='#d62728', linewidth=1)
        plt.legend([number_of_infected, number_of_new_infected, number_of_healthy, number_of_clients_in_queue],
                   ['number_of_infected', 'number_of_new_infected', 'number_of_healthy', 'number_of_clients_in_queue'])
        plt.savefig('{}_time.png'.format(Data.filename))
