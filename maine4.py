from game import Game
from log import Log
from autoe4 import AutoE4

from datetime import datetime
import json, time

account = json.load(open('account.json'))
game = Game(account)

e4Fleet = [ '萤火虫', '苏赫巴托尔', '加贺', '列克星敦', '萨拉托加', '突击者' ]
e4Dismantle = [
    '奥马哈', '翡翠', '进取', '撒切尔',
    '扶桑', '山城', '内华达', '俄克拉荷马', '反击',
    '摩耶', '鸟海', '昆西', '古鹰', '加古', '青叶', '衣笠', '休斯顿',
#    '亚特兰大', '朱诺', '圣胡安',
#    '响', '电',
    '普林斯顿',
    '列克星敦', '罗德尼', '马里兰', '西弗吉尼亚', '索玛雷兹',
    '胡德', '威尔士亲王'
]
autoE4 = AutoE4(game, e4Fleet, e4Dismantle)

while True:
    time.sleep(10)

    for fleet in game.fleets[0:3]:
        exp = fleet.expedition
        if exp is not None and datetime.now() > exp.endTime:
            exp.getResult()
            exp.start(fleet)
            Log.i('Restarted expedition %d' % exp.id)

    fleet = game.fleets[3]
    for ship in fleet.ships:
        if ship.isBroken():
            ship.instantRepair()
    if autoE4.getReady(fleet):
        time.sleep(10)
        if autoE4.run() == AutoE4.Pit:
            game.restart()
    else:
        Log.e('Cannot get fleet ready')
