class StatisticData:
    nrOfSimulation = 0
    woundRoll = 0
    saveRoll = 0
    finalHit = 0
    woundHandedOut = 0
    woundRollTable = []
    saveRollTable = []
    finalHitTable = []
    woundHandedOutTable = []
    simulationList = []


    def woundRollTableAdd(self,woundRoll):
        return self.woundRollTable.append(woundRoll)
    def saveRollTableAdd(self,saveRoll):
        return self.saveRollTable.append(saveRoll)
    def finalHitTableAdd(self,finalHit):
        return self.finalHitTable.append(finalHit)
    def simulationListAdd(self,finalHit):
        return self.simulationList.append(len(finalHit))
