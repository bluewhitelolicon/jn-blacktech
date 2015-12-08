from datetime import datetime
import os

class Log:
    verboseLevel = 'd'

    logFile = open('log.txt', 'a')

    def v(msg):
        if Log.verboseLevel is 'v':
            Log.showMsg('VERBOSE', msg)

    def d(msg):
        Log.showMsg('DEBUG', msg, Log.verboseLevel in 'vd')

    def i(msg):
        Log.showMsg('INFO', msg, Log.verboseLevel in 'vdi')

    def w(msg):
        Log.showMsg('WARNING', msg)

    def e(msg, halt = True):
        Log.showMsg('ERROR', msg)
        if halt:
            Log.logFile.close()
            os._exit(0)

    def showMsg(label, msg, printToScreen = True):
        time = str(datetime.now()).split('.')[0]
        msg = '[' + label + '] ' + time + ' ' + msg
        if printToScreen:
            if len(msg) < 1000:
                print(msg)
            else:
                print(msg[:1000] + '...')
        Log.logFile.write(msg + '\n')
        Log.logFile.flush()
