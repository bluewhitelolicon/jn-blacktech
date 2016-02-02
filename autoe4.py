from battle import Battle
from log import Log

class AutoE4:
    OK = 0
    Pit = -1
    Broke = -2
    Error = -3

    def __init__(self, game, shipNames, dismantleList = [ ]):
        self.game = game
        self.ships = [ game.findShip(name) for name in shipNames ]
        self.dismantleList = dismantleList
        self.fleet = None
        self.formerShips = None

    def isReady(self):
        return (self.fleet is not None) and (self.fleet.isReady())

    def getReady(self, fleet):
        if self.fleet is not None and self.fleet != fleet:
            Log.i('Already has fleet')
            return False
        for i in range(len(self.ships)):
            if not self.ships[i].isIdle():
                Log.i('%s is not idle' % self.ships[i].getName())
                return False
            if self.ships[i].isBroken():
                Log.i('%s is broken' % self.ships[i].getName())
                return False

        self.fleet = fleet
        self.formerShips = fleet.ships.copy()
        for i in range(6):
            if self.ships[i] != self.fleet.ships[i]:
                fleet.changeShips(self.ships)
                fleet.fill()
                return True
        fleet.fill()
        return True

    def end(self):
        ret = self.fleet
        self.fleet.changeShips(self.formerShips)
        self.fleet = None
        self.formerShips = None
        return ret

    def run(self):
        if not self.fleet.isReady():
            return AutoE4.Error

        self.battle = Battle(self.game, 9916, self.fleet)
        spot, enemy = self.battle.go()
        Log.i('Spot: ' + str(spot))
        Log.i('Enemy fleet: ' + str(enemy))
        if spot != 991602:
            return AutoE4.Pit

        self.newShips = [ None, None, None ]

        for i in range(3):
            if i != 0:
                self.battle.go()
            self.battle.engage(2)
            self.newShips[i], hp = self.battle.giveUp()
            Log.i('Got %s at spot %d' % (self.newShips[i].getName() if self.newShips[i] is not None else 'nothing', i))
            Log.i(self.fleet.printHp())
            for ship in self.fleet.ships:
                if ship.isBroken():
                    self.end()
                    return AutoE4.Broke

        self.end()
        return AutoE4.OK

    def end(self):
        self.battle.quit()
        self.fleet.fill()

        for ship in self.newShips:
            if ship is not None:
                if ship.getName() in self.dismantleList:
                    Log.i('Dismantle ' + ship.getName())
                    keepEquipt = (ship.getName() in [ '翡翠', '列克星敦' ])
                    ship.dismantle(keepEquipt)
                else:
                    Log.i('Keep ship ' + ship.getName())
                    if '威廉' in ship.getName():
                        Log.e('Done')
