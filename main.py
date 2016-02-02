from game import Game
from log import Log

from datetime import datetime
import json, time

account = json.load(open('account.json'))
game = Game(account)

while True:
    time.sleep(10)

    for fleet in game.fleets:
        exp = fleet.expedition
        if exp is not None and datetime.now() > exp.endTime:
            exp.getResult()
            exp.start(fleet)
            Log.i('Restarted expedition %d' % exp.id)
