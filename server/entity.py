#!/usr/bin/python
"""
CS Games 2011
AI Competition

Chris Iverach-Brereton

This file contains the generic Entity class that
Survivor and Zombie inherit from
"""

import random
import gameSquare
import gameBoard

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
        
        self.actionsTaken = 0   # how many actions has this entity taken in this turn?
    
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
        
    def checkMove(self, direction):
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
        #print destSquare
        
        if destSquare==None or not destSquare.isEmpty() or not destSquare.isPassable():
            return False
        else:
            return True
        
    def move(self, direction):
        """
        Move from the current square in the specified direction if possible
        Return T if the move was valid and occurred successfully
        
        The client simply prints out the move
        The server deals with actually updating the world state
        """
        
        dirTxt = [
            'Invalid',
            'North',
            'South',
            'West',
            'East'
        ]
        
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
            
        # verify that the square is legal (i.e. on the board)
        if destX < 0 or destX >= len(gameBoard.GameBoard._instance._grid[0]) or destY < 0 or destY >= len(gameBoard.GameBoard._instance._grid):
            return False
            
        destSquare = gameSquare.findSquareByLocation(destX,destY)
        
        # only allow orthogonal moves of 1 square
        if destSquare==None:
            print '[debug] Entity',self._id,'cannot move in direction',dirTxt[direction],'(invalid square)'
            return False
        elif not destSquare.isEmpty():
            print '[debug] Entity',self._id,'cannot move in direction',dirTxt[direction],'(already occupied)'
            return False
        elif not destSquare.isPassable():
            print '[debug] Entity',self._id,'cannot move in direction',dirTxt[direction],'(impassible)'
            return False
        elif not self.canMakeAction():
            return False
            
        print '* Entity',self._id,'moved',dirTxt[direction]
        self._square.clearOccupant()
        destSquare.setOccupant(self)
        self.actionsTaken = self.actionsTaken+1
        
        return True
        
    def attack(self, targetSquare):
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
        if targetSquare.isEmpty():
            print '[debug] Entity',self._id,'cannot attack an empty square'
            return False
        elif abs(currX - destX) > 1 or abs(currY - destY) > 1:
            print '[debug] Entity',self._id,'cannot attack; target too far away'
            return False
        elif not self.canMakeAction():
            return False
            
        # do the actual attack
        target = targetSquare.getOccupant()
        
        if random.randint(0,100) < 100 * self._meleeAccuracy:
            target._hp = target._hp - 1
            
            if target._hp <= 0:
                print '* Entity',self._id,'killed entity',target._id,'(melee)'
                targetSquare.clearOccupant()
                
            else:
                print '* Entity',self._id,'hit entity',target._id,'(melee)'
        else:
            print '* Entity',self._id,'missed entity',target._id,'(melee)'
            
        return True
        
        
    def setSquare(self,sq):
        self._square = sq;
        
    def getSquare(self):
        return self._square
        
    def canMakeAction(self):
        if self.actionsTaken >=2:
            print '[cheat] Entity',self._id,'tried taking too many actions'
            return False
        elif self._hp <= 0:
            print '[cheat] Entity',self._id,'cannot take actions; it is dead'
            return False
        elif self._square == None:
            print '[error] Entity',self._id,'is not on a square'
            return False
            
        return True
        
    def isDead(self):
        return self._hp <= 0

Entity.lastId = -1
Entity.allEntities = []
Entity.ZOMBIE_TEAM = 1
Entity.HUMAN_TEAM = 0
