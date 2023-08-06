import os
from datetime import datetime


class monitor(object):
    def __init__(self, unique_id, log_path=""):
        self.unique_id = unique_id
        self.init = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.name = self.init + "_logfile.txt"
        self.path = os.path.join(log_path, self.name)
        self.red = '\033[31m'
        self.white = '\033[0m'
        self.green = '\033[32m'
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        with open(self.path, "w") as file:
            out = "Initializing Logging File at {}".format(self.init)
            file.write(out+"\n")
            print(out)
            out = "............................................."
            file.write(out+"\n")
            print(out)

    def log(self, text, indent=0):
        out = datetime.now().strftime("%H:%M:%S.%f") + (" " * 3 * (indent + 1)) + text
        with open(self.path, "a") as file:
            file.write(out + "\n")
        print(out)

    def error(self, text, indent=0):
        out = datetime.now().strftime("%H:%M:%S.%f") + (" " * 3 * (indent + 1)) + "ERROR: " + text
        with open(self.path, "a") as file:
            file.write(out + "\n")
        print(self.red + out + self.white)
