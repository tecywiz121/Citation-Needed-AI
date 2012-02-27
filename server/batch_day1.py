#!/usr/bin/python

import subprocess
import argparse
import fcntl
import os

MAX_TURNS = 10

teamExecutables = [
    # paths to competitor executables go here
    # in order from team 1 to team n
    '../python/main.py',
    '../c++/main'
]

dimensions = [
    [10,10],
    [15,15]#,
#    [25,25],
#    [50,50]
]

zombies = [
    5,
    10#,
#    25,
#    50
]

blocked = [
    0,
    5,
    10,
    15
]

obscured = [
    0,
    5,
    10,
    25
]

humans = [
    1
]

cmd = './main.py {playerExe} --height {height} --width {width} --zombies {zombies} --humans {humans} --blocked {blocked} --obscured {obscured}'

csv = open('day1_raw.csv','w')
csv.write('Team No,Attempt,Height,Width,Zombies,Humans,Turns,Win\n')

csvTemplate = '{team},{turn},{height},{width},{zombies},{humans},{turns},{win}\n'

clean = open('day1_summary.csv','w')
clean.write('Team No,Avg Turns,Wins,Draws,Losses\n')

cleanTemplate = '{team},{score},{wins},{draws},{losses}\n'

for i in range(len(teamExecutables)):
    
    numWins = 0
    numDraws = 0
    numLosses = 0
    totalTurns = 0
    totalGames = 0
    
    
    for d in dimensions:
        width = d[0]
        height = d[1]
        
        for z in zombies:
            for b in blocked:
                for o in obscured:
                    for h in humans:
                        exe = cmd.format(
                            playerExe = teamExecutables[i],
                            height = height,
                            width = width,
                            zombies = z,
                            humans = h,
                            blocked = b,
                            obscured = o
                        )
                        
                        for t in range(MAX_TURNS):
                            print 'Executing',exe
                            client = subprocess.Popen(exe.split(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False,bufsize=1)
                            
                            (stdout,stderr) = client.communicate()
                            
                            winLossDraw = stdout.split('\n')[-4]
                            turns = stdout.split('\n')[-3]
                            
                            if 'win' in winLossDraw:
                                winLoss = 1
                            else:
                                winLoss = 0
                                
                            turns = turns.split()[-2]
                            
                            # write to the raw log
                            csv.write(csvTemplate.format(
                                team = i,
                                turn = t,
                                height = height,
                                width = width,
                                zombies = z,
                                humans = h,
                                turns = 200 if winLoss else turns,
                                win = winLoss
                            ))
                            
                            # update the summary stats
                            totalGames = totalGames +1
                            
                            if 'win' in winLossDraw:
                                numWins = numWins+1
                            elif 'draw' in winLossDraw:
                                numDraws = numDraws+1
                            else:
                                numLosses = numLosses+1
                                
                            totalTurns = totalTurns + int(turns)
                            
    avgTurns = totalTurns/totalGames
    clean.write(cleanTemplate.format(wins=numWins, draws=numDraws, losses=numLosses, score=avgTurns,team=i))

csv.close()
clean.close()
