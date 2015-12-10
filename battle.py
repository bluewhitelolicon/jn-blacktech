from log import Log

class Battle:
    def __init__(self, game, stageId, fleet):
        if not fleet.isReady():
            Log.w('Fleet ' + str(fleet.id) + ' is not ready for battle')
            raise Exception('Fleet is not ready')
        game.startStage(stageId, fleet)
        self.game = game
        self.fleet = fleet
        self.spot = 0

    def go(self, moveTime = 5, searchTime = 5):
        if self.spot == -1:
            raise Exception('Stage finished')
        self.spot = self.game.nextSpot()
        time.sleep(moveTime)
        ret = self.game.searchEnemy(self.spot)
        time.sleep(searchTime)
        return ret

    def engage(self, formation, time = 30):
        selfHp, enemyHp, lastSpot = self.game.engage(self.spot, self.fleet, formation)
        if lastSpot:
            self.spot = -1
        time.sleep(time)
        return selfHp, enemyHp

    def chase(self, time = 20):
        return self.getResult(True, time)

    def giveUp(self):
        return self.getResult(False)

    def getResult(self, doNightBattle, time = 0):
        newShip, ships = self.game.getBattleResult(doNightBattle)
        for i in range(len(fleet.ship)):
            fleet.ships[i].setProps(ships[i])
        time.sleep(time)
        return newShip, fleet.getShipHp()

    def quit(self):
        self.game.quitStage()
