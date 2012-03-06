#!/usr/bin/python
"""
AI Competition main (for day 1)
"""

import sys
import time

# for AI part 1 use the first import
# for AI part 2 use the second import
#from EditMe_Day1 import *
from EditMe_Day2 import *

# read in some test input to verify everything as we go
s = raw_input('# enter board dimensions (width height) > ')
print
height = int(s.split()[1])
width = int(s.split()[0])

boardStr = ''
board = GameBoard(height,width)

gameIsOn = True

player = None

while(gameIsOn):
    s = raw_input().strip()
    if len(s) > 0 and s[0]!='#':
        if s=='GAME OVER':
            sys.stderr.write('Received game over signal from server\n')
            gameIsOn = False

        elif s=='BEGIN BOARD':
            boardStr = s + '\n'

        elif s=='END BOARD':
            board.loadParameters(boardStr)
            if player == None:
                player = PlayerAI(board)
                #sys.stderr.write('Player Square: '+str(player._human._square)+'\n')
            print 'START TURN'
            player.takeTurn()
            print 'END TURN'
            sys.stdout.flush()
        else:
            boardStr = boardStr + s + '\n'

print
print 'GAME OVER'
