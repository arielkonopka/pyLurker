import pygame
import random
import sys
import time
import pygame
import json
from pygame import FULLSCREEN
from pygame import surface
from Board import board
from pygame import draw
from pygame import font


class skinManager:
    fname=None
    skinObject=None
    spriteSize=None
    textureFile=None
    shapes=None
    def __init__(self,fname,skinName='GNU Robbo'):
        #the file must exist, we do not have a fallback for it
        self.fname=fname
        fDesc=open(self.fname)
        self.skinObject=json.load(fDesc)
        fDesc.close()
        for skin in self.skinObject:
            if skin['SkinName']==skinName:
                #ok, here is our skin to be read
                self.spriteSize=(skin['SpriteSize'][0],skin['SpriteSize'][0])
                self.textureFile=skin['Textures']['TextureFile']
                self.lightsFile=skin['Textures']['LightsFile']
                self.shapes=skin['Shapes']
                self.interlace=skin["Interlace"]
    def getObj(self,name):
        return self.shapes[name]














class videoManager:
    animatedObject=[[[(0,0)]]]

    def __init__(self,scrHndl:pygame.surface.Surface,skinMngr,playground,BoardPosOnScreen=(10,30),BoardSize=(60,20)):
        spriteSize=skinMngr.spriteSize
        interlace=skinMngr.interlace
        textureFile=skinMngr.textureFile
        self.teleportIn=skinMngr.getObj('teleportIn')
        self.teleportOut=skinMngr.getObj('teleportOut')
        self.player=skinMngr.getObj('player')
        self.wall=skinMngr.getObj('wall')
        self.bomb=skinMngr.getObj('bomb')
        self.ammo=skinMngr.getObj('ammo')
        self.box=skinMngr.getObj('box')
        self.key=skinMngr.getObj('key')
        self.token=skinMngr.getObj('token')
        self.box=skinMngr.getObj('box')
        self.missile=skinMngr.getObj('missile')
        self.empty=skinMngr.getObj('empty')
        self.door=skinMngr.getObj('door')
        self.monster=skinMngr.getObj('monster')
        self.exit=skinMngr.getObj('exit')
        self.teleport=skinMngr.getObj('teleport')
        self.dying=skinMngr.getObj('elementDie')


        #load the texture file first
        self.__iconsTexture=pygame.image.load(textureFile)
        #set up the texture parameters
        self.__iconWidth=spriteSize[0]
        self.__IconHeight=spriteSize[1]
        self.interlace=interlace
        self.__boardPos=BoardPosOnScreen
        self.__BoardSize=(BoardSize[0]*self.__iconWidth,BoardSize[1]*self.__IconHeight)
        self.__boardSizeElements=BoardSize
        #this is our screen surface
        self.__srcHndl:pygame.surface.Surface=scrHndl  
        self.__viewUpperCorner=(0,0)
        pygame.font.init()
        self.__font=pygame.font.SysFont("Courier",40)


    def drawObjectOnScreen(self,position,objectType):
        #player-5th row
        if not objectType:
         #   print('no')
            return
        switcher={
            board.EMPTYELEMENT:self.drawEmpty,
            board.PLAYER:self.drawPlayer,
            board.WALL:self.drawWall,
            board.BOX:self.drawBox,
            board.BOMB:self.drawBomb,
            board.AMMO:self.drawAmmo,
            board.KEY:self.drawKey,
            board.TOKEN:self.drawToken,
            board.MISSILE:self.drawMissile,
            board.DOOR:self.drawDoor,
            board.MONSTER:self.drawMonster,
            board.EXIT:self.drawExit,
            board.TELEPORT:self.drawTeleport
            }
#        if objectType[0]!=board.EMPTYELEMENT and self.playground!=None:
#            bg=  switcher.get(self.playground[position[0]][position[1]].steppingOn.Type)  
        
        drawFunc=switcher.get(objectType[0])
        rect=(position[0],position[1],32,32)
        
        smell=objectType[4]
        if smell[1]>0:
            pygame.draw.rect(self.__srcHndl,(smell[1],smell[1],smell[1]),rect)

        if  drawFunc:
            drawFunc(position,objectType)
