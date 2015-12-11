from ship import Ship

class Fleet:
    def __init__(self, game, id_, ships):
        self.game = game
        self.id = id_
        self.ships = ships
        self.expedition = None

        for ship in self.ships:
            ship.fleet = self

    def isReady(self):
        if not self.ships:
            return False
        for ship in self.ships:
            if not ship.isIdle() or ship.isBadlyBroken() or not ship.isFilled():
                return False
        return True

    def getShipHp(self):
        return [ ship.hp for ship in self.ships ]

    def setRunningExpedition(self, exp):
        self.expedition = exp

    def fill(self):
        if self.expedition is not None:
            return False
        for ship in self.ships:
            if not ship.isFilled():
                self.game.fill(self)
                for ship in self.ships:
                    ship.setFilled()
                return True
        return True

    def changeShips(self, ships):
        if self.expedition is not None:
            return False
        self.game.changeShips(self, ships)
        self.ships = ships
        for ship in ships:
            ship.fleet = self
        return True
