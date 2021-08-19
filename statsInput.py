import sys

from SpecialRules import SpecialRules
from Unit import Unit
from random import randint
from StatisticData import StatisticData
import re
import UnitDataParser

rollFlag = ""


def wound_table():
    value_str_tgh = unitA.Strength / unitB.Toughness

    if value_str_tgh >= 2.0:
        return 2
    elif 2.0 > value_str_tgh > 1.0:
        return 3
    elif value_str_tgh == 1.0:
        return 4
    elif 0.5 < value_str_tgh < 1:
        return 5
    elif value_str_tgh <= 1 / 2:
        return 6


def roll(nrOfRolls, passRollValue):
    global rollFlag
    for i in range(nrOfRolls):
        roll_value = randint(1, 6)
        if rollFlag == "hit roll":
            if special_rules_unitA.ReRollHit > 0 \
                    and roll_value <= special_rules_unitA.ReRollHit:
                roll_value = randint(1, 6) + special_rules_unitA.AddToRollHit
            else:
                roll_value = roll_value + special_rules_unitA.AddToRollHit

        if rollFlag == "wound roll":
            if special_rules_unitA.APRoll >= roll_value:
                special_rules_unitA.NumberOfSpecialAPHits = special_rules_unitA.NumberOfSpecialAPHits + 1

            if 0 < special_rules_unitA.ExplodesRoll <= roll_value:
                special_rules_unitA.AdditionalWound = special_rules_unitA.AdditionalWound + special_rules_unitA.ExplodesWound

            if special_rules_unitA.ReRollWound > 0 \
                    and roll_value <= special_rules_unitA.ReRollWound:
                roll_value = randint(1, 6) + special_rules_unitA.AddToRollWound
            else:
                roll_value = roll_value + special_rules_unitA.AddToRollWound

        if rollFlag == "sv roll":
            if special_rules_unitA.ReRollSV > 0 \
                    and roll_value <= special_rules_unitA.ReRollSV:
                roll_value = randint(1, 6) + special_rules_unitA.AddToRollSV
            else:
                roll_value = roll_value + special_rules_unitA.AddToRollSV

        if rollFlag == "inv roll":
            if special_rules_unitA.ReRollINV > 0 \
                    and roll_value <= special_rules_unitA.ReRollINV:
                roll_value = randint(1, 6) + special_rules_unitA.AddToRollINV
            else:
                roll_value = roll_value + special_rules_unitA.AddToRollINV

        if roll_value >= passRollValue:
            yield roll_value
        else:
            yield False
    rollFlag = ""


def hit_roll():
    global rollFlag
    global battle_type
    if battle_type is "Melee":
        mode = unitA.WS
    else:
        mode = unitA.BS
    rollFlag = "hit roll"
    return [i for i in (roll(unitA.ATK * unitA.Models, mode)) if i is not False]


def wound_roll(hitRoll):
    global rollFlag
    rollFlag = "wound roll"
    return [i for i in (roll(len(hitRoll), wound_table())) if i is not False]


def sv_inv_roll(woundRoll):
    global rollFlag
    final_hit_table = []
    ap = unitA.AP
    for i in range(len(woundRoll)):
        SaveRoll = 0
        if i <= special_rules_unitA.NumberOfSpecialAPHits:
            unitA.AP = special_rules_unitA.SpecialAP

        if unitB.INV > 0:
            if unitB.SV + unitA.AP <= unitB.INV:
                rollFlag = "sv roll"
                SaveRoll = next(roll(1, unitB.SV + unitA.AP))
                if SaveRoll is not False:
                    final_hit_table.append(SaveRoll)
                unitA.AP = ap
            else:
                rollFlag = "inv roll"
                SaveRoll = next(roll(1, unitB.INV))
                if SaveRoll is not False:
                    final_hit_table.append(SaveRoll)
        else:
            rollFlag = "sv roll"
            SaveRoll = next(roll(1, unitB.SV + unitA.AP))
            if SaveRoll is not False:
                final_hit_table.append(SaveRoll)
            unitA.AP = ap

    return final_hit_table


def final_hits(wound_roll, save_roll):
    return wound_roll[:len(wound_roll) - len(save_roll)]


