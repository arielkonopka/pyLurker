#!/usr/bin/python3 
import pygame
import time
import sys
from LevelManager import levelManger as lvlM
from GfxDrv import gfxDrv
from GfxDrv import Sky 
from Board import board as board
from InputHandler import inputHandler as ih
from pygame import surface

LM=lvlM.lvlManger('./LevelData/Levels.json')
myPlayground=LM.createBoardObject(0)

SM=gfxDrv.skinManager('./Data/skins/skin.json')


myPlayground.iterateMech(None)



vh=gfxDrv.videoManager(SM,myPlayground,(1024,768),LM)



layers = Sky.sky([1920, 1080])
# sys.exit()
myInput=ih.iHandler()
state=0
statecnt=0
pos=(40,40)
direction=board._LEFT
level=0
lives=5 #lives implemented
#print(LM.getLevelsNo()-1)

#res=vh.startProcess(vh)
#res[0].start
#res[1].send("dupa")
while 1:

    cmd=myInput.getInput(layers)
    levelData=LM.getLevel(level)
   # scrHandle.fill(levelData['Colour'])
   # layers.draw(scrHandle)
    myPlayground.iterateMech(cmd)
    changedBoxes=myPlayground.getChangedBoxes()
    stats=myPlayground.getStats()
    #res[1].send([changedBoxes,stats,level])    

    if stats[4]<=0:
        if myPlayground.exitAchived==True: 
            if level<LM.getLevelsNo()-1:
                level+=1
            else:
                sys.exit()
        else:
            lives-=1
            if lives<=0:
                sys.exit()  
#        board.boardMember.players=-1
        myPlayground=LM.createBoardObject(level)
    vh.renderObjects(changedBoxes,level)
    vh.drawStats(stats)
    pygame.display.flip()
    #pygame.display.flip()
    time.sleep(1 / 40)
    statecnt-=1
    




