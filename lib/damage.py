#!/usr/bin/env python

import re

damage_code_re = re.compile(r'^(-?\d\d*)([PS])(\s\s*\(([^)]*)\))?$')

class InvalidDamageCode(Exception):
    pass

class DamageValue(object):
    def __init__(self, damage_code):
        self.damage_code = damage_code
        self.damage_type = None
        self.damage = 0
        self.is_special = False
        self.is_modifier = False
        self.special_type = None

        self.parse_damage_code(damage_code)

    def parse_damage_code(self, damage_code):
        global damage_code_re

        if damage_code.startswith('-'):
            self.is_modifier = True
        elif damage_code.startswith('+'):
            self.is_modifier = True
            damage_code = damage_code[1:]
        
        match = damage_code_re.match(damage_code)
        if not match:
            raise InvalidDamageCode("Damage code [%s] is invalid." % (damage_code,))
        
        self.damage = int(match.group(1))
        self.damage_type = match.group(2)
        if match.group(4):
            self.is_special = True
            self.special_type = match.group(4)

    def __str__(self):
        dv_str = "%d%s" % (self.damage, self.damage_type)
        if self.damage >= 0 and self.is_modifier:
            dv_str = '+' + dv_str
        if self.is_special:
            dv_str += " (%s)" % (self.special_type,)
        return dv_str

    def __add__(self, other):
        if not isinstance(other, DamageValue):
            return NotImplemented
        if not other.is_modifier and not self.is_modifier:
            return NotImplemented
        
        new_dv = DamageValue(self.damage_code)
        if new_dv.is_modifier and not other.is_modifier:
            # Assumption: special damage stripped by modifier...
            new_dv.damage = other.damage + new_dv.damage
            new_dv.is_modifier = False
        else:
            new_dv.damage += other.damage
            new_dv.damage_type = other.damage_type
            new_dv.is_special = other.is_special
            new_dv.special_type = other.special_type
            if not (new_dv.is_modifier and other.is_modifier):
                new_dv.is_modifier = False

        new_dv.damage_code = str(new_dv)
        return new_dv

