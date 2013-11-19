#!/usr/bin/env python

import optparse
from lib.damage import DamageValue
from lib.shooting import *

def parse_cmd_line():
    usage = """%prog [options]

This program resolves a shooting event in shadowrun 5e. 

"""
    parser = optparse.OptionParser(usage = usage)

    shooter = optparse.OptionGroup(parser, 'Attacker options')
    shooter.add_option("-A", "--accuracy", help = "Accuracy of weapon (default = 7)",
                      default = "7")
    shooter.add_option("-d", "--damage", help = "Base damage value of weapon " +
                      "(default = 7P)", default = "7P")
    shooter.add_option("-M", "--attack_modifier", default = "0",
                       help = "Modifiers to the attack roll (default = 0)")
    shooter.add_option("-p", "--attack_pool", help = "Attack pool starting size " +
                      "(default = 6)", default = "6")
    shooter.add_option("-P", "--armor_piercing", help = "Armor piercing value for " +
                      "firearm (default = 0)", default = "0")
    parser.add_option_group(shooter)

    target = optparse.OptionGroup(parser, "Defender options")
    target.add_option("-a", "--armor", help = "Defender armor value (default = 12)",
                      default = "12")
    target.add_option("-b", "--body", help = "Defender body (default = 4)",
                      default = "4")
    target.add_option("-i", "--intuition", help = "Defender intuition (default = 4)",
                      default = "4")
    target.add_option("-m", "--defensive_modifier", default = "0",
                      help = "Defensive modifier (default = 0)")
    target.add_option("-r", "--reaction", help = "Defender reaction (default = 7)",
                      default = "7")
    parser.add_option_group(target)

    (options, args) = parser.parse_args()

    try:
        DamageValue(options.damage)
    except Exception as e:
        parser.error("Invalid damage value [%s] (%s)" % (options.damage, str(e)))

    return options

def main():
    options = parse_cmd_line()

    shooter = ShootingCharacter(agility = 0, firearm = int(options.attack_pool))

    target = ShootingCharacter(intuition = int(options.intuition),
                               reaction = int(options.reaction),
                               armor = int(options.armor),
                               body = int(options.body))

    accuracy = int(options.accuracy)
    ap = int(options.armor_piercing)
    damage_value = DamageValue(options.damage)

    attack_modifier = int(options.attack_modifier)
    defensive_modifier = int(options.defensive_modifier)

    result = shoot(shooter, target, damage_value, accuracy, ap,
                   defense_modifier = defensive_modifier, verbose = True,
                   attack_modifier = attack_modifier)

if __name__ == '__main__':
    main()
