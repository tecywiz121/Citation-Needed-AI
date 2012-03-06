#!/usr/bin/python
"""
CS Games 2012
AI Competition

Chris Iverach-Brereton

This file contains the squares that the game board is made up of
Each type of square is a subclass of a generic GameSquare superclass
"""

import entity
import sys

class GameSquare:
    """
    This class is the generic superclass that all other types of square
    inherit from
    """

    _id = -1
    _isPassable = True
    _blocksLOS = False
    _isSearched = False
    _x = -1
    _y = -1

    # the Entity that is in this square
    _occupant = None


    def __init__(self, x, y, isPassable=True, blocksLOS=False, isSearched=False):
        """
        Create a new square with a specific x/y position
        """
        self._x = x
        self._y = y

        self._isPassable = isPassable
        self._blocksLOS = blocksLOS
        self._isSearched = isSearched

        GameSquare.lastId = GameSquare.lastId + 1
        self._id = GameSquare.lastId

        GameSquare.allSquares.insert(self._id,self)

    def __str__(self):
        occupantId = -1
        if(self._occupant!=None):
            occupantId = self._occupant.getId()

        return "Square {0} [occupant:{1},passable:{2},blocklos:{3},searched:{4},x:{5},y:{6}]".format(
            self._id,
            occupantId,
            self._isPassable,
            self._blocksLOS,
            self._isSearched,
            self._x,
            self._y
        )

    def loadParameters(self, configStr):
        tokens = configStr.split()
        id = tokens[1]
        self._id = int(id)

        attrs = configStr[configStr.index('[')+1:configStr.index(']')]
        attrTokens = attrs.split(',')

        for t in attrTokens:
            tokens = t.split(':')
            name = tokens[0].lower().strip()
            value = tokens[1].lower().strip()


            if name == 'occupant':
                if int(value) == -1:
                    self._occupant = None

                else:
                    #sys.stderr.write(str(value)+ ' ' + str(len(entity.Entity.allEntities))+'\n')
                    self.setOccupant(entity.Entity.allEntities[int(value)])

            elif name == 'passable':
                self._isPassable = (value == 'true')

            elif name == 'blocklos':
                self._blocksLOS = (value == 'true')

            elif name == 'searched':
                self._isSearched = (value == 'true')

            elif name == 'x':
                self._x = int(value)

            elif name == 'y':
                self._y = int(value);

    def isSearched(self):
        return self._isSearched

    def isPassable(self):
        return self._isPassable

    def blocksLOS(self):
        return self._blocksLOS

    def search(self):
        if not self.isSearched():
            self.isSearched = True

    def isEmpty(self):
        return self._occupant == None


    def getRow(self):
        return self._y

    def getColumn(self):
        return self._x

    def getId(self):
        return self._id

    def setOccupant(self, entity):
        self._occupant = entity
        if entity!=None:
            entity.setSquare(self)

    def getOccupant(self):
        return self._occupant

    def clearOccupant(self):
        if self._occupant !=None:
            self._occupant.setSquare(None)
        self.setOccupant(None)

GameSquare.lastId = -1
GameSquare.DIRECTION_UP = 1
GameSquare.DIRECTION_DOWN = 2
GameSquare.DIRECTION_LEFT = 3
GameSquare.DIRECTION_RIGHT = 4

GameSquare.allSquares = []

def findSquareByLocation(x,y):
    """
    Find a square with specific x/y coordinates
    (note: x is the same as column, y is the same as row
    so if you use row/column notation instead of x/y you
    should call this function as findSquareByLocation(col,row)
    """
    for s in GameSquare.allSquares:
        if s._x == x and s._y == y:
            return s
    return None
