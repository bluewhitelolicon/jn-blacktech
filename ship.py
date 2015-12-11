class Ship:
    # status
    Idle = 0
    Repairing = 1

    def __init__(self, game, id_, shipClass, lv, hp, maxHp, fuel, ammo):
        self.game = game
        self.id = id_
        self.shipClass = shipClass
        self.lv = lv
        self.hp = hp
        self.maxHp = maxHp
        self.fuel = fuel
        self.ammo = ammo
        self.status = Ship.Idle
        self.fleet = None

    def setProps(self, ship):
        self.lv = ship.lv
        self.hp = ship.hp
        self.maxHp = ship.maxHp
        self.fuel = ship.fuel
        self.ammo = ship.ammo

    def getShipType(self):
        return self.shipClass.shipType

    def isIdle(self):
        return self.status == Ship.Idle and self.fleet.expedition is None

    def isInjured(self):
        return self.hp < self.maxHp

    def isBadlyBroken(self):
        return self.hp * 4 < self.maxHp

    def isFilled(self):
        return self.fuel == self.shipClass.fuel and self.ammo == self.shipClass.ammo

    def setRepaired(self):
        self.hp = self.maxHp

    def setFilled(self):
        self.fuel = self.shipClass.fuel
        self.ammo = self.shipClass.ammo

    def dismantle(self):
        self.game.dismantleShip(self)
        self.game.removeShip(self)
