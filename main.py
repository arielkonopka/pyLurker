
import pygame
import time
import sys
from LevelManager import levelManger as lvlM
from GfxDrv import gfxDrv
from GfxDrv import Sky 
from Board import board as board
from InputHandler import inputHandler as ih
from pygame import surface

LM=lvlM.lvlManger('/home/c/PycharmProjects/pythonProject/LevelData/Levels.json')
myPlayground=LM.createBoardObject(0)

SM=gfxDrv.skinManager('/home/c/PycharmProjects/pythonProject/Data/skins/skin.json')


myPlayground.iterateMech(None)
changedBoxes=myPlayground.getChangedBoxes() #this will return all changed boxes
#print(changedBoxes)






scrHandle:pygame.surface.Surface= gfxDrv.screenInit([1620, 780])
vh=gfxDrv.videoManager(scrHandle,SM,myPlayground)



layers = Sky.sky([1920, 1080])
# sys.exit()
myInput=ih.iHandler()
state=0
statecnt=0
pos=(40,40)
direction=board._LEFT
level=0
print(LM.getLevelsNo()-1)
while 1:
    cmd=myInput.getInput(layers)
    scrHandle.fill([40, 20, 80])
   # layers.draw(scrHandle)
    myPlayground.iterateMech(cmd)
    changedBoxes=myPlayground.getChangedBoxes() #this will return all changed boxes
    stats=myPlayground.getStats()
    vh.drawStats(stats)
    vh.renderObjects(changedBoxes)
    if stats[4]<=0:

        if myPlayground.exitAchived==True: 
            if level<LM.getLevelsNo()-1:
                level+=1
            else:
                sys.exit()
        else:
            pass  

        myPlayground=LM.createBoardObject(level)
    pygame.display.flip()
    time.sleep(1 / 40)
    statecnt-=1
 # qqq  print(cmd)
    




q