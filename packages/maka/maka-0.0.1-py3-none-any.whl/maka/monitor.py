import os
from datetime import datetime


class monitor(object):
    def __init__(self, unique_id, log_path=""):
        self.unique_id = unique_id
        self.init = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.name = self.init + "_logfile.txt"
        self.path = os.path.join(log_path, self.name)
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        with open(self.path, "w") as file:
            file.write("Initializing Logging File at {} \n".format(self.init))
            file.write("............................................. \n".format(self.init))

    def log(self, text, indent=0):
        out = datetime.now().strftime("%H:%M:%S.%f") + (" " * 3 * (indent + 1)) + text
        with open(self.path, "a") as file:
            file.write(out + "\n")
        print(out)

    def error(self, text, indent=0):
        out = datetime.now().strftime("%H:%M:%S.%f") + (" " * 3 * (indent + 1)) + "ERROR: " + text
        with open(self.path, "a") as file:
            file.write(out + "\n")
        print(out)
