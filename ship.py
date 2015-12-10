class Ship:
    # status
    Idle = 0
    Repairing = 1
    RunningExpedition = 2

    def __init__(self, game, id_, shipClass, lv, hp, maxHp, fuel, ammo):
        self.game = game
        self.id = id_
        self.shipClass = shipClass
        self.lv = lv
        self.hp = hp
        self.maxHp = hp
        self.fuel = fuel
        self.ammo = ammo
        self.status = Ship.Idle

    def getShipType(self):
        return self.shipClass.shipType

    def isBadlyBroken(self):
        return self.hp * 4 < self.maxHp

    def isFilled(self):
        return self.fuel == self.shipClass.fuel and self.ammo == self.shipClass.ammo
