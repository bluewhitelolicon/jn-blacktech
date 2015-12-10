from log import Log

from datetime import datetime

class Expedition:
    def __init__(self, game, id_, time, fleetRequirement, basicAward, extraAward):
        self.game = game
        self.id = id_
        self.time = time
        self.fleetRequirement = fleetRequirement
        self.basicAward = basicAward
        self.extraAward = extraAward
        self.fleet = None
        self.endTime = None

    def setStatus(self, fleet, endTime):
        self.fleet = fleet
        self.endTime = endTime
        fleet.setRunningExpedition(self)

    def start(self, fleet):
        if not fleet.isReady() or not self.fleetRequirement.acceptFleet(fleet):
            return None
        self.endTime = self.game.startExpedition(self, fleet)
        self.fleet = fleet
        fleet.setRunningExpedition(self)
        Log.i("Fleet " + str(fleet.id) + " has started expedition " + str(self.id))
        Log.i("    will return at " + self.endTime.time().__str__().split('.')[0])
        return self.endTime

    def getResult(self):
        if self.fleet is None or datetime.now() < self.endTime:
            return None
        bigSuccess, resource = self.game.getExpeditionResult(self)
        self.game.addResource(resource)
        self.fleet.setRunningExpedition(None)
        self.fleet = None
        self.endTime = None
        return bigSuccess

class FleetRequirement:
    def __init__(self, shipNum, flagShipLv, numOfType):
        self.shipNum = shipNum
        self.flagShipLv = flagShipLv
        self.numOfType = numOfType

    def acceptFleet(self, fleet):
        if len(fleet.ships) < self.shipNum or fleet.ships[0].lv < self.flagShipLv:
            return False

        check = self.numOfType.copy()
        for ship in fleet.ships:
            if ship.getShipType() in check:
                check[ship.getShipType()] -= 1
        for rest in check.values():
            if rest > 0:
                return False

        return True
