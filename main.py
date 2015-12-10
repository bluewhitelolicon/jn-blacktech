from game import Game
from log import Log

from datetime import datetime
import json, time

account = json.load(open('account.json'))
game = Game(account)

while True:
    for fleet in game.fleets:
        exp = fleet.expedition
        if exp is not None and datetime.now() > exp.endTime:
            Log.i('Restarting expedition ' + str(exp.id) + '...')
            exp.getResult()
            exp.start(fleet)

    time.sleep(10)
