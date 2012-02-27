#!/usr/bin/python
"""
CS Games 2011
AI Competition

Chris Iverach-Brereton

This file contains the Human class

Competitors may edit this file by adding additional functions & properties necessary for
their AI.  However, any additional functions must not illegally edit the state of the game;
competitors are NOT allowed to edit HP, accuracy, bullet count, etc...

Illegally changing the state of the game world will result in disqualification
"""

from entity import *
import gameBoard
import random

class Human(Entity):
    
    # how many bullets does this survivor have?
    _bullets = 30
    
    # how accurate is shooting?
    _rangedAccuracy = 0.30
    
    def __init__(self, configStr):
        self._team = 0
        Entity.__init__(self, configStr)
        self._meleeAccuracy = 0.20
        self._hp = 2
        
    
    def initLoadParameters(self, configStr):
        """
        Initialize this survivor from the output of __str__
        """
        
        # let the superclass handle everything it knows about
        Entity.initFromString(self,configStr)
        
        # deal with Survivor-specific attributes
        attrs = configStr[configStr.index('[')+1:configStr.index(']')]
        attrTokens = attrs.split(',')
        
        for t in attrTokens:
            tokens = t.split(':')
            name = tokens[0].lower().strip()
            value = tokens[1].lower().strip()
            
            if name == 'ammo':
                self._bullets = int(value)
            
            elif name == 'ranged':
                self._rangedAccuracy = float(value)
    
    def __str__(self):
        return "Entity {0} [hp:{1},ammo:{2},team:{3},melee:{4},ranged:{5}]".format(self.getId(), self.getHP(), self._bullets,self._team,self._meleeAccuracy,self._rangedAccuracy)
    
    def shoot(self, targetSquare):
        """
        Fire a bullet at the entity in the target square
        Note: firing at a square with a friendly entity is allowed;
        make sure you check for friendly fire before calling shoot()!
        Note: you may commit suicide by shooting your own square
        
        returns True if the shot was fired
        returns False if the shot was either blocked or we're out of bullets or there's no target in the square
        
        The client simply prints the action
        The server actually "rolls" and applies damage
        """
        
        #print '[debug] Entity',self._id,'attempting to shoot square',targetSquare._id
        
        # check the dummy cases and return False if any of them are true
        if not gameBoard.GameBoard._instance._checkLOS(self.getSquare(), targetSquare):
            print '[debug] Entity',self._id,'cannot shoot; blocked LOS'
            return False
        elif self._bullets <= 0:
            print '[debug] Entity',self._id,'cannot shoot; no ammo'
            return False
        elif targetSquare.isEmpty():
            print '[debug] Entity',self._id,'cannot shoot; empty target square'
            return False
        elif not self.canMakeAction():
            return False
        elif self._bullets <= 0:
            print '[cheat] Entity',self._id,'cannot shoot; no ammo'
            return False
            
        
        # do the actual attack
        target = targetSquare.getOccupant()
        self._bullets = self._bullets - 1
        if random.randint(0,100) < self._rangedAccuracy * 100:
            target._hp = target._hp - 1
            
            if target._hp <= 0:
                print '* Entity',self._id,'killed entity',target._id,'(ranged)'
                targetSquare.clearOccupant()
            else:
                print '* Entity',self._id,'hit entity',target._id,'(ranged)'
        else:
            print '* Entity',self._id,'missed entity',target._id,'(ranged)'
        
        return True

    def search(self,targetSquare):
        if targetSquare.isSearched():
            print '[cheat] Entity',self._id,'cannot search; square is already looted'
            return False
        elif not self.canMakeAction():
            return False
            
        targetSquare._isSearched = True
        
        # find out what we found:
        rnd = random.randint(0,100)
        
        if rnd < 20:
            numBullets = random.randint(5,10)
            print '* Entity',self._id,'found',numBullets,'bullets'
            self._bullets = self._bullets + numBullets
        elif rnd < 40:
            print '* Entity',self._id,'found a',self.randomFood(),'(+1 HP)'
            self._hp = self._hp + 1
        elif rnd < 50:
            print '* Entity',self._id,'found medical supplies','(+2 HP)'
            self._hp = self._hp + 2
        elif rnd < 55:
            print '* Entity',self._id,'found a',self.randomArmour(),'(+5 HP)'
            self._hp = self._hp + 5
        elif rnd < 60:
            increase = random.randint(1,10) * 0.01
            print '* Entity',self._id,'found a',self.randomRangedWeapon(),'(+{0}% chance to do ranged damage)'.format(increase*100)
            self._rangedAccuracy = self._rangedAccuracy + increase
        elif rnd < 65:
            increase = random.randint(1,10) * 0.01
            print '* Entity',self._id,'found a',self.randomMeleeWeapon(),'(+{0}% chance to do melee damage)'.format(increase*100)
            self._meleeAccuracy = self._meleeAccuracy + increase
        else:
            print '* Entity',self._id,'did not find anything of value'
            
        return True
            
    def randomFood(self):
        items = [
            'chicken mcnugget',
            'hamburger',
            'jersey milk bar',
            'tube of pringles',
            'pizza pop',
            'head of lettuce',
            'granola bar',
            'poutine',
            'turkey leg',
            'hot dog',
            'twinkie',
            'raisin muffin',
            'jar of maple syrop'
        ]
        
        return random.choice(items)
    
    def randomMeleeWeapon(self):
        items = [
            'machete',
            'chainsaw',
            'kukri',
            'bowie knife',
            'broadsword',
            'katana',
            'set of brass knuckles',
            'signpost',
            'bullwhip',
            'bayonette',
            'nail file',
            'hammer',
            'sledgehammer',
            'poleaxe',
            'fire axe',
            'diamond pickaxe'
        ]
        
        return random.choice(items)

    def randomRangedWeapon(self):
        items = [
            'assault rifle',
            'shotgun',
            'pistol',
            'throwing knife',
            'shuriken',
            'laser sight',
            'telescopic sight',
            'sniper rifle',
            'bazooka',
            'grenade',
            'crossbow',
            'plasma rifle',
            'bfg 9000'
        ]
        
        return random.choice(items)
        
    def randomArmour(self):
        items = [
            'bicycle helmet',
            'set of greaves',
            'pair of leather boots',
            'pair of motorcycle gloves',
            'paintball mask',
            'set of hockey pads',
            'pair of fuzzy socks',
            'bandana',
            'golden bracer',
            'diamond chestpiece',
            'gas mask'
        ]
        
        return random.choice(items)
