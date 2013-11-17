#!/usr/bin/env python

import dices
import unittest

class TestDices(unittest.TestCase):
    def test_roller(self):
        roller = dices.DiceRoller(12, limit = 2) # Expect 4 hits average
        sum_without_limit = 0
        for i in xrange(10000):
            roll = roller.roll()
            sum_without_limit += roll.raw_hits
            
            if roll.is_glitch:
                self.assertLessEqual(roll.raw_hits, 6)
                if roll.is_critical_glitch:
                    self.assertEqual(roll.raw_hits, 0)
                    self.assertFalse(roll.is_success)

            if roll.raw_hits > 0 and roll.raw_hits <= 2:
                self.assertEqual(roll.raw_hits, roll.hits)
                self.assertTrue(roll.is_success)
            elif roll.raw_hits > 2:
                self.assertEqual(roll.hits, 2)
                self.assertTrue(roll.is_success)
            else:
                self.assertEqual(roll.hits, 0)
                self.assertFalse(roll.is_success)
        
        average_hits = float(sum_without_limit) / 10000.0
        self.assertTrue(average_hits < 4.1 and average_hits > 3.9)

    def test_roller_modifier(self):
        roller = dices.DiceRoller(6)

        for i in xrange(100):
            roll = roller.roll(-5)
            self.assertLessEqual(roll.raw_hits, 1)

    def test_roll_critical_glitch(self):
        roll = dices.DiceRoll([1, 1, 1, 4, 3, 2])

        self.assertTrue(roll.is_glitch)
        self.assertTrue(roll.is_critical_glitch)
        self.assertFalse(roll.is_success)
        self.assertEqual(roll.hits, 0)
        self.assertEqual(roll.raw_hits, 0)

    def test_roll_glitch(self):
        roll = dices.DiceRoll([1, 1, 1, 4, 3, 5])

        self.assertTrue(roll.is_glitch)
        self.assertFalse(roll.is_critical_glitch)
        self.assertTrue(roll.is_success)
        self.assertEqual(roll.hits, 1)
        self.assertEqual(roll.raw_hits, 1)

    def test_roll_failure(self):
        roll = dices.DiceRoll([1, 1, 3, 4, 3, 2])

        self.assertFalse(roll.is_glitch)
        self.assertFalse(roll.is_critical_glitch)
        self.assertFalse(roll.is_success)
        self.assertEqual(roll.hits, 0)
        self.assertEqual(roll.raw_hits, 0)

    def test_roll_success(self):
        roll = dices.DiceRoll([1, 1, 6, 4, 3, 2])

        self.assertFalse(roll.is_glitch)
        self.assertFalse(roll.is_critical_glitch)
        self.assertTrue(roll.is_success)
        self.assertEqual(roll.hits, 1)
        self.assertEqual(roll.raw_hits, 1)

    def test_roll_success_limited(self):
        roll = dices.DiceRoll([1, 6, 6, 5, 5, 2], limit = 3)

        self.assertFalse(roll.is_glitch)
        self.assertFalse(roll.is_critical_glitch)
        self.assertTrue(roll.is_success)
        self.assertEqual(roll.hits, 3)
        self.assertEqual(roll.raw_hits, 4)

if __name__ == '__main__':
        unittest.main()
