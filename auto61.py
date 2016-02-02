from battle import Battle
from ship import Ship
from log import Log

# Train ships at 6-1-A automatically
class Auto61:
    def __init__(self, game, fleet, ships, mustRepair, needInstRepair, dismantleList):
        self.game = game
        self.fleet = fleet
        self.ships = ships
        # whether or not the ships can continue fighting when HP is lower than 1/2
        self.mustRepair = mustRepair
        # to repair large ship instantly
        self.needInstRepair = needInstRepair # TODO: not work when mustRepair is False
        # when get a new ship, dismantle it if it's in this list
        self.dismantleList = dismantleList
        # backup the ships before 6-1 start
        self.formerShips = None
        # whether or not 6-1 is running
        self.isLooping = False

    def tryGetReady(self):
        # Check if the fleet is ready
        if self.fleet.expedition is not None:
            return False

        # Check if ships are ready
        for i in range(len(self.ships)):
            if not self.ships[i].isIdle():
                Log.i("Ship %s is not idle" % self.ships[i].getName())
                return False
            if self.ships[i].isBroken() and self.mustRepair[i]:
                Log.i("Ship %s needs repair" % self.ships[i].getName())
                return False
            if self.ships[i].isBadlyBroken():
                Log.i("Ship %s is broken" % self.ships[i].getName())
                return False

        self.formerShips = self.fleet.ships
        self.fleet.changeShips(self.ships)
        self.fleet.fill()
        self.isLooping = True
        return True

    def canRun(self):
        if not self.isLooping:
            return False
        for i in range(len(self.ships)):
            if self.ships[i].isBroken() and self.mustRepair[i]:
                if self.needInstRepair[i]:
                    self.ships[i].instantRepair()
                else:
                    return False
        return self.fleet.isReady()

    def run(self):
        if not self.canRun():
            return False
        battle = Battle(self.game, 601, self.fleet)

        spot, enemy = battle.go()
        Log.i('Enemy fleet: ' + str(enemy))

        if (enemy == [ 1, 1, 14, 14, 14 ]) or (enemy == [ ]):
            Log.i('CV detected, retreat')
            self.game.restart()
            return True

        battle.start(5)
        newShip, hp = battle.chase()
        battle.quit()

        Log.i('Battle result:')
        for ship in self.fleet.ships:
            Log.i('    %s Lv:%d HP:%d/%d' % (ship.getName(), ship.lv, ship.hp, ship.maxHp))

        if newShip is None:
            Log.i('No ship got')
        elif newShip.getName() in self.dismantleList or self.game.isDormFull():
            Log.i('Dismantle ' + newShip.getName())
            newShip.dismantle()
        else:
            Log.i('Got ship ' + newShip.getName())

        self.fleet.fill()
        return True

    def end(self):
        self.fleet.changeShips(self.formerShips)
        self.formerShips = None
        self.isLooping = False

        for ship in self.ships:
            if ship.isInjured() and ship.status != Ship.Repairing:
                Log.i('Try to repair ship %s' % ship.getName())
                for repairYard in self.game.repairYards:
                    if repairYard.ship is None:
                        Log.i('Success')
                        repairYard.repair(ship)
                        break
            elif not ship.isInjured():
                Log.i('Ship %s is not injured' % ship.getName())
            elif ship.status == Ship.Repairing:
                Log.i('Ship %s is already being repaired' % ship.getName())
            else:
                Log.w('error')

    def tryRepair(self): # TODO
        return False