def dmgParser():
    statistic_data.woundHandedOut = 0
    for i in range(len(statistic_data.finalHit)):
        if unitA.Dmg.isdecimal():
            dealtDmg = unitA.Dmg
        else:
            add = 0
            roll = int(re.findall("d(.*)", unitA.Dmg)[0])
            if re.findall('(.*)d', unitA.Dmg)[0].isdecimal():
                add = int(re.findall('(.*)d', unitA.Dmg)[0])
            dealtDmg = (randint(1, roll) + add)

        statistic_data.woundHandedOut = statistic_data.woundHandedOut + int(dealtDmg)
    return statistic_data.woundHandedOut + special_rules_unitA.AdditionalWound


def main():
    # add if for -ap input
    # 6 mortal wound special rule
    # rerrol 1 special rule
    # dodatkowe ataki

    for i in range(statistic_data.nrOfSimulation):
        a = hit_roll()
        statistic_data.woundRoll = wound_roll(a)


        statistic_data.saveRoll = sv_inv_roll(statistic_data.woundRoll)
        statistic_data.finalHit = final_hits(statistic_data.woundRoll, statistic_data.saveRoll)
        statistic_data.woundRollTableAdd(statistic_data.woundRoll)
        statistic_data.saveRollTableAdd(statistic_data.saveRoll)
        statistic_data.finalHitTableAdd(statistic_data.finalHit)
        statistic_data.simulationListAdd(statistic_data.finalHit)
        statistic_data.woundHandedOutTable.append(dmgParser())
        special_rules_unitA.AdditionalWound = 0


    print(sum(statistic_data.simulationList) / len(statistic_data.simulationList))
    print(statistic_data.simulationList)
    print(statistic_data.woundHandedOutTable)
    print((sum(statistic_data.woundHandedOutTable) / len(statistic_data.woundHandedOutTable)))

    with open("result.txt", "a+") as result_file:
        result_file.write("Average hits: "
                          + str(sum(statistic_data.simulationList) / len(statistic_data.simulationList)) +
                          "\nAverage wound: "
                          + str((sum(statistic_data.woundHandedOutTable) / len(statistic_data.woundHandedOutTable))))


def get_stats(file,type):

    fraction = re.findall(type+' Fraction: (.*)', file)[0]
    unit = re.findall(type+ ' Unit: (.*)', file)[0]
    weapon = re.findall(type+' Weapon/Profile: (.*)', file)[0]
    try:
        armour = re.findall(type+' Armour: (.*)', file)[0]
    except:
        armour = 0
    model = re.findall(type+' Models: (.*)', file)[0]
    return UnitDataParser.find_file_in_folder(fraction, unit, weapon, armour), model


if __name__ == '__main__':
    with open("data.txt") as file:
        read_file = file.read()

    statistic_data = StatisticData()
    statistic_data.nrOfSimulation = int(re.findall('Number Of Simulation = (.*)', read_file)[0])

    special_rules_unitA = SpecialRules()
    Astats, Amodel = get_stats(read_file,"Attacker")
    Bstats, Bmodel = get_stats(read_file,"Blocker")
    battle_type = Astats[1]["Type"]

    unitA = Unit(TF=int(Astats[0]["T"]),
                 atk=int(Astats[0]["A"]),
                 S=int(Astats[0]["S"])+int(Astats[1]["S"].replace("+","")),
                 ap=int(Astats[1]["AP"].replace("-","")),
                 wound=int(Astats[0]["W"]),
                 bs=int(Astats[0]["BS"].replace("+","")),
                 ws=int(Astats[0]["WS"].replace("+","")),
                 sv=int(Astats[0]["Save"].replace("+","")),
                 models=int(Amodel),
                 inv=int(re.findall("\d",Astats[2]["Description"])[0]),
                 dmg=Astats[1]["D"])

    unitB = Unit(TF=int(Bstats[0]["T"]),
                 atk=int(Bstats[0]["A"]),
                 S=int(Bstats[0]["S"]),
                 ap=int(Bstats[1]["AP"].replace("-", "")),
                 wound=int(Bstats[0]["W"]),
                 bs=int(Bstats[0]["BS"].replace("+","")),
                 ws=int(Bstats[0]["WS"].replace("+","")),
                 sv=int(Bstats[0]["Save"].replace("+", "")),
                 models=int(Bmodel),
                 inv=int(re.findall("\d", Bstats[2]["Description"])[0]),
                 dmg=Bstats[1]["D"])

    main()
