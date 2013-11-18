#!/usr/bin/env python

from dices import DiceRoller
from damage import DamageValue

shooting_effects = ['missed', 'grazed', 'soaked', 'damaged']

class ShootingEffect(object):
    def __init__(self, effect = None, damage = None, glitch = False,
                 critical_glitch = False):
        self.effect = effect
        if damage is None:
            self.damage = DamageValue('0S')
        else:
            self.damage = damage
        self.glitch = glitch
        self.critical_glitch = critical_glitch

class ShootingCharacter(object):
    def __init__(self, agility = 1, intuition = 1, reaction = 1, armor = 0,
                 body = 1, firearm = 1):
        self.agility = agility
        self.intuition = intuition
        self.reaction = reaction
        self.armor = armor
        self.body = body
        self.firearm = firearm

def shoot(shooter_char, shot_char, damage, accuracy, ap, attack_modifier = 0,
          defense_modifier = 0, verbose = False, roller = DiceRoller):
    attack_pool = shooter_char.agility + shooter_char.firearm

    defense_pool = shot_char.reaction + shot_char.intuition

    if verbose:
        print "Attack pool: [%d]\t\tDefense pool: [%d]" % (attack_pool,
                    defense_pool)

    attack_roll = roller(attack_pool, limit = accuracy)
    attack_result = attack_roll.roll(attack_modifier)

    if verbose:
        print "Attack roll: %s\t\t(hits: %d)" % (attack_result.roll,
                    attack_result.hits)

    glitch = False
    if attack_result.is_glitch:
        glitch = True

    if attack_result.is_critical_glitch:
        if verbose:
            print "Critical Glitch!\n"
        return ShootingEffect('missed', glitch = glitch, critical_glitch = True)

    defense_roll = roller(defense_pool)
    defense_result = defense_roll.roll(defense_modifier)

    if verbose:
        print "Defense roll: %s\t\t(hits: %d)" % (defense_result.roll,
                    defense_result.hits)

    net_hits = attack_result.hits - defense_result.hits
    if net_hits < 0 or (net_hits == 0 and attack_result.hits == 0):
        if verbose:
            print "Missed!\n"
        return ShootingEffect('missed', glitch = glitch)
    elif net_hits == 0 and attack_result.hits > 0:
        if verbose:
            print "Grazed!\n"
        return ShootingEffect('grazed', glitch = glitch)

    damage_mod = DamageValue('+%d%s' % (net_hits, damage.damage_type))
    raw_damage = damage + damage_mod

    net_armor = shot_char.armor + ap
    if net_armor < 0:
        net_armor = 0
    if raw_damage.damage_type == 'P' and raw_damage.damage <= net_armor:
        raw_damage += DamageValue('-0S')

    if verbose:
        print "Damage to soak: [%s]\t\t(base: %s)" % (str(raw_damage),
                    str(damage))

    soak_pool = shot_char.body + net_armor
    soak_roll = roller(soak_pool)
    soak_result = soak_roll.roll()

    if verbose:
        print "Soak roll: %s\t\t(hits: %d)" % (soak_result.roll,
                    soak_result.hits) 

    net_damage = raw_damage
    if soak_result.hits > 0:
        net_damage += DamageValue('-%d%s' % (soak_result.hits,
                                             net_damage.damage_type))

    if net_damage.damage <= 0:
        if verbose:
            print "Soaked!\n"
        return ShootingEffect('soaked', glitch = glitch)
    else:
        if verbose:
            print "Damaged! (%s)\n" % (str(net_damage),)
        return ShootingEffect('damaged', damage = str(net_damage), glitch = glitch)
