import os
import logging
import numpy as np
from scipy.io.matlab import loadmat
from multiprocessing import Queue, Process


class MultiThreadDataset:
    """
    Multi-thread Dataset
    
    Never call .next() in multi-thread/process program!
    """
    def __init__(self, data_path, data_loader, thread=1, sort_by_name=False):
        self.thread = thread
        self.data_paths = [os.path.join(data_path, p) for p in os.listdir(data_path)]
        if sort_by_name:
            self.data_paths.sort(key=lambda x: int(os.path.basename(x).split('.')[0]))
        self.length = len(self.data_paths)
        self.data_paths.extend([self.data_paths[0] for _ in range(thread)])
        self.idx = 0
        self.data = Queue()
        self.get_data = data_loader
        self._process = []
        while self.idx < thread:
            process = Process(target=self.get_data, args=(self.data_paths[self.idx], self.data))
            process.start()
            self._process.append(process)
            self.idx += 1
        self.get = 0

    def next(self):
        if self.get >= self.length:
            return None
        if self.idx >= self.length + self.thread:
            datum = self.data.get()
            self._process[0].terminate()
            self._process.pop(0)
            self.get += 1
            return datum
        datum = self.data.get()
        self._process[0].terminate()
        self._process.pop(0)
        process = Process(target=self.get_data, args=(self.data_paths[self.idx], self.data))
        process.start()
        self._process.append(process)
        self.idx += 1
        self.get += 1
        return datum

    def __len__(self):
        return self.length


def get_channel(datum_path):
    Mat = loadmat(datum_path)
    return Mat['H'], Mat['Hhat'], np.sum(Mat['C'], 0), Mat['Epsilon']


def get_channel2queue(datum_path, queue: Queue):
    queue.put(get_channel(datum_path))


class Channels(MultiThreadDataset):
    def __init__(self, data_path, thread=1, sort_by_name=False):
        super().__init__(data_path, get_channel2queue, thread, sort_by_name)
