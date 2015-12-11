from shipclass import ShipClass
from ship import Ship
from fleet import Fleet
from expedition import Expedition, FleetRequirement
from repairyard import RepairYard
from resource import Resource

from datetime import datetime

class Packer:
    def __init__(self, game):
        self.game = game

    def makeShipClass(self, data):
        id_ = int(data['cid'])
        name = str(data['title'])
        fuel = int(data['maxOil'])
        ammo = int(data['maxAmmo'])
        shipType = int(data['type'])
        return ShipClass(id_, name, fuel, ammo, shipType)

    def makeShip(self, data):
        id_ = int(data['id'])
        shipClass = self.game.getShipClass(int(data['shipCid']))
        lv = int(data['level'])
        hp = int(data['battleProps']['hp'])
        maxHp = int(data['battlePropsMax']['hp'])
        fuel = int(data['battleProps']['oil'])
        ammo = int(data['battleProps']['ammo'])
        return Ship(self.game, id_, shipClass, lv, hp, maxHp, fuel, ammo)

    def makeFleet(self, data):
        id_ = int(data['id'])
        ships = [ self.game.getShip(int(x)) for x in data['ships'] ]
        return Fleet(self.game, id_, ships)

    def makeExpedition(self, data):
        shipNum = int(data['needShipNum'])
        flagShipLv = int(data['needFlagShipLevel'])
        numOfType = { int(pair['type']) : int(pair['num']) for pair in data['needShipType'] }
        fr = FleetRequirement(shipNum, flagShipLv, numOfType)

        id_ = int(data['id'])
        time = int(data['needTime'])
        basicAward = self.makeResource(data['award'])
        extraAward = self.makeResource(data['pruductGoods'])
        return Expedition(self.game, id_, time, fr, basicAward, extraAward)

    def makeRepairYard(self, data):
        id_ = int(data['id'])
        if 'shipId' in data:
            ship = self.game.getShip(int(data['shipId']))
            endTime = datetime.fromtimestamp(int(data['endTime']))
            return RepairYard(self.game, id_, ship, endTime)
        else:
            return RepairYard(self.game, id_)

    def makeResource(self, data):
        fuel = 0
        ammo = 0
        steel = 0
        alum = 0
        shipBlueprint = 0
        equiptBlueprint = 0
        fastRepair = 0
        fastBuild = 0
        if '2' in data: fuel = data['2']
        if '3' in data: ammo = data['3']
        if '4' in data: steel = data['4']
        if '9' in data: alum = data['9']
        return Resource(fuel, ammo, steel, alum, shipBlueprint, equiptBlueprint, fastRepair, fastBuild) 
