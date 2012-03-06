#!/usr/bin/python
"""
CS Games 2012
AI Competition

Chris Iverach-Brereton

This file contains the generic Entity class that
Survivor and Zombie inherit from
"""

import random
import gameSquare

class Entity:
    """
    A generic entity that can exist in the game world
    """

    # a unique ID assigned to each entity
    _id = -1

    # the entity's hit-points
    _hp = 2

    # the odds of this entity doing damage in melee
    _meleeAccuracy = 0.5

    _team = 0

    _square = None

    def __init__(self, configStr=None):
        Entity.lastId = Entity.lastId+1
        self._id = Entity.lastId

        if(configStr != None):
            self.loadParameters(configStr)

        Entity.allEntities.insert(self._id,self)

    def loadParameters(self, configStr):
        """
        Parse the output from Entity.__str__ and apply it
        to this object
        """

        tokens = configStr.split()
        id = int(tokens[1])

        if id!=self._id:
            print '# ERROR: wrong id for entity',self._id,'found:',id

        self._id = int(id)

        attrs = configStr[configStr.index('[')+1:configStr.index(']')]
        attrTokens = attrs.split(',')

        for t in attrTokens:
            tokens = t.split(':')
            name = tokens[0].lower().strip()
            value = tokens[1].lower().strip()

            if name == 'hp':
                self._hp = int(value)

            elif name == 'team':
				self._team = int(value)

            elif name == 'melee':
                self._meleeAccuracy = float(value)

    def __str__(self):
        return "Entity {0} [hp:{1},team:{2},melee:{3}]".format(self._id, self._hp,self._team,self._meleeAccuracy)

    def getId(self):
        return self._id

    def getHP(self):
        return self._hp

    def getTeam(self):
		return self._team

    def getMeleeAccuracy(self):
        return self._meleeAccuracy

    def checkMove(self, direction):
        """
        Check if the entity is able to move in the specified direction
        """
        currY = self._square.getRow()
        currX = self._square.getColumn()

        destX = currX
        destY = currY

        if direction == gameSquare.GameSquare.DIRECTION_UP:
            destY = destY - 1
        elif direction == gameSquare.GameSquare.DIRECTION_DOWN:
            destY = destY + 1
        elif direction == gameSquare.GameSquare.DIRECTION_LEFT:
            destX = destX - 1
        elif direction == gameSquare.GameSquare.DIRECTION_RIGHT:
            destX = destX + 1

        destSquare = gameSquare.findSquareByLocation(destX,destY)

        if destSquare==None or not destSquare.isEmpty() or not destSquare.isPassable():
            return False
        else:
            return True

    def move(self, direction, real=False):
        """
        Move from the current square in the specified direction if possible
        Return T if the move was valid and occurred successfully

        The client simply prints out the move
        The server deals with actually updating the world state
        """

        currY = self._square.getRow()
        currX = self._square.getColumn()

        destX = currX
        destY = currY

        if direction == gameSquare.GameSquare.DIRECTION_UP:
            destY = destY - 1
        elif direction == gameSquare.GameSquare.DIRECTION_DOWN:
            destY = destY + 1
        elif direction == gameSquare.GameSquare.DIRECTION_LEFT:
            destX = destX - 1
        elif direction == gameSquare.GameSquare.DIRECTION_RIGHT:
            destX = destX + 1

        destSquare = gameSquare.findSquareByLocation(destX,destY)

        # only allow orthogonal moves of 1 square
        if not self.canTakeAction() or destSquare==None or not destSquare.isEmpty() or not ((currX - destX == 0 and abs(currY - destY) == 1) or (abs(currX - destX) == 1 and currY - destY == 0)):
            return False

        if real:
            print('MOVE {0} {1}'.format(self._id,direction))
        return True

    def attack(self, targetSquare, real=False, board=None):
        """
        Attack the occupant of an adjacent square in melee
        Note: you may attack your own square to commit suicide without using bullets

        Returns True if the attack was successfully accomplished
        Returns False if the attack was not allowed because the square is too far away or the target square was empty

        The client program simply prints out the decisions to STDOUT
        The Server program will actually "roll" and apply damage
        """

        # check that the square is occupied and in melee range
        currX = self._square.getRow()
        currY = self._square.getColumn()
        destX = targetSquare.getRow()
        destY = targetSquare.getColumn()
        if not self.canTakeAction() or targetSquare.isEmpty() or abs(currX - destX) > 1 or abs(currY - destY) > 1:
            return False

        # print out the attack
        if real:
            print("ATTACK {0} {1}".format(self._id, targetSquare.getId()))
        elif board:
            for idx,z in enumerate(board._entities):
                if z.getId() == targetSquare.getOccupant().getId():
                    z._hp -= 1 * self._meleeAccuracy
                    if z._hp <= 0:
                        targetSquare.clearOccupant()
                        del board._entities[idx]
                    break


        return True

    def isDead(self):
        return self._hp <= 0

    def getSquare(self):
        return self._square

    def setSquare(self,sq):
        self._square = sq

    def canTakeAction(self):
        return not self.isDead() #and self._square != None

Entity.lastId = -1
Entity.allEntities = []
Entity.ZOMBIE_TEAM = 1
Entity.HUMAN_TEAM = 0
