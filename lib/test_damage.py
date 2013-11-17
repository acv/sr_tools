#!/usr/bin/env python

import damage
import unittest

class TestDamage(unittest.TestCase):
    def test_damage_01(self):
        d = damage.DamageValue('7P')
        self.assertFalse(d.is_special)
        self.assertEqual(d.damage, 7)
        self.assertEqual(d.damage_type, 'P')
        self.assertEqual(str(d), '7P')

    def test_damage_02(self):
        d = damage.DamageValue('9P (f)')
        self.assertTrue(d.is_special)
        self.assertEqual(d.damage, 9)
        self.assertEqual(d.damage_type, 'P')
        self.assertEqual(d.special_type, 'f')
        self.assertEqual(str(d), '9P (f)')

    def test_damage_03(self):
        with self.assertRaises(damage.InvalidDamageCode):
            d = damage.DamageValue('55R (x)')

    def test_damage_sum_01(self):
        d = damage.DamageValue('-2S (e)')
        d2 = damage.DamageValue('8P')
        ds = d + d2

        self.assertTrue(ds.is_special)
        self.assertEqual(ds.damage, 6)
        self.assertEqual(ds.damage_type, 'S')
        self.assertEqual(ds.special_type, 'e')
        self.assertEqual(str(ds), '6S (e)')

        ds = d2 + d

        self.assertTrue(ds.is_special)
        self.assertEqual(ds.damage, 6)
        self.assertEqual(ds.damage_type, 'S')
        self.assertEqual(ds.special_type, 'e')
        self.assertEqual(str(ds), '6S (e)')

    def test_damage_sum_02(self):
        d = damage.DamageValue('+2P (f)')
        d2 = damage.DamageValue('8P')
        ds = d + d2

        self.assertTrue(ds.is_special)
        self.assertEqual(ds.damage, 10)
        self.assertEqual(ds.damage_type, 'P')
        self.assertEqual(ds.special_type, 'f')
        self.assertEqual(str(ds), '10P (f)')

    def test_damage_sum_03(self):
        d = damage.DamageValue('+2P (f)')
        d2 = damage.DamageValue('-2S (e)')
        ds = d + d2

        self.assertTrue(ds.is_special)
        self.assertEqual(ds.damage, 0)
        self.assertEqual(ds.damage_type, 'S')
        self.assertEqual(ds.special_type, 'e')
        self.assertEqual(str(ds), '+0S (e)')

        ds = d2 + d

        self.assertTrue(ds.is_special)
        self.assertEqual(ds.damage, 0)
        self.assertEqual(ds.damage_type, 'P')
        self.assertEqual(ds.special_type, 'f')
        self.assertEqual(str(ds), '+0P (f)')

    def test_damage_sum_04(self):
        d = damage.DamageValue('4P')
        d2 = damage.DamageValue('3S')

        with self.assertRaises(TypeError):
            ds = d + d2

        with self.assertRaises(TypeError):
            ds = d + '3S'

if __name__ == '__main__':
        unittest.main()
