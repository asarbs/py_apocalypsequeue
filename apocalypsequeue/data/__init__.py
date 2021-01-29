from datetime import datetime


class Data:
    now = datetime.now() # current date and time
    date_time = now.strftime("%Y%m%d_%H%M%S_time")
    filename = '{}.csv'.format(date_time)

    def __init__(self):
        self.outdata = {}

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

    def dump(self):
        csvfile = open(Data.filename, "w+")
        csvfile.write(
            "time step; num_of_timesteps;number of infected; number of new infected;number of healthy; number of clients in queue\n")
        for time_step in self.outdata:
            # {"number_of_infected": 0, "number_of_new_infected": 0, "number_of_clients_in_queue": 0, "number_of_healthy": 0}
            line = '{};{};{:.2f};{:.2f};{:.2f};{:.2f}\n'.format(time_step,
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