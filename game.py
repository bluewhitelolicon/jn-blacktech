from connection import Connection
from packer import Packer
from log import Log

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

    def getFleet(self, id_):
        return self.fleets[id_ - 1]

    def addResource(self, res):
        pass # TODO

    def startExpedition(self, exp, fleet):
        data = self.conn.post('/explore/start/' + str(fleet.id) + '/' + str(exp.id) + '/', 'pve_level=1')
        return datetime.fromtimestamp(int(data['pveExploreVo']['levels'][0]['endTime']))

    def getExpeditionResult(self, exp):
        data = self.conn.get('/explore/getResult/' + str(exp.id))
        return (int(data['bigSuccess']) == 1), self.packer.makeResource(data['newAward'])
