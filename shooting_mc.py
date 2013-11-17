#!/usr/bin/env python

import optparse
from lib.damage import DamageValue
from lib.shooting import *

def monte_carlo(shooter, target, columns, rolls, damage_value, accuracy, ap,
                defensive_modifier, attack_modifier):
    raw_results = []

    for bonus in xrange(columns):
        raw_results.append({})
        for i in xrange(rolls):
            result = shoot(shooter, target, damage_value, accuracy, ap,
                           defense_modifier = defensive_modifier,
                           attack_modifier = (bonus + attack_modifier))
            damage = str(result.damage)
            if result.critical_glitch:
                damage = 'Critical Glitch!'
            elif result.effect != 'damaged':
                damage = result.effect.capitalize() + '!'
            if damage not in raw_results[bonus]:
                raw_results[bonus][damage] = 0
            raw_results[bonus][damage] += 1
            if result.effect == 'damaged':
                if 'Hit!' not in raw_results[bonus]:
                    raw_results[bonus]['Hit!'] = 0
                    raw_results[bonus]['Stun!'] = 0
                    raw_results[bonus]['Physical!'] = 0
                raw_results[bonus]['Hit!'] += 1
                if damage.endswith('P'):
                    raw_results[bonus]['Physical!'] += 1
                elif damage.endswith('S'):
                    raw_results[bonus]['Stun!'] += 1

    return raw_results

def print_table(shooter, raw_results, rolls, attack_modifier):
    columns = len(raw_results)
    rows = set()
    longest = 0
    for bonus in xrange(columns):
        for label in raw_results[bonus]:
            if label not in rows:
                rows.add(label)
                if len(label) > longest:
                    longest = len(label)

    def print_full_bar():
        print "\t+-" + ('-' * longest) + '-+' + ((('-' * 10) + '+') * columns)

    format_str = "\t| %" + str(longest) + "s |" + (' %8.8s |' * columns)

    print "\n\t+-" + ('-' * longest) + '-+' + (('-' * ((10 * columns) + columns - 1)) + '+')
    label = ' Attack Pool Size'
    print "\t| " + (' ' * longest) + ' |' + (label + (' ' * ((10 * columns) + 
                        columns - 1 - len(label))) + '|')
    print "\t| " + (' ' * longest) + ' +' + ((('-' * 10) + '+') * columns)
    raw_pool = shooter.agility + shooter.firearm + attack_modifier
    args = ['']
    for i in xrange(columns):
        args.append(str(raw_pool + i))
    print format_str % tuple(args)
    print_full_bar()

    words = []
    stun = []
    physical = []

    for row in rows:
        if row.endswith('S'):
            stun.append(int(row[:-1]))
        elif row.endswith('P'):
            physical.append(int(row[:-1]))
        else:
            words.append(row)

    result = []
    for row in sorted(words):
        result.append(row)
    words = result

    result = []
    for row in sorted(stun):
        result.append(str(row) + 'S')
    stun = result

    result = []
    for row in sorted(physical):
        result.append(str(row) + 'P')
    physical = result

    def print_rows(rows):
        for label in rows:
            args = [label]
            for i in xrange(columns):
                if label in raw_results[i]:
                    args.append(str(float(raw_results[i][label]) / rolls * 100))
                else:
                    args.append(' -')

            print format_str % tuple(args)
        print_full_bar()

    print_rows(words)
    if len(stun) > 0:
        print_rows(stun)
    if len(physical) > 0:
        print_rows(physical)

def print_sim_details(shooter, target, accuracy, ap, dv, columns, rolls,
                      defensive_modifier, attack_modifier):
    print "\nShadowrun 5 Firearms Combat Damage Simulator\n"
    print "Simulation Details:"
    print "\tNumber of columns:           %d" % (columns,)
    print "\tNumber of rolls per columns: %d" % (rolls,)
    print "\nAttacker Details:"
    print "\tBase Attack Pool:            %d" % ((shooter.agility +
                                                  shooter.firearm),)
    print "\tAttack Modifier:             %d" % (attack_modifier,)
    print "\tWeapon Damage Value:         %s" % (str(dv),)
    print "\tWeapon Accuracy:             %d" % (accuracy,)
    print "\tWeapon Armor Piercing:       %d" % (ap,)
    print "\nDefender Details:"
    print "\tArmor:                       %d" % (target.armor,)
    print "\tBody:                        %d" % (target.body,)
    print "\tIntuition:                   %d" % (target.intuition,)
    print "\tReaction:                    %d" % (target.reaction,)
    print "\tDefensive Modifier:          %d" % (defensive_modifier,)

def parse_cmd_line():
    usage = """%prog [options]

This program runs a monte-carlo simulation to evaluate the effect of various
attack pool size when shooting a specific weapon against a runner. The stats
are provided through command-line arguments and an ASCII table is printed
summarizing the stats (expressed as % of attacks).

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

    sim = optparse.OptionGroup(parser, "Simulation options")
    sim.add_option("-c", "--columns", help = "Number of columns (attack pool " +
                      "steps) to plot (default = 8)", default = "8")
    sim.add_option("-I", "--iterations", help = "Number of iterations of the " +
                      "simulation to run for each column. (default = 10000)",
                      default = "10000")
    parser.add_option_group(sim)

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

    columns = int(options.columns)
    rolls = int(options.iterations)

    accuracy = int(options.accuracy)
    ap = int(options.armor_piercing)
    dv = DamageValue(options.damage)

    attack_modifier = int(options.attack_modifier)
    defensive_modifier = int(options.defensive_modifier)

    print_sim_details(shooter, target, accuracy, ap, dv, columns, rolls,
                      defensive_modifier, attack_modifier)

    raw_results = monte_carlo(shooter, target, columns, rolls, dv, accuracy, ap,
                              defensive_modifier, attack_modifier)
    print_table(shooter, raw_results, rolls, attack_modifier)

if __name__ == '__main__':
    main()
