#!/usr/bin/python
"""
CS Games 2012
AI Competition

Chris Iverach-Brereton

This file contains the game board and all associated functions & utility classes
"""

from gameSquare import *
import human
import zombie
import random
import math
import entity

class GameBoard:
    """
    This class contains an array of squares, and tracks
    the positions of suvivors and zombies throughout the game
    """

    _grid = []
    _entities = []

    def __init__(self, width=0, height=0, numHumans=0, numZombies=0):
        """
        Create a new, empty board with a specific height and width
        """

        # create the empty grid
        for y in range(height):
            self._grid.insert(y,[])
            for x in range(width):
                passable = False
                blocksLOS = False
                searched = False

                self._grid[y].insert(x, GameSquare(x,y, passable,blocksLOS))

        GameBoard._instance = self

    def loadParameters(self, configStr):
        """
        Create a new game board based on another GameBoard's string representation
        """

        lines = configStr.split('\n')
        for l in lines:
            l = l.strip().lower()
            if len(l)>0 and l[0] != '#' and l!='begin board' and l!='end board': # if the line is a comment or a block divider we ignore it
                #print '#',l
                tokens = l.split()
                id = int(tokens[1])

                if tokens[0] == 'square':
                    GameSquare.allSquares[id].loadParameters(l)
                elif tokens[0] == 'entity':
                    # create the new entities if they do not already exist
                    # otherwise update it
                    if(id>entity.Entity.lastId):
                        if 'team:0' in l:
                            e = human.Human(l)
                        else:
                            e = zombie.Zombie(l)
                        self._entities.insert(e._id,e)
                        #sys.stderr.write(str(e)+'\n')
                    else:
                        entity.Entity.allEntities[id].loadParameters(l)



    def __str__(self):
        """
        Convert the board to a parsable string
        """

        template = """BEGIN BOARD
{1}
{0}
END BOARD"""

        entities = ''
        for e in self._entities:
            entities = entities + str(e) + '\n'

        squares = ''
        for row in self._grid:
            for cell in row:
                squares = squares + str(cell) + '\n'

        return template.format(squares,entities)

    def getWidth(self):
        return len(self._grid[0])

    def getHeight(self):
        return len(self._grid)

    def isAdjacent(self, src, target):
        dx = target.getColumn() - src.getColumn()
        dy = target.getRow() - src.getRow()

        return abs(dx) <= 1 and abs(dy) <= 1

    # NOTE FOR JAVA/C++: talk to Chris about how this should be implemented
    def _checkLOS(self, src, dest):
        """
        Check if there is clear LOS between the source and destination GameSquares
        """
        dx = dest.getColumn() - src.getColumn()
        dy = dest.getRow() - src.getRow()

        # normalize dx and dy
        maxSteps = max(abs(dx),abs(dy))
        if maxSteps>0:
            dy = dy / maxSteps
            dx = dx / maxSteps

        x = src.getColumn()
        y = src.getRow()

        while(int(x) != dest.getColumn() or int(y) !=dest.getRow()):
            square = self._grid[int(y)][int(x)]
            if square.blocksLOS():
                return False

            x = x+dx
            y = y+dy

        return True

    def getSquare(self, x, y):
        return self._grid[y][x]

    def draw(self):
        """
        Draw the board as an ascii grid
        """
        for row in self._grid:
            print '#',
            for square in row:
                ch = None
                if square.isEmpty():
                    if square.blocksLOS() and not square.isPassable():
                        ch = '@'
                    elif square.blocksLOS():
                        ch = '$'
                    elif not square.isPassable():
                        ch = '*'
                    elif square.isSearched():
                        ch = ','
                    else:
                        ch = '.'
                elif square.getOccupant().getTeam() == 0:
                    ch = 'H'
                else:
                    ch = 'Z'

                print ch,
            print

    def getEntities(self,team):
        """
        Return a list of all entities on a single team
        """
        entities = []

        for e in self._entities:
            if e.getTeam() == team:
                entities.insert(0,e)

        if len(entities) == 0:
            return None
        else:
            return entities

# NOTE FOR JAVA/C++: talk to Chris about how this should be implemented
GameBoard.checkLOS = lambda self,src,dest : GameBoard._instance._checkLOS(src,dest)
