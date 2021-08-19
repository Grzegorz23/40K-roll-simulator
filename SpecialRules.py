import re


class SpecialRules:
    SpecialAP = 0
    APRoll = 0
    NumberOfSpecialAPHits = 0
    ExplodesRoll = 0
    ExplodesWound = 0
    AdditionalWound = 0
    ReRollHit = 0
    ReRollWound = 0
    ReRollSV = 0
    ReRollINV = 0
    AddToRollHit = 0
    AddToRollWound = 0
    AddToRollSV = 0
    AddToRollINV = 0
    def __init__(self):

        with open("data.txt") as file:
            read_file = file.read()

        if int(re.findall('Explodes: (.*) mortal: .*', read_file)[0]) > 0:
            self.ExplodesRoll = int(re.findall('Explodes: (.*) mortal: .*', read_file)[0])
            self.ExplodesWound = int(re.findall('Explodes: .* mortal: (.*)', read_file)[0])

        if int(re.findall('Special AP: (.*) roll: .*', read_file)[0]) > 0:
            self.SpecialAP = int(re.findall('Special AP: (.*) roll: .*', read_file)[0])
            self.APRoll = int(re.findall('Special AP: .* roll: (.*)', read_file)[0])

        if int(re.findall('Re-Roll Wound: (.*)', read_file)[0]) > 0:
            self.ReRollWound = int(re.findall('Re-Roll Wound: (.*)', read_file)[0])

        if int(re.findall('Re-Roll Hit: (.*)', read_file)[0]) > 0:
            self.ReRollHit = int(re.findall('Re-Roll Hit: (.*)', read_file)[0])

        if int(re.findall('Re-Roll SV: (.*)', read_file)[0]) > 0:
            self.ReRollSV = int(re.findall('Re-Roll SV: (.*)', read_file)[0])

        if int(re.findall('Re-Roll INV: (.*)', read_file)[0]) > 0:
            self.ReRollINV = int(re.findall('Re-Roll INV: (.*)', read_file)[0])

        if int(re.findall('Add to wound roll: (.*)', read_file)[0]) > 0:
            self.ReRollINV = int(re.findall('Add to wound roll: (.*)', read_file)[0])

        if int(re.findall('Add to hit roll: (.*)', read_file)[0]) > 0:
            self.ReRollINV = int(re.findall('Add to hit roll: (.*)', read_file)[0])

        if int(re.findall('Add to SV roll: (.*)', read_file)[0]) > 0:
            self.ReRollINV = int(re.findall('Add to SV roll: (.*)', read_file)[0])

        if int(re.findall('Add to INV roll: (.*)', read_file)[0]) > 0:
            self.ReRollINV = int(re.findall('Add to INV roll: (.*)', read_file)[0])


