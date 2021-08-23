import pygame
import sys
from Board import board

class iHandler():
    keyDown = False
    keyCode = None
    keyCnt = 0
    __keysPressed=[]

    def __init__(self):
        self.keyCnt=0
        self.keyDown=False
        self.keyCode=None

    def getInput(self,layers):
       # exCMD=None
        exCmdLeft=None
        exCmdRight=None
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (self.keyDown and self.keyCode == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if self.__keysPressed:
                    self.__keysPressed.append(event)
                else:
                    self.__keysPressed=[event]
            elif event.type == pygame.KEYUP:
                for myEvents in self.__keysPressed:
                    if event.key==myEvents.key:
                        self.__keysPressed.remove(myEvents)
                        break
        if self.__keysPressed:            
            for event in self.__keysPressed:
                if event.key==pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    exCMD=board._EXIT
                    break
              #  print("{} -> {}".format(event.key, event.mod & 1 ))
                
                if event.key==pygame.K_UP:
                    exCmdLeft=(board._UP,event.mod) 
                    continue
                elif event.key==pygame.K_DOWN:
                    exCmdLeft=(board._DOWN,event.mod)
                    continue
                elif event.key==pygame.K_LEFT:
                    exCmdLeft=(board._LEFT,event.mod)
                    continue
                elif event.key==pygame.K_RIGHT:
                    exCmdLeft=(board._RIGHT,event.mod)
                elif event.key==pygame.K_a:
                    exCmdRight=(board._LEFT,event.mod)
                    continue
                elif event.key==pygame.K_d:
                    exCmdRight=(board._RIGHT,event.mod)
                    continue
                elif event.key==pygame.K_w:
                    exCmdRight=(board._UP,event.mod)
                    continue
                elif event.key==pygame.K_s:
                    exCmdRight=(board._DOWN,event.mod)

        return (exCmdLeft,exCmdRight)


