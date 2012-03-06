#!/usr/bin/python
"""
CS Games 2012
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
    _rangedAccuracy = 0.50

    def __init__(self, configStr):
        self._team = Entity.HUMAN_TEAM
        Entity.__init__(self, configStr)


    def loadParameters(self, configStr):
        """
        Initialize this survivor from the output of __str__
        """

        # let the superclass handle everything it knows about
        Entity.loadParameters(self,configStr)

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

    def shoot(self, targetSquare, board=None, real=False):
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

        if board == None:
            board = gameBoard.GameBoard._instance

        # check the dummy cases and return False if any of them are true
        # NOTE FOR JAVA/C++: Talk to Chris about how checkLOS should be implemented
        if not self.canTakeAction() or not board._checkLOS(self.getSquare(), targetSquare) or self._bullets <= 0 or targetSquare.isEmpty():
            return False

        if real:
            print('SHOOT {0} {1}'.format(self.getId(), targetSquare.getId()))
	else:
            for idx, z in enumerate(board._entities):
                if z.getId() == targetSquare.getOccupant().getId():
                    z._hp -= 1 * self._rangedAccuracy
                    if z._hp <= 0:
                        targetSquare.clearOccupant()
                        del board._entities[idx]
                    break
        return True

    def search(self):
        """
        Search the current square for supplies
        """
        if not self.canTakeAction() or self._square.isSearched():
            return False
        print('SEARCH {0} {1}'.format(self.getId(), self._square.getId()))
        return True

    def getRangedAccuracy(self):
        return self._rangedAccuracy

    def countAmmo(self):
        return self._bullets
