#!/usr/bin/env python

import random
from math import ceil

class DiceRoll(object):
    def __init__(self, roll, limit = None):
        self.raw_hits = 0
        self.hits = 0
        self.is_success = False
        self.is_glitch = False
        self.is_critical_glitch = False
        self.roll = roll

        num_dices = len(roll)
        num_hits = 0
        num_glitches = 0

        for result in roll:
            if result in (5, 6):
                num_hits += 1
            elif result == 1:
                num_glitches += 1

        if num_hits > 0:
            self.is_success = True

        self.raw_hits = num_hits
        self.hits = num_hits
        if limit is not None:
            if self.hits > limit:
                self.hits = limit

        if num_glitches >= ceil(float(num_dices) / 2.0) and len(roll) > 0:
            self.is_glitch = True

        if self.is_glitch and not self.is_success:
            self.is_critical_glitch = True

class DiceRoller(object):
    def __init__(self, dices_to_roll, limit = None):
        self.dices_to_roll = dices_to_roll
        self.limit = limit
        self.random = random.SystemRandom()

    def _roll_dices(self, dices_to_roll):
        result = []
        random_gen = self.random
        for i in xrange(dices_to_roll):
            result.append(random_gen.randint(1, 6))
        return result

    def roll(self, modifier = 0):
        dices_to_roll = self.dices_to_roll + modifier
        return DiceRoll(self._roll_dices(dices_to_roll), self.limit)