#this routine is for still unmutable inanimated objects, but different types
#            0          1               2               3        4               5             6
#(x,y),elem.type,elem.direction,elem.animPhase,elem.subType,self.smell[x][y],elem.outPorting,elem.inPorting))
    def drawBasicElement(self,position,objectType,animPatt):
        if objectType[5] >0 or objectType[6]>0 or objectType[7]>0:
            #teleportation
            if objectType[5]>0:
                #portIn
                xPos=self.teleportIn[objectType[5]%len(self.teleportIn)][0]
                yPos=self.teleportIn[objectType[5]%len(self.teleportIn)][1]
            if objectType[6]>0:
                #portout
                xPos=self.teleportOut[objectType[6]%len(self.teleportOut)][0]
                yPos=self.teleportOut[objectType[6]%len(self.teleportOut)][1]
            if objectType[7]>0:
                #portout
                xPos=self.dying[objectType[7]%len(self.dying)][0]
                yPos=self.dying[objectType[7]%len(self.dying)][1]    
        else:
            sdirection=None
            if not animPatt:
                return
            if objectType[1]!=None: 
                sdirection=animPatt[objectType[1] % (len(animPatt))]
            else:   
                sdirection=animPatt[0]
           # print("{} -> {} ".format(objectType[3],len(sdirection) ))
            sType=sdirection[objectType[3] % len(sdirection) ]
            xPos=sType[objectType[2] % len(sType)][0]
            yPos=sType[objectType[2] % len(sType)][1]
        self.__srcHndl.blit(self.__iconsTexture,position,((self.__iconWidth+self.interlace)*xPos+self.interlace,
            (self.__IconHeight+self.interlace)*yPos+self.interlace,
            self.__iconWidth,
            self.__IconHeight))
    
    def drawTeleport(self,position,objectType):
        self.drawBasicElement(position,objectType,self.teleport)

    def drawMonster(self,position,objectType):
        self.drawBasicElement(position,objectType,self.monster)
    
    def drawMissile(self,position,objectType):
        self.drawBasicElement(position,objectType,self.missile)

    def drawToken(self,position,objectType):
        self.drawBasicElement(position,objectType,self.token)   
    def drawKey(self,position,objectType):
        self.drawBasicElement(position,objectType,self.key)   
    def drawBox(self,position,objectType):
        self.drawBasicElement(position,objectType,self.box)

    def drawBomb(self,position,objectType):
        self.drawBasicElement(position,objectType,self.bomb)

    def drawAmmo(self,position,objectType):
        self.drawBasicElement(position,objectType,self.ammo)

    def drawWall(self,position,objectType):
        self.drawBasicElement(position,objectType,self.wall)


    def drawPlayer(self,position,objectType):
        self.drawBasicElement(position,objectType,self.player)
    def drawEmpty(self,position,objectType):
        return
        self.drawBasicElement(position,objectType,self.empty)
    def drawDoor(self,position,objectType):
        self.drawBasicElement(position,objectType,self.door)

    def drawExit(self,position,objectType):
        self.drawBasicElement(position,objectType,self.exit)

    def renderObjects(self,objlist):
        vUX:int=self.__viewUpperCorner[0]
        vUY:int=self.__viewUpperCorner[1]
        bSX:int=self.__boardSizeElements[0]
        bSY:int=self.__boardSizeElements[1]
        bPX:int=self.__boardPos[0]
        bPY:int=self.__boardPos[1]
        for obj in objlist:
            if not obj:
                continue
            x:int=obj[0]
            y:int=obj[1]
            if x<=bSX+vUX  and x>=vUX  and y<=vUY+bSY and y>=vUY:
                posx=(x-vUX)*self.__iconWidth+bPX
                posy=(y-vUY)*self.__IconHeight+bPY
               # print((posx,posy),(obj[2],obj[3],obj[4]))
               #(x,y,elem.type,elem.direction,elem.animPhase,elem.subType,self.smell[x][y])
                self.drawObjectOnScreen((posx,posy),(obj[2],obj[3],obj[4],obj[5],obj[6],obj[7],obj[8],obj[9]))


    def drawStats(self,stats):
        sf=self.__font.render("Keys: {}  Ammo: {} Tokens: {} Tokens remaining: {}".format(stats[0],stats[1],stats[2],stats[3]), None, (200,200,200))
        self.__srcHndl.blit(sf,(200,700))
        pass




def screenInit(scrSize):
    pygame.init()
 #   screen = pygame.display.set_mode(scrSize, FULLSCREEN, 8)
    screen = pygame.display.set_mode(scrSize)
  
    return screen

def standalone():
    print("This is a pyRobbo gfx driver, and should not be used as a standalone application, sorry.")
    skin=skinManager('/home/c/PycharmProjects/pythonProject/Data/skins/skin.json')
    
    
    pass



if __name__=='__main__':
    standalone()




