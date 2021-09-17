import time
from threading import Thread


class Progressbar:
    def __init__(self, total, prefix):
        self.go_to = 0
        self.this_step = 0
        self.total = total
        self.prefix = prefix
        self.fast = False

    def start(self):
        progress_thread = Thread(target=self.run())
        progress_thread.daemon = True
        progress_thread.start()

    def run(self):
        while self.this_step <= self.total:
            sleeping_time = 0.1 if self.fast else 0.5
            if self.this_step <= self.go_to:
                self.printProgressBar(self.this_step)
                time.sleep(sleeping_time)
            else:
                time.sleep(sleeping_time)

    def progress_to(self, value):
        self.go_to = value

    def printProgressBar(self, iteration, suffix='', decimals=1,
                         length=100, fill='█', printEnd="\r"):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(self.total)))
        filledLength = int(length * iteration // self.total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'{self.prefix} |{bar}| {percent}% {suffix}', end=printEnd)

        if iteration == self.total:
            print("\n")
