#!/usr/bin/python
"""
CS Games 2011
AI Competition

Chris Iverach-Brereton

This file contains the Zombie class, which is controlled
entirely by the computer

Competitors should NOT need to edit this file

#################
We asked if we could import this, and some guy with a wicked beard said so
#################
"""
import sys

from entity import *
import gameSquare
import math

class Zombie(Entity):

    # how far away can the zombie see people?
    _agroRange = 5

    def __init__(self, configStr=None):
        self._team = 1
        Entity.__init__(self, configStr)
        self._hp = 5

    def __str__(self):
        return Entity.__str__(self)

    def takeTurn(self, board):
        #print '[info] Entity',self._id,'starting turn'
        src = board.getEntities(Entity.HUMAN_TEAM)

        humans = []
        for h in src:
            if not h.isDead():
                humans.insert(0,h)
        random.shuffle(humans)

        # find the closest human
        closestHuman = None
        shortestDistance = math.sqrt(board.getWidth()**2+board.getHeight()**2)
        for h in humans:
            if not h.isDead() and h._square!=None and (board._checkLOS(self._square, h._square) or board.isAdjacent(self._square, h._square)):
                dy = self._square.getRow() - h._square.getRow()
                dx = self._square.getColumn() - h._square.getColumn()

                if math.sqrt(dy**2 + dx**2) < shortestDistance:
                    closestHuman = h
                    shortestDistance = math.sqrt(dy**2 + dx**2)

        #sys.stderr.write('ZOMBIE EMULATOR %s\n' % closestHuman)
        if closestHuman != None and int(shortestDistance) <= self._agroRange:
            print '[info] Entity',self._id,'smells living flesh'
            # move towards the human or attack if possible
            dy = self._square.getRow() - closestHuman._square.getRow()
            dx = self._square.getColumn() - closestHuman._square.getColumn()

            if abs(dy) <=1 and abs(dx) <=1:
                self.attack(closestHuman._square, False, board)
            else:
                # for this section we identfy the preferred directions to gi
                # i.e. the ones that move us closest to the target
                # if the primary direction fails try the backup (if one exists)
                # if two directions are equally weighted then randomly pick one
                # if nothing works don't move

                if dy > 0 and dx > 0:       # move up/left
                    # move along primary direction
                    if abs(dy) > abs(dx) and self.checkMove(gameSquare.GameSquare.DIRECTION_UP):
                        self.move(gameSquare.GameSquare.DIRECTION_UP)
                    elif abs(dy) < abs(dx) and self.checkMove(gameSquare.GameSquare.DIRECTION_LEFT):
                        self.move(gameSquare.GameSquare.DIRECTION_LEFT)

                    # primary failed; move along secondary
                    elif abs(dy) > abs(dx) and self.checkMove(gameSquare.GameSquare.DIRECTION_LEFT):
                        self.move(gameSquare.GameSquare.DIRECTION_LEFT)
                    elif abs(dy) < abs(dx) and self.checkMove(gameSquare.GameSquare.DIRECTION_UP):
                        self.move(gameSquare.GameSquare.DIRECTION_UP)

                    # tied primaries
                    # try either direction in a random order
                    elif abs(dy) == abs(dx):
                        r = random.randint(0,1)
                        if r==0 and self.checkMove(gameSquare.GameSquare.DIRECTION_UP):
                            self.move(gameSquare.GameSquare.DIRECTION_UP)
                        elif r==0 and self.checkMove(gameSquare.GameSquare.DIRECTION_LEFT):
                            self.move(gameSquare.GameSquare.DIRECTION_LEFT)
                        elif r==1 and self.checkMove(gameSquare.GameSquare.DIRECTION_LEFT):
                            self.move(gameSquare.GameSquare.DIRECTION_LEFT)
                        elif r==1 and self.checkMove(gameSquare.GameSquare.DIRECTION_UP):
                            self.move(gameSquare.GameSquare.DIRECTION_UP)



                elif dy < 0 and dx > 0:     # move down/left
                    # move along primary direction
                    if abs(dy) > abs(dx) and self.checkMove(gameSquare.GameSquare.DIRECTION_DOWN):
                        self.move(gameSquare.GameSquare.DIRECTION_DOWN)
                    elif abs(dy) < abs(dx) and self.checkMove(gameSquare.GameSquare.DIRECTION_LEFT):
                        self.move(gameSquare.GameSquare.DIRECTION_LEFT)

                    # primary failed; move along secondary
                    elif abs(dy) > abs(dx) and self.checkMove(gameSquare.GameSquare.DIRECTION_LEFT):
                        self.move(gameSquare.GameSquare.DIRECTION_LEFT)
                    elif abs(dy) < abs(dx) and self.checkMove(gameSquare.GameSquare.DIRECTION_DOWN):
                        self.move(gameSquare.GameSquare.DIRECTION_DOWN)

                    # tied primaries
                    # try either direction in a random order
                    elif abs(dy) == abs(dx):
                        r = random.randint(0,1)
                        if r==0 and self.checkMove(gameSquare.GameSquare.DIRECTION_DOWN):
                            self.move(gameSquare.GameSquare.DIRECTION_DOWN)
                        elif r==0 and self.checkMove(gameSquare.GameSquare.DIRECTION_LEFT):
                            self.move(gameSquare.GameSquare.DIRECTION_LEFT)
                        elif r==1 and self.checkMove(gameSquare.GameSquare.DIRECTION_LEFT):
                            self.move(gameSquare.GameSquare.DIRECTION_LEFT)
                        elif r==1 and self.checkMove(gameSquare.GameSquare.DIRECTION_DOWN):
                            self.move(gameSquare.GameSquare.DIRECTION_DOWN)

                elif dy > 0 and dx < 0:     # move up/right
                    # move along primary direction
                    if abs(dy) > abs(dx) and self.checkMove(gameSquare.GameSquare.DIRECTION_UP):
                        self.move(gameSquare.GameSquare.DIRECTION_UP)
                    elif abs(dy) < abs(dx) and self.checkMove(gameSquare.GameSquare.DIRECTION_RIGHT):
                        self.move(gameSquare.GameSquare.DIRECTION_RIGHT)

                    # primary failed; move along secondary
                    elif abs(dy) > abs(dx) and self.checkMove(gameSquare.GameSquare.DIRECTION_RIGHT):
                        self.move(gameSquare.GameSquare.DIRECTION_RIGHT)
                    elif abs(dy) < abs(dx) and self.checkMove(gameSquare.GameSquare.DIRECTION_UP):
                        self.move(gameSquare.GameSquare.DIRECTION_UP)

                    # tied primaries
                    # try either direction in a random order
                    elif abs(dy) == abs(dx):
                        r = random.randint(0,1)
                        if r==0 and self.checkMove(gameSquare.GameSquare.DIRECTION_UP):
                            self.move(gameSquare.GameSquare.DIRECTION_UP)
                        elif r==0 and self.checkMove(gameSquare.GameSquare.DIRECTION_RIGHT):
                            self.move(gameSquare.GameSquare.DIRECTION_RIGHT)
                        elif r==1 and self.checkMove(gameSquare.GameSquare.DIRECTION_RIGHT):
                            self.move(gameSquare.GameSquare.DIRECTION_RIGHT)
                        elif r==1 and self.checkMove(gameSquare.GameSquare.DIRECTION_UP):
                            self.move(gameSquare.GameSquare.DIRECTION_UP)

                elif dy < 0 and dx < 0:     # move down/right
                    # move along primary direction
                    if abs(dy) > abs(dx) and self.checkMove(gameSquare.GameSquare.DIRECTION_DOWN):
                        self.move(gameSquare.GameSquare.DIRECTION_DOWN)
                    elif abs(dy) < abs(dx) and self.checkMove(gameSquare.GameSquare.DIRECTION_RIGHT):
                        self.move(gameSquare.GameSquare.DIRECTION_RIGHT)

                    # primary failed; move along secondary
                    elif abs(dy) > abs(dx) and self.checkMove(gameSquare.GameSquare.DIRECTION_RIGHT):
                        self.move(gameSquare.GameSquare.DIRECTION_RIGHT)
                    elif abs(dy) < abs(dx) and self.checkMove(gameSquare.GameSquare.DIRECTION_DOWN):
                        self.move(gameSquare.GameSquare.DIRECTION_DOWN)

                    # tied primaries
                    # try either direction in a random order
                    elif abs(dy) == abs(dx):
                        r = random.randint(0,1)
                        if r==0 and self.checkMove(gameSquare.GameSquare.DIRECTION_DOWN):
                            self.move(gameSquare.GameSquare.DIRECTION_DOWN)
                        elif r==0 and self.checkMove(gameSquare.GameSquare.DIRECTION_RIGHT):
                            self.move(gameSquare.GameSquare.DIRECTION_RIGHT)
                        elif r==1 and self.checkMove(gameSquare.GameSquare.DIRECTION_RIGHT):
                            self.move(gameSquare.GameSquare.DIRECTION_RIGHT)
                        elif r==1 and self.checkMove(gameSquare.GameSquare.DIRECTION_DOWN):
                            self.move(gameSquare.GameSquare.DIRECTION_DOWN)

                elif dy > 0:                # move up only
                    if self.checkMove(gameSquare.GameSquare.DIRECTION_UP):
                        self.move(gameSquare.GameSquare.DIRECTION_UP)

                elif dy < 0:                # move down only
                    if self.checkMove(gameSquare.GameSquare.DIRECTION_DOWN):
                        self.move(gameSquare.GameSquare.DIRECTION_DOWN)

                elif dx > 0:                # move left only
                    if self.checkMove(gameSquare.GameSquare.DIRECTION_LEFT):
                        self.move(gameSquare.GameSquare.DIRECTION_LEFT)

                elif dx < 0:                # move right only
                    if self.checkMove(gameSquare.GameSquare.DIRECTION_RIGHT):
                        self.move(gameSquare.GameSquare.DIRECTION_RIGHT)

                else:                       # this should never happen
                    print '* Entity',self._id,'smells brains but can\'t reach them'

        else:
            print '[info] Entity',self._id,'staggers randomly'
            # move in a random direction
            direction = random.randint(1,4)
            increment = random.randint(0,1)
            if increment == 0:
                increment = -1

            for i in range(4):
                if self.checkMove(direction):
                    self.move(direction)
                    return
                #print 'can\'t move',direction
                direction = direction + increment

                if direction <=0:
                    direction = 4
                elif direction > 4:
                    direction = 1


        #print '[info] Entity',self._id,'done turn'
