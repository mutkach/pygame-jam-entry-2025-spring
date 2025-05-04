from typing import Iterable, Iterator


class Linspace(Iterator):
    def __init__(self, lbound, rbound, steps):
        self.pos = lbound
        self.rbound = rbound
        self.lbound = lbound
        self.step = (rbound-lbound)/steps
        
    def __iter__(self):
        return self

    def __next__(self):
        self.pos += self.step
        if self.pos > self.rbound:
            raise StopIteration
        return self.pos
            
