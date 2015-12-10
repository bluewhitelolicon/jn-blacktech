from game import Game
from log import Log

from datetime import datetime
from threading import Lock, Timer
import json

commonDelay = 10
lock = Lock()

account = json.load(open('account.json'))
game = Game(account)

def doActions():
    lock.acquire()
    Log.i('Doing actions...')

    for fleet in game.fleets:
        exp = fleet.expedition
        if exp is not None:
            if datetime.now() > exp.endTime:
                Log.i('Restarting expedition ' + str(exp.id) + '...')
                exp.getResult()
                exp.start(fleet)
            doActionsAt(exp.endTime)

    Log.i('Done')
    lock.release()

def doActionsAt(time):
    Log.i('Will do actions at ' + str(time.time()).split('.')[0])
    if time < datetime.now():
        doActions()
    else:
        delay = (time - datetime.now()).total_seconds() + commonDelay
        Timer(delay, doActions).start()

doActions()
