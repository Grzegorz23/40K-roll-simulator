# A-tf,A-atk,A-s,A-ap,A-wound,A-bs,A-ws,A-sv2,A-models,A-inv,A-dmg
# B-tf,B-atk,B-s,B-ap,B-wound,B-bs,B-ws,B-sv2,B-models,B-inv,B-dmg
class Unit:
    Toughness = 0
    WS = 0
    BS = 0
    Wound = 0
    ATK = 0
    Strength = 0
    AP = 0
    SV = 0
    INV = 0
    Models = 0
    Dmg = 0

    def __init__(self,TF,atk,S,ap,sv,inv,ws,bs,wound,models,dmg):
        self.Toughness = TF
        self.ATK = atk
        self.Strength = S
        self.AP = ap
        self.SV = sv
        self.INV = inv
        self.WS = ws
        self.BS = bs
        self.Wound = wound
        self.Models = models
        self.Dmg = dmg



    