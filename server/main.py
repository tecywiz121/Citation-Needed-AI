#!/usr/bin/python
"""
Main server for the AI competition
"""
# Creates a child process for the competitor AI, communicates via STDIO
# 
# Main processing:
#     1- write world state to player process
#     2- wait for input from player process
#     3- process player output
#     4- sanity check world state; verify player moves are legal before applying them
#     5- update world state
#     6- move zombies (updates world state)
#     7- print new world state to client
#     8- flush player process stdin

import subprocess
import argparse
import fcntl
import os

from gameBoard import *

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("playerExe", metavar="/path/to/player/ai", type=str, help="Path to the player AI executable", default=None)
parser.add_argument("--height", type=int, help="Height of the board", default=12)
parser.add_argument("--width", type=int, help="Width of the board", default=12)
parser.add_argument("--zombies", type=int, help="Number of zombies", default=5)
#parser.add_argument("--player-row", type=int, help="Row for the human player to start on", default=-1)
#parser.add_argument("--player-col", type=int, help="Column for the human player to start on", default=-1)
parser.add_argument("--humans", type=int, help="Number of human players", default=1)
parser.add_argument("--blocked", type=int, help="%% of squares that are impassible", default=5)
parser.add_argument("--obscured", type=int, help="%% of squares that are passible but block LOS", default=10)
parser.add_argument("--max-turns", type=int, help="Maximum number of turns allowed before we assume the human wins", default=200)
args = parser.parse_args()

print 'Generating random board of size',args.width,'by',args.height,'containing',args.zombies,'zombies'
board = GameBoard(args.width,args.height,args.humans,args.zombies, args.blocked, args.obscured)

print 'Placing entities on the board'
for e in GameBoard._entities:
    square = board.randomEmptySquare()
    square.setOccupant(e)
    print 'placing entity',e._id,'on square',square._id

print 'Initial board state:'
print str(board)
turn = 1
print '\n\n=== START OF TURN',turn,'==='
board.draw()

print 'Starting Child Process',args.playerExe
client = subprocess.Popen(args.playerExe.split(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False,bufsize=1)
client.stdout.flush()

# set up client.stderr as non-blocking
#fd = client.stdout.fileno()
#fl = fcntl.fcntl(fd, fcntl.F_GETFL)
#fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
fd = client.stderr.fileno()
fl = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
print 'PID:',client.pid

print 'Writing initial state to child process'
client.stdin.write(str(args.width)+" "+str(args.height)+"\n")
client.stdin.write(str(board)+"\n")
client.stdin.flush()

gameOver = False

turns = 0

print 'Starting Game'
while not gameOver:
    turns = turns+1
    
    client.stderr.flush()
    try:
        dbg = client.stderr.readline().strip()
        if len(dbg) > 0:
            print '[debug]',dbg
    except:
        dbg = ''
    
    client.stdout.flush()
    line = client.stdout.readline().strip()
    
    actions = []
    
    while line != 'END TURN':
        try:
            dbg = client.stderr.readline().strip()
            if len(dbg) > 0:
                print '[debug]',dbg
        except:
            dbg = ''
        
        if len(line) > 0 and line[0]!='#':
            #print '>',line,'<'
            actions.insert(len(actions), line)
        #elif len(line) > 0 and line[0]=='#':
        #    print '[debug]',line.lstrip('#')
            
        #client.stdout.flush()
        #client.stderr.flush()
        #client.stdin.flush()
        line = client.stdout.readline().strip()
        
        #print '>>>',line
        
    actions.insert(len(actions), line)
    
    print '[info] Recieved end of turn signal from client'
    
    # get ready for the new turn
    for e in Entity.allEntities:
        e.actionsTaken = 0
    
    # handle all of the actions the player wants to perform
    for a in actions:
        tokens = a.split()
        
        if len(tokens) == 3:
            action = tokens[0].strip().upper()
            entity = Entity.allEntities[int(tokens[1])]
            target = int(tokens[2])
            
            #print '[info] Evaluating player action',action
            
            if action == 'MOVE':
                entity.move(target)
            
            elif action == 'SHOOT':
                entity.shoot(board.getSquareById(target))
            
            elif action == 'SEARCH':
                entity.search(board.getSquareById(target))
                
            elif action == 'ATTACK':
                entity.attack(board.getSquareById(target))
                
    # zombies take their turns
    print '[info] Taking Zombie Turns'
    zombies = board.getEntities(Entity.ZOMBIE_TEAM)
    random.shuffle(zombies)
    for z in zombies:
        if not z.isDead():
            z.takeTurn(board)
    print '[info] Zombie Turns Over'
            
    
    # check for game over
    humans = board.getEntities(Entity.HUMAN_TEAM)
    numAlive = 0
    for h in humans:
        if not h.isDead():
            numAlive = numAlive + 1
    
    numZ = 0
    for z in zombies:
        if not z.isDead():
            numZ = numZ + 1
    
    if numZ == 0 and numAlive == 0:
        print '* Everything died! Draw'
        gameOver = True
    elif numZ == 0:
        print '* All zombies are dead! Player win'
        gameOver = True
    elif numAlive == 0:
        print '* All humans are dead! Player loss'
        gameOver = True
    elif turns==args.max_turns:
        print '* Ran out of turns.  Draw'
        gameOver = True
    else:
        turn = turn+1
        print '\n\n=== START OF TURN',turn,'==='
        board.draw()
        client.stdin.write(str(board)+'\n')
        client.stdin.flush()

client.stdin.write('GAME OVER\n')
client.stdin.flush()
gameOver = True
print '* Player AI lasted',turn,'turns'
print 'GAME OVER'
