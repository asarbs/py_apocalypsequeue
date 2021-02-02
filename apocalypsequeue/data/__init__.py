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
        #plt.figure(figsize=(10.24, 16.00), dpi=100)
        fig, axs = plt.subplots(2)
        fig.set_figheight(15)
        fig.set_figwidth(15)

        number_of_infected, = axs[0].plot('time_step', 'number_of_infected', data=df, marker='', color='#1f77b4', linewidth=1)
        number_of_new_infected, = axs[0].plot('time_step', 'number_of_new_infected', data=df, marker='', color='#ff7f0e', linewidth=1)
        number_of_healthy, = axs[0].plot('time_step', 'number_of_healthy', data=df, marker='', color='#2ca02c', linewidth=1)
        number_of_clients_in_queue, = axs[0].plot('time_step', 'number_of_clients_in_queue', data=df, marker='', color='#d62728', linewidth=1)
        axs[1].bar('time_step', 'number_of_infection', data=df, color='#6f1787')

        axs[0].set_xlabel("Czas [krok symulacji]")
        axs[0].set_ylabel("Liczba klientów")
        axs[0].set_title("Statysyki klientów w czasie")
        axs[0].legend([number_of_infected, number_of_new_infected, number_of_healthy, number_of_clients_in_queue],
                   ['Liczba wszystkich zainfekowanych', 'Liczba zainfekowanych w trakcie symulacji', 'Liczba zdrowych', 'Liczba klientów w kolejce'])

        axs[1].set_xlabel("Czas [krok symulacji]")
        axs[1].set_ylabel("Liczba infeksji")
        axs[1].set_title("Liczba infekcji w kroku symulacji")

        plt.savefig('{}_time.png'.format(Data.filename), dpi=100)
