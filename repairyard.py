from ship import Ship

from datetime import datetime

class RepairYard:
    def __init__(self, game, id_, ship = None, endTime = None):
        self.game = game
        self.id = id_
        self.ship = ship
        self.endTime = endTime

    def repair(self, ship):
        if self.ship is not None:
            return None
        if not ship.isInjured():
            return None
        self.ship = ship
        self.endTime = self.game.repair(ship, self)
        ship.status = Ship.Repairing
        return self.endTime

    def repairComplete(self):
        if self.ship is None or datetime.now() < self.endTime:
            return False
        self.game.repairComplete(self)
        self.ship.setRepaired()
        self.ship.status = Ship.Idle
        self.ship = None
        self.endTime = None
        return True
