from game import Game
from ship import Ship
from auto61 import Auto61
from log import Log

from datetime import datetime
import json, time

account = json.load(open('account.json'))
game = Game(account)

shipNames61 = [ '威奇塔', '黑背豺', '旁遮普人', '沙利文', '巨像', '百眼巨人' ]
shipLv61 = [ None, None, None, None, None, None ]
mustRepair = [ False, False, False, False, True, True ]
needInstRepair = [ False ] * 6
#dismantleList = [ '博格', '普林斯顿' ] #, '亚特兰大', '朱诺', '圣胡安' ]
#dismantleList = [ '反击', '希佩尔', '布吕歇尔', '博格', '普林斯顿', '彭萨科拉', '新奥尔良', '胡德', '欧根亲王', '亚特兰大', '朱诺', '圣胡安', '布鲁克林' ]
#dismantleList = [ '反击', '希佩尔', '布吕歇尔', '博格', '普林斯顿', '彭萨科拉', '新奥尔良', '胡德', '欧根亲王', '亚特兰大', '朱诺', '圣胡安', '布鲁克林', 'Z16', '卡辛杨', '安东尼', '布雷恩', '沃克兰', '弗兰克·诺克斯', '鲍尔' ]
dismantleList = [ '反击', '希佩尔', '布吕歇尔', '博格', '普林斯顿', '彭萨科拉', '新奥尔良', '胡德', '欧根亲王', '亚特兰大', '朱诺', '圣胡安', '布鲁克林', 'Z21', 'Z22', 'Z16', '卡辛杨', '安东尼', '布雷恩', '沃克兰', '弗兰克·诺克斯', '鲍尔' ]

ships61 = [ None, None, None, None, None, None ]
for i in range(6):
    if type(shipNames61[i]) is int:
        ships61[i] = game.getShip(shipNames61[i])
    else:
        ships61[i] = game.findShip(shipNames61[i], shipLv61[i])
#ships61 = [ game.findShip(name) for name in shipNames61 ]
auto61 = Auto61(game, game.fleets[-1], ships61, mustRepair, needInstRepair, dismantleList)

for fleet in game.fleets:
    if fleet.expedition is not None:
        exp = fleet.expedition
        Log.i("Expedition %d (fleet %d) will return at %s" % (exp.id, fleet.id, exp.endTime))

for repairYard in game.repairYards:
    if repairYard.ship is not None:
        Log.i('Repairing %s, will finish at %s' % (repairYard.ship.getName(), repairYard.endTime))

if game.fleets[-1].expedition is None:
    if not auto61.tryGetReady():
        Log.e('Cannot get 6-1 ready')

while True:
    for fleet in game.fleets[:-1]:
        exp = fleet.expedition
        if datetime.now() > exp.endTime:
            exp.getResult()
            time.sleep(2)
            exp.start(fleet)
            Log.i('Restarted expedition %d' % exp.id)

    for repairYard in game.repairYards:
        if (repairYard.ship is not None) and (datetime.now() > repairYard.endTime):
            repairYard.complete()
            for ship in game.ships.values():
                if ship.isInjured() and ship.status != Ship.Repairing:
                    Log.i('Ship %s is injured' % ship.getName())
                    Log.i('auto61.isLooping = ' + str(auto61.isLooping))
                    Log.i(str((ship not in ships61) or (not auto61.isLooping)))
                    if (ship not in ships61) or (not auto61.isLooping):
                        Log.i('Try to repair ' + ship.getName())
                        repairYard.repair(ship)
                        break

    fleet = game.fleets[-1]
    if auto61.isLooping:
        auto61.run()
        if (not auto61.canRun()) and (not auto61.tryRepair()):
            auto61.end()
            time.sleep(5)
            game.expeditions[10003].start(fleet)
            Log.i('6-1 end')
    else:
        exp = fleet.expedition
        if datetime.now() > exp.endTime:
            exp.getResult()
            if auto61.tryGetReady():
                Log.i('6-1 start')
            else:
                exp.start(fleet)
                Log.i('Restarted expedition %d' % exp.id)

    time.sleep(10)
