import os
import re
import xml.etree.ElementTree as ET

def unit_data_parser(path,what_to_find):
    data = {}
    root = ET.parse(path).getroot()
    for elem in root.iter():
        if re.search("profile$",elem.tag):
            if re.search("'name': '"+str(what_to_find)+"',", str(elem.attrib)):
                for profile_child in elem:
                    if re.search("characteristics", profile_child.tag):
                        for characteristics_child in profile_child:
                            if re.search("characteristic", characteristics_child.tag):
                                data[characteristics_child.attrib["name"]] = characteristics_child.text
            elif (what_to_find == 0):
                data['Description'] = '0'
    return data


def find_file_in_folder(fraction,unit,weapon,armour):
    ret = []
    path = "DATA\wh40k"
    stats_to_find = [unit,weapon,armour]
    for i in stats_to_find:
        for file in os.listdir(r"DATA\wh40k"):
            if file.endswith(".cat") and re.search(fraction, str(file)):
                ret.append(unit_data_parser(path+"\\"+file,i))

    return ret

