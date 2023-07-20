import multiprocessing as mp
from typing import Callable


class Pool:
    __pool: mp.Pool
    __max_proc: int
    __args: list = []
    __func: Callable
    __lock: mp.Lock
    def __init__(self, max_proc: int):
        self.__max_proc = max_proc
        self.__pool = mp.Pool(self.__max_proc)
        self.__lock = mp.Lock()

    def add_target_func(self, func: Callable):
        self.__func = func

    def add_args(self, args: list):
        self.__args = args

    def add_arg(self, arg):
        self.__args.append([*arg, self.__lock])

    def run(self):
        self.__pool.map(self.__func, self.__args)