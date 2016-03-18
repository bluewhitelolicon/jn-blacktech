from battle import Battle
from log import Log

class Auto25:
    OK = 0
    Pit = -1
    Broke = -2
    Error = -3
    Success = -4

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
            return Auto25.Error

        self.battle = Battle(self.game, 205, self.fleet)
        spot, enemy = self.battle.go()
        Log.i('Spot: ' + str(spot))
        Log.i('Enemy fleet: ' + str(enemy))
        # if spot != 991602:
        #     return AutoE3.Pit

        self.newShips = [ None, None, None ,None,None]

        for i in range(5):
            if i != 0:
                spot, enemy = self.battle.go()
                Log.i('Spot: ' + str(spot))
                Log.i('Enemy fleet: ' + str(enemy))
                if i == 2:
                    if spot != 20504:
                        return Auto25.Pit
            self.battle.start(2)
            self.newShips[i], hp = self.battle.giveUp()
            Log.i('Got %s at spot %d' % (self.newShips[i].getName() if self.newShips[i] is not None else 'nothing', i))
            Log.i(self.fleet.printHp())
            for ship in self.fleet.ships:
                if ship.isBadlyBroken():
                    self.end()
                    return Auto25.Broke
        self.end()
        return Auto25.OK

    def end(self):
        self.battle.quit()
        self.fleet.fill()

        for ship in self.newShips:
            if ship is not None:
                if ship.getName() in self.dismantleList:
                    Log.i('Dismantle ' + ship.getName())
                    ship.dismantle()
                else:
                    Log.i('Keep ship ' + ship.getName())
