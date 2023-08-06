from time import time


class Timer:
    def __init__(self):
        self.start()

    def __get_time(self):
        return time() * 1000

    def start(self):
        self.start_time = self.__get_time()

    def get_elapsed(self):
        return self.__get_time() - self.start_time
