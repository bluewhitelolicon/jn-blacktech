from ship import Ship

class Fleet:
    def __init__(self, game, id_, ships, isRunningExp):
        self.game = game
        self.id = id_
        self.ships = ships
        if isRunningExp:
            for ship in self.ships:
                ship.status = Ship.RunningExpedition

    def isReady(self):
        if not self.ships:
            return False
        for ship in self.ships:
            if ship.status != Ship.Idle or ship.isBadlyBroken() or not ship.isFilled():
                return False
        return True

    def setRunningExpedition(self, status):
        for ship in self.ships:
            if status:
                ship.status = Ship.RunningExpedition
            else:
                ship.status = Ship.Idle
