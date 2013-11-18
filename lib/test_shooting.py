#!/usr/bin/env python

import dices
import unittest
from damage import DamageValue
from shooting import *

class LoadedDiceRoller(dices.DiceRoller):
    def roll_only(self, dices_to_roll, number):
        result = []
        for i in xrange(dices_to_roll):
            result.append(number)
        return result

class RollCriticalGlitch(LoadedDiceRoller):
    def _roll_dices(self, dices_to_roll):
        return self.roll_only(dices_to_roll, 1)

class RollFailure(LoadedDiceRoller):
    def _roll_dices(self, dices_to_roll):
        return self.roll_only(dices_to_roll, 2)

class RollSuccess(LoadedDiceRoller):
    def _roll_dices(self, dices_to_roll):
        return self.roll_only(dices_to_roll, 5)

class RollFiveFourThree(LoadedDiceRoller):
    def _roll_dices(self, dices_to_roll):
        roll = RollFiveFourThree.rolls.pop(0)
        result = []
        for i in xrange(dices_to_roll):
            if i < roll:
                result.append(5)
            else:
                result.append(2)
        return result

def get_guard():
    return ShootingCharacter(agility = 3, firearm = 4)

def get_runner():
    return ShootingCharacter(intuition = 6, reaction = 6, armor = 9, body = 8)

class TestShooting(unittest.TestCase):
    def test_shooting_char_01(self):
        guard = get_guard()

        self.assertEqual(guard.agility, 3)
        self.assertEqual(guard.intuition, 1)
        self.assertEqual(guard.reaction, 1)
        self.assertEqual(guard.armor, 0)
        self.assertEqual(guard.body, 1)
        self.assertEqual(guard.firearm, 4)

    def test_shooting_char_02(self):
        runner = get_runner()

        self.assertEqual(runner.agility, 1)
        self.assertEqual(runner.intuition, 6)
        self.assertEqual(runner.reaction, 6)
        self.assertEqual(runner.armor, 9)
        self.assertEqual(runner.body, 8)
        self.assertEqual(runner.firearm, 1)

    def test_shooting_effect(self):
        guard = get_guard()
        runner = get_runner()
        damage = DamageValue('10P')
        accuracy = 5
        ap = -2

        effect = shoot(guard, runner, damage, accuracy, ap, roller = RollCriticalGlitch)
        self.assertTrue(effect.glitch)
        self.assertTrue(effect.critical_glitch)
        self.assertEqual(effect.effect, 'missed')
        self.assertEqual(str(effect.damage), '0S')

        runner.intuition = 2
        runner.reaction = 1
        runner.body = 1
        effect = shoot(guard, runner, damage, accuracy, ap, roller = RollSuccess)
        self.assertFalse(effect.glitch)
        self.assertFalse(effect.critical_glitch)
        self.assertEqual(effect.effect, 'damaged')
        self.assertEqual(str(effect.damage), '4P')
        runner = get_runner()

        effect = shoot(guard, runner, damage, accuracy, ap, roller = RollFailure)
        self.assertFalse(effect.glitch)
        self.assertFalse(effect.critical_glitch)
        self.assertEqual(effect.effect, 'missed')
        self.assertEqual(str(effect.damage), '0S')

        RollFiveFourThree.rolls = [5, 4, 3]
        effect = shoot(guard, runner, damage, accuracy, ap, roller = RollFiveFourThree)
        self.assertFalse(effect.glitch)
        self.assertFalse(effect.critical_glitch)
        self.assertEqual(effect.effect, 'damaged')
        self.assertEqual(str(effect.damage), '8P')

        RollFiveFourThree.rolls = [7, 4, 3]
        effect = shoot(guard, runner, damage, accuracy, ap, roller = RollFiveFourThree)
        self.assertFalse(effect.glitch)
        self.assertFalse(effect.critical_glitch)
        self.assertEqual(effect.effect, 'damaged')
        self.assertEqual(str(effect.damage), '8P')

if __name__ == '__main__':
    unittest.main()
