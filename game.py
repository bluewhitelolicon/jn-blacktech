from connection import Connection
from packer import Packer
from log import Log

from datetime import datetime

class Game:
    def __init__(self, account):
        self.shipClasses = { }
        self.ships = { }
        self.fleets = [ None, None, None, None ]
        self.expeditions = { }

        self.packer = Packer(self)

        Log.i('Initializing game...')
        self.conn = Connection('2.1.0')
        gameData = self.conn.get('/index/getInitConfigs/')

        for shipClassData in gameData['shipCard']:
            if int(shipClassData['npc']) == 0 and int(shipClassData['release']) == 1:
                shipClass = self.packer.makeShipClass(shipClassData)
                self.shipClasses[shipClass.id] = shipClass

        for expeditionData in gameData['pveExplore']:
            expedition = self.packer.makeExpedition(expeditionData)
            self.expeditions[expedition.id] = expedition

        Log.i('Logging in...')
        loginData = self.conn.get('/index/passportLogin/' + account['username'] + '/' + account['password'] + '/')
        self.conn.setServer(account['server'])
        self.conn.get('//index/login/' + loginData['userId'])

        Log.i('Initializing user data...')
        userData = self.conn.get('/api/initGame/')

        for shipData in userData['userShipVO']:
            ship = self.packer.makeShip(shipData)
            self.ships[ship.id] = ship

        for fleetData in userData['fleetVo']:
            fleet = self.packer.makeFleet(fleetData)
            self.fleets[fleet.id - 1] = fleet

        for expStatusData in userData['pveExploreVo']['levels']:
            exp = self.expeditions[int(expStatusData['exploreId'])]
            fleet = self.fleets[int(expStatusData['fleetId']) - 1]
            endTime = datetime.fromtimestamp(int(expStatusData['endTime']))
            exp.setStatus(fleet, endTime)

        Log.i('Done')

    def getShipClass(self, id_):
        return self.shipClasses[id_]

    def getShip(self, id_):
        return self.ships[id_]

    def getFleet(self, id_):
        return self.fleets[id_ - 1]

    def addResource(self, res):
        pass # TODO

    # Expedition

    def startExpedition(self, exp, fleet):
        data = self.conn.post('/explore/start/' + str(fleet.id) + '/' + str(exp.id) + '/', 'pve_level=1')
        for expData in data['pveExploreVo']['levels']:
            if int(expData['exploreId']) == exp.id:
                return datetime.fromtimestamp(int(expData['endTime']))
        Log.e('startExpedition: unexpected response')

    def getExpeditionResult(self, exp):
        data = self.conn.get('/explore/getResult/' + str(exp.id))
        return (int(data['bigSuccess']) == 1), self.packer.makeResource(data['newAward'])

    # Battle

    def startStage(self, stageId, fleet):
        self.conn.get('/pve/challenge129/' + str(stageId) + '/' + str(fleet.id) + '/0')

    def quitStage(self):
        self.conn.get('/pve/pveEnd/')
        self.conn.get('/active/getUserData')  # faking official client

    def nextSpot(self):
        data = self.conn.get('/pve/next/')
        return int(data['node'])

    def searchEnemy(self, spot):
        data = self.conn.get('/pve/spy/' + str(spot))
        # FIXME: return what?

    def engage(self, spot, fleet, formation):
        data = self.conn.get('/pve/deal/' + str(spot) + '/' + str(fleet.id) + '/' + str(formation))
        selfHp = data['hpBeforeNightWarSelf']
        enemyHp = data['hpBeforeNightWarEnemy']
        lastSpot = (int(data['pveLevelEnd']) == 1)

    def getBattleResult(self, doNightBattle):
        url = '/pve/getWarResult/'
        if doNightBattle:
            url += '1'
        else:
            url += '0'
        data = self.conn.get(url)

        newShip = None
        if 'newShipVO' in data:
            newShip = self.packer.makeShip(data['newShipVO'][0])

        ships = None
        if type(data['shipVO']) is list:
            ships = [ self.packer.makeShip(shipData) for shipData in data['shipVO'] ]
        else:
            ships = [ self.packer.makeShip(data['shipVO']) ]

        return newShip, ships
