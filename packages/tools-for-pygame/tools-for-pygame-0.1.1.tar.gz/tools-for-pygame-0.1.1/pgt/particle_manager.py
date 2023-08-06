#!/usr/bin/env python3

import time
from typing import Callable


class ParticleManager:
    def __init__(self,
                 draw_func: Callable,
                 update_func: Callable,
                 deletion_check: Callable,
                 update_rate: float = 0):
        self.particles = []
        self.draw_func = draw_func
        self.update_func = update_func
        self.del_check = deletion_check
        self.update_rate = update_rate
        self.last_updated = time.perf_counter()

    def add_particle(self, attributes: list):
        self.particles.append(attributes)

    def update(self):
        to_del = []
        for idx, particle in enumerate(self.particles):
            self.update_func(particle)
            if self.del_check(particle):
                to_del.append(idx)
        for i in reversed(to_del):
            del self.particles[i]

    def draw(self, surface):
        if time.perf_counter() - self.last_updated > self.update_rate:
            self.update()
            self.last_updated = time.perf_counter()
        for i in self.particles:
            self.draw_func(i, surface)
