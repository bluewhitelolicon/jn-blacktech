from connection import Connection
from packer import Packer
from log import Log

import time
from datetime import datetime

class Game:
    def __init__(self, account):
        self.username = account['username']
        self.password = account['password']
        self.server = account['server']

        self.shipClasses = { }
        self.ships = { }
        self.fleets = [ None, None, None, None ]
        self.expeditions = { }
        self.repairYards = [ None, None, None, None ]
        self.maxShipNum = 0
        self.errorCodes = { }

        self.packer = Packer(self)

        Log.i('Initializing game...')
        self.conn = Connection()
        self.gameData = self.conn.get('/index/getInitConfigs/')

        for shipClassData in self.gameData['shipCard']:
            if int(shipClassData['npc']) == 0 and int(shipClassData['release']) == 1:
                shipClass = self.packer.makeShipClass(shipClassData)
                self.shipClasses[shipClass.id] = shipClass

        for expeditionData in self.gameData['pveExplore']:
            expedition = self.packer.makeExpedition(expeditionData)
            self.expeditions[expedition.id] = expedition

        Log.errorCodes = { int(k) : v for k, v in self.gameData['errorCode'].items() }

        Log.i('Logging in...')
        loginData = self.conn.httpsGet('/index/passportLogin/%s/%s/' % (self.username, self.password))
        self.conn.setServer(self.server)
        time.sleep(1)
        self.conn.get('//index/login/' + loginData['userId'])

        Log.i('Initializing user data...')
        self.userData = self.conn.get('/api/initGame/')
        self.conn.get('/pevent/getPveData/')
        self.conn.get('/pve/getPveData/')
        time.sleep(5)
        self.conn.get('/active/getUserData/')
        self.conn.get('/campaign/getUserData/')
        self.conn.get('/pve/getUserData/')

        for shipData in self.userData['userShipVO']:
            ship = self.packer.makeShip(shipData)
            self.ships[ship.id] = ship

        for fleetData in self.userData['fleetVo']:
            fleet = self.packer.makeFleet(fleetData)
            self.fleets[fleet.id - 1] = fleet

        for expStatusData in self.userData['pveExploreVo']['levels']:
            exp = self.expeditions[int(expStatusData['exploreId'])]
            fleet = self.fleets[int(expStatusData['fleetId']) - 1]
            endTime = datetime.fromtimestamp(int(expStatusData['endTime']))
            exp.setStatus(fleet, endTime)

        for repairYardData in self.userData['repairDockVo']:
            ry = self.packer.makeRepairYard(repairYardData)
            self.repairYards[ry.id - 1] = ry

        self.maxShipNum = int(self.userData['userVo']['detailInfo']['shipNumTop'])

        Log.i('Done')

    def restart(self):
        self.conn = Connection()
        self.conn.get('/index/getInitConfigs/')
        loginData = self.conn.get('/index/passportLogin/%s/%s/' % (self.username, self.password))
        self.conn.setServer(self.server)
        self.conn.get('//index/login/' + loginData['userId'])
        self.conn.get('/api/initGame/')
        Log.i('Game restarted')

    def getShipClass(self, id_):
        return self.shipClasses[id_]

    def getShip(self, id_):
        return self.ships[id_]

    def findShip(self, name, lv = None):
        ret = None
        for ship in self.ships.values():
            if ship.getName() == name:
                if lv is not None and ship.lv == lv:
                    Log.i('Found ship %s of level %d, id: %d' % (name, ship.lv, ship.id))
                    return ship
                if ret is None or ret.lv < ship.lv:
                    ret = ship
        return ret

    def getFleet(self, id_):
        return self.fleets[id_ - 1]

    def isDormFull(self):
        return len(self.ships) >= self.maxShipNum

    def addShip(self, ship):
        self.ships[ship.id] = ship

    def addResource(self, res):
        pass # TODO

    def removeShip(self, ship):
        del self.ships[ship.id]

    # Ship

    def repair(self, ship, repairYard):
        data = self.conn.get('/boat/repair/%d/%d/' % (ship.id, repairYard.id))
        for ryData in data['repairDockVo']:
            if int(ryData['id']) == repairYard.id:
                return datetime.fromtimestamp(int(ryData['endTime']))

    def repairComplete(self, repairYard):
        self.conn.get('/boat/repairComplete/%d/%d/' % (repairYard.id, repairYard.ship.id))

    def instantRepair(self, ship):
        self.conn.get('/boat/instantRepairShips/[%d]/' % ship.id)

    def dismantleShip(self, ship, keepEquipt = True):
        self.conn.get('/dock/dismantleBoat/[%d]/%d/' % (ship.id, (0 if keepEquipt else 1)))

    # Fleet

    def changeShips(self, fleet, ships):
        ships = [ ship.id for ship in ships ]
        ships = str(ships).replace(' ', '')
        self.conn.get('/boat/instantFleet/%d/%s/' % (fleet.id, ships))

    def changeShip(self, fleet, pos, ship):
        self.conn.get('/boat/changeBoat/%d/%d/%d/' % (fleet.id, ship.id, pos))

    def fill(self, fleet):
        ships = [ ship.id for ship in fleet.ships ]
        ships = str(ships).replace(' ', '')
        self.conn.get('/boat/supplyBoats/%s/' % ships)

    # Expedition

    def startExpedition(self, exp, fleet):
        data = self.conn.post('/explore/start/%d/%d/' % (fleet.id, exp.id), 'pve_level=1')
        for expData in data['pveExploreVo']['levels']:
            if int(expData['exploreId']) == exp.id:
                return datetime.fromtimestamp(int(expData['endTime']))
        Log.e('startExpedition: unexpected response')

    def getExpeditionResult(self, exp):
        data = self.conn.get('/explore/getResult/%d/' % exp.id)
        return (int(data['bigSuccess']) == 1), self.packer.makeResource(data['newAward'])

    # Battle

    def startStage(self, stageId, fleet):
        self.conn.post('/pve/challenge/%d/%d/0/' % (stageId, fleet.id), 'pve_level=1')

    def quitStage(self):
        # faking official client
        self.conn.get('/active/getUserData/')
        self.conn.get('/pve/getUserData/')
        self.conn.get('/campaign/getUserData/')

    def nextSpot(self):
        data = self.conn.get('/pve/next/')
        return int(data['node'])

    def searchEnemy(self, spot):
        data = self.conn.get('/pve/spy/')
        if int(data['enemyVO']['isFound']) == 0:
            return [ ]
        return [ int(ship['type']) for ship in data['enemyVO']['enemyShips'] ]

    def startBattle(self, spot, fleet, formation):
        data = self.conn.get('/pve/deal/%d/%d/%d/' % (spot, fleet.id, formation))
        selfHp = data['warReport']['hpBeforeNightWarSelf']
        enemyHp = data['warReport']['hpBeforeNightWarEnemy']
        lastSpot = (int(data['pveLevelEnd']) == 1)
        return selfHp, enemyHp, lastSpot

    def getBattleResult(self, doNightBattle):
        data = self.conn.get('/pve/getWarResult/%d/' % (1 if doNightBattle else 0))

        newShip = None
        if 'newShipVO' in data:
            newShip = self.packer.makeShip(data['newShipVO'][0])

        ships = None
        if type(data['shipVO']) is list:
            ships = [ self.packer.makeShip(shipData) for shipData in data['shipVO'] ]
        else:
            ships = [ self.packer.makeShip(data['shipVO']) ]

        return newShip, ships
