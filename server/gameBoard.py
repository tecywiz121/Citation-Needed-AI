#!/usr/bin/python
"""
CS Games 2011
AI Competition

Chris Iverach-Brereton

This file contains the game board and all associated functions & utility classes
"""

from gameSquare import *
import human
import zombie
import random
import math

class GameBoard:
    """
    This class contains an array of squares, and tracks
    the positions of suvivors and zombies throughout the game
    """
    
    _grid = []
    _squares = []
    _entities = []
    
    def __init__(self, width=0, height=0, numHumans=1, numZombies=10, percentBlocked=0, percentObscured=0):
        """
        Create a new, empty board with a specific height and width
        """
        
        # create the empty grid
        for y in range(height):
            self._grid.insert(y,[])
            for x in range(width): 
            
                passable = True
                blocksLOS = False
                searched = False
            
                if random.randint(0,100) < percentObscured:
                    blocksLOS = True
                else:
                    blocksLOS = False
            
                if random.randint(0,100) < percentBlocked:
                    passable = False
                else:
                    passable = True
            
                
            
                self._grid[y].insert(x, GameSquare(x,y, passable,blocksLOS))
                self._squares.insert(len(self._squares), self._grid[y][x])
                
        for i in range(numHumans):
            self._entities.insert(len(self._entities),human.Human(None))
            
        for i in range(numZombies):
            self._entities.insert(len(self._entities),zombie.Zombie(None))
            
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
                    if(id>Entity.lastId):
                        self._entities.insert(0,zombie.Zombie(l))
                    else:
                        Entity.allEntities[id].loadParameters(l)
                    
                
        
    def __str__(self):
        """
        Convert the board to a parsable string
        """
        
        template = """BEGIN BOARD
{1}{0}END BOARD"""
        
        entities = ''
        for e in self._entities:
            entities = entities + str(e) + '\n'
            
        squares = ''
        for row in self._grid:
            for cell in row:
                squares = squares + str(cell) + '\n'
                
        return template.format(squares,entities)
        
    def _checkLOS(self, src, dest):
        """
        Check if there is clear LOS between the source and destination GameSquares
        """
        dx = dest.getColumn() - src.getColumn()
        dy = dest.getRow() - src.getRow()
        
        # normalize dx and dy based on the total distance travelled
        maxSteps = max(abs(dx),abs(dy))
        if maxSteps>0:
            dy = dy / maxSteps
            dx = dx / maxSteps
        
        x = src.getColumn()
        y = src.getRow()
        
        while(int(x) != dest.getColumn() and int(y) !=dest.getRow()):
            #print x,y
            square = self._grid[int(y)][int(x)]
            if square.blocksLOS():
                return False
            
            x = x+dx
            y = y+dy
            
        return True

    def isAdjacent(self, src, target):
        dx = target.getColumn() - src.getColumn()
        dy = target.getRow() - src.getRow()
        
        return abs(dx) <= 1 and abs(dy) <= 1

    def getSquare(self, x, y):
        return self._grid[y][x]
        
    def getSquareById(self, id):
        return self._squares[id]

    def draw(self):
        for row in self._grid:
            for square in row:
                ch = None
                if square.isEmpty():
                    if square.blocksLOS() and not square.isPassable():
                        ch = 'X'
                    elif square.blocksLOS():
                        ch = '+'
                    elif not square.isPassable():
                        ch = 'x'
                    elif square.isSearched():
                        ch = ','
                    else:
                        ch = '.'
                elif square.getOccupant().getTeam() == 0:
                    ch = 'H'
                else:
                    ch = 'Z' #str(square.getOccupant().getId())
                    
                print ch,
            print

    def randomEmptySquare(self):
        row = random.randint(0,len(self._grid)-1)
        col = random.randint(0,len(self._grid[0])-1)
        
        while self._grid[row][col].getOccupant()!=None or not self._grid[row][col].isPassable():
            row = random.randint(0,len(self._grid)-1)
            col = random.randint(0,len(self._grid[0])-1)
            
        return self._grid[row][col]

    def getEntities(self,team):
        entities = []
        
        for e in self._entities:
            if e.getTeam() == team:
                entities.insert(0,e)
                
        if len(entities) == 0:
            return None
        else:
            return entities
            
    def getWidth(self):
        return len(self._grid[0])
    
    def getHeight(self):
        return len(self._grid)

GameBoard.checkLOS = lambda self,src,dest : GameBoard._instance._checkLOS(src,dest)
