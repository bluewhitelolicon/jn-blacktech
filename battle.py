from log import Log

import time

class Battle:
    def __init__(self, game, stageId, fleet):
        if not fleet.isReady():
            Log.w('Fleet ' + str(fleet.id) + ' is not ready for battle')
            self.spot = -1
        else:
            game.startStage(stageId, fleet)
            self.game = game
            self.fleet = fleet
            self.spot = 0
            self.canChase = None

    def go(self, moveTime = 5, searchTime = 5):
        if self.spot == -1:
            Log.w('Battle: something wrong')
            return None
        self.spot = self.game.nextSpot()
        time.sleep(moveTime)
        ret = self.game.searchEnemy(self.spot)
        time.sleep(searchTime)
        return ret

    def engage(self, formation, waitTime = 30):
        selfHp, enemyHp, lastSpot = self.game.engage(self.spot, self.fleet, formation)

        canChase = False
        for hp in enemyHp:
            if hp != 0:
                canChase = True

        if lastSpot:
            self.spot = -1

        time.sleep(waitTime)
        return selfHp, enemyHp

    def chase(self, waitTime = 20):
        if self.canChase:
            return self.getResult(True, waitTime)
        else:
            return self.getResult(False)

    def giveUp(self):
        return self.getResult(False)

    def getResult(self, doNightBattle, waitTime = 0):
        newShip, ships = self.game.getBattleResult(doNightBattle)
        self.game.addShip(newShip)
        for i in range(len(self.fleet.ships)):
            fleet.ships[i].setProps(ships[i])
        time.sleep(waitTime)
        return newShip, fleet.getShipHp()

    def quit(self):
        self.game.quitStage()
