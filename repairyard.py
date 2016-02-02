from ship import Ship
from log import Log

from datetime import datetime, timedelta

class RepairYard:
    def __init__(self, game, id_, ship = None, endTime = None):
        self.game = game
        self.id = id_
        self.ship = ship
        self.endTime = endTime

        if ship is not None:
            ship.status = Ship.Repairing

    def repair(self, ship):
        if self.ship is not None:
            Log.i('Repair yard is busy (repairing %s)' % self.ship.getName())
            return None
        if not ship.isInjured():
            Log.i('%s is not injured' % ship.getName())
        if not ship.isIdle():
            Log.i('%s is not idle' % ship.getName())
        if (not ship.isInjured()) or (not ship.isIdle()):
            return None
        self.ship = ship
        self.endTime = self.game.repair(ship, self)
        ship.status = Ship.Repairing
        Log.i("Repairing %s, will finish at %s" % (ship.getName(), self.endTime))
        return self.endTime

    def smartRepair(self, ship):
        self.repair(ship)
        if self.ship is None:
            return False

        if (self.endTime - datetime.now()) > timedelta(hours = 2):
            self.instantRepair()
            return True
        else:
            return False

    def complete(self):
        if self.ship is None or datetime.now() < self.endTime:
            return False
        self.game.repairComplete(self)
        self.ship.setRepaired()
        self.ship.status = Ship.Idle
        Log.i("Ship %s is repaired" % self.ship.getName())
        self.ship = None
        self.endTime = None
        return True
