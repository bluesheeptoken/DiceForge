from typing import *
from dataclasses import dataclass
from collections import defaultdict, Counter
import numpy as np


@dataclass
class Proba:
    def __init__(self, proba: Dict[int, int]):
        self.proba: DefaultDict[int, int] = defaultdict(
            int, proba
        )  # number of faces -> face

    @staticmethod
    def from_list(l: List[int]):
        c = Counter(l)
        return Proba(defaultdict(int, c))

    def __add__(self, proba: "Proba") -> "Proba":
        new_proba = defaultdict(int)
        for k, v in self.proba.items():
            for k2, v2 in proba.proba.items():
                new_proba[k + k2] += v * v2
        return Proba(new_proba)

    def normalize(self):
        total = self.total_possibilities()
        new_proba = defaultdict(int)
        for k, v in self.proba.items():
            new_proba[k] = v / total
        return new_proba

    def luck(self, threshold):
        count = 0
        for k, v in self.proba.items():
            if threshold <= k:
                count += v
        return count / self.total_possibilities()

    def total_possibilities(self) -> int:
        return sum(self.proba.values())

    def __mul__(self, value: int) -> "Proba":
        proba = self
        for _ in range(value - 1):
            proba += self
        return proba

    def inverse_cum_sum(self):
        l = np.zeros(max(self.proba.keys()) + 1)
        for k, v in self.proba.items():
            l[k] = v
        l = l[::-1].cumsum()[::-1]
        l /= l[0]  # l[0] is max of the list by definition
        return l[l > 0.01]
