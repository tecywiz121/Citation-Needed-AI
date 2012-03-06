#!/usr/bin/python
"""
CS Games 2011
AI Competition

Chris Iverach-Brereton

This file contains the Player class & related namespace for day 1 of the competition

Competitors must NOT create any code that illegally edits the state of the game (e.g.
changing human/zombie hit points).  Doing so may result in disqualification

Competitors must edit this file to create their AI for the competition

The AI must analyze the state of the world and assign two actions to their Survivor.
Available actions are:
    survivor.move(int) -- walk to an adjacent square (movement is orthogonal only)
                          directions are: GameSquare.DIRECTION_UP, .DIRECTION_DOWN, .DIRECTION_LEFT, .DIRECTION_RIGHT
    _players[i].attack(GameSquare) -- attack a zombie in an adjacent square (may be adjacent diagonally)
    _players[i].shoot(GameSquare) -- fire at a zombie.  The square may be any distance away, but requires clear LOS.  Uses 1 ammunition
    _players[i].search() -- search the survivor's current square for supplies

Each game square may be searched exactly once.
Searching a GameSquare may result in:
    - extra HP
    - extra ammunition
    - better melee or ranged accuracy
Humans may perform the same action multiple times in a turn, but are limited to exactly 2 actions
total for any given turn

Anything written to STDERR will be printed out by the server for debugging purposes
"""

# DO NOT CHANGE THESE IMPORTS
from entity import *
from human import *
from zombie import *
from gameSquare import *
from gameBoard import *
import sys


# add any additional imports you may need here
#import random
from internal import *
import time

turnTime = 0
def time_remaining():
    now = time.time()
    elapsed = now - turnTime
    return 2.0 - elapsed

class PlayerAI:
    _humans = []    # the team of human the player AI controls
    _board = None   # the game board the human and zombies exist on

    def __init__(self, board):
        self._board = board
        self._humans = board.getEntities(Entity.HUMAN_TEAM)
        self._zombies = board.getEntities(Entity.ZOMBIE_TEAM)

    def XYtoD(self, srcX, srcY, destX, destY):
        if destX > srcX:
            return GameSquare.DIRECTION_RIGHT
        elif destX < srcX:
            return GameSquare.DIRECTION_LEFT
        elif destY > srcY:
            return GameSquare.DIRECTION_DOWN
        elif destY < srcY:
            return GameSquare.DIRECTION_UP

        raise Exception('wtf?')

    def takeTurn(self):
        """
        Competitors must edit this function.
        You control a group of humans.  Each human can take two actions on their turn:
        e.g. move, move
        e.g. move, shoot
        e.g. shoot, move
        e.g. shoot, shoot
        e.g. attack, shoot
        e.g. move, search
        etc...

        Move accepts a direction as the parameter: GameSquare.DIRECTION_UP/.DIRECTION_DOWN/.DIRECTION_LEFT/.DIRECTION_RIGHT

        Shoot requires a target square and uses ammunition

        Attack requires a target square adjacent to the human (this square can be adjascent diagonally)
        Attack does not consume ammunition

        Search will search the current square for supplies.  Each square may only be searched once
        The human might find more ammunition, a bigger gun, first aid supplies

        For debugging anything you write to stderr will be printed by the server with a "[debug]" prefix
        """
        turnTime = time.time()
        sys.stderr.write('Starting player AI turn\n')

        field = Field(self._board.getWidth(), self._board.getHeight())
        for x in range(field.width):
            for y in range(field.height):
                square = self._board.getSquare(x, y)
                if not square.isPassable():
                    field.unpassable[(y, x)] = True
                if square.blocksLOS():
                    field.unseeable[(y, x)] = True
                if square.isSearched():
                    field.searched[(y, x)] = True

        board = ZombieBoard(field)

        for h in self._humans:
            if not h.isDead():
                square = h.getSquare()
                board.add_human(square.getColumn(), square.getRow(),
                                health=h.getHP(),
                                melee=h.getMeleeAccuracy(),
                                ranged=h.getRangedAccuracy(),
                                bullets=h.countAmmo(),
                                id=h._id)

        for z in self._zombies:
            square = z.getSquare()
            board.add_zombie(square.getColumn(), square.getRow(),
                            health=z.getHP(),
                            melee=z.getMeleeAccuracy())

        while board.is_max():
            move = board.minimax()
            sys.stderr.write('%s %s\n' % (move.action, move.value))
            sys.stderr.flush()

            action = move.action

            if action[0] == 'search':
                human = move.entities[(action[1], action[2])]
                square = self._board.getSquare(action[1], action[2])
                print 'SEARCH {0} {1}'.format(human.id, square._id)
            elif action[0] == 'move':
                direction = self.XYtoD(*action[1:])
                human = move.entities[(action[3],action[4])]
                print('MOVE {0} {1}'.format(human.id,direction))
            elif action[0] == 'melee':
                human = move.entities[(action[1], action[2])]
                square = self._board.getSquare(action[3], action[4])
                print 'ATTACK {0} {1}'.format(human.id, square._id)
            elif action[0] == 'shoot':
                human = move.entities[(action[1], action[2])]
                square = self._board.getSquare(action[3], action[4])
                print 'SHOOT {0} {1}'.format(human.id, square._id)
            board = move


        sys.stderr.write('Player turn finished\n')
