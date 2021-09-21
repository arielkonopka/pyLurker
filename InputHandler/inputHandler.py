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
                mod=0
                if event.key==pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    exCMD=board._EXIT
                    break
       #         pygame.K_LCTRL
              #  print("{} -> {}".format(event.key, event.mod & 1 ))
                if event.key==pygame.K_LCTRL or event.key==pygame.K_RCTRL or (event.mod & (pygame.KMOD_CTRL | pygame.KMOD_LCTRL)):
                    mod=1
                if event.key==pygame.K_UP or event.key==pygame.K_w:
                    exCmdLeft=(board._UP,mod) 
                    continue
                elif event.key==pygame.K_DOWN or event.key==pygame.K_s:
                    exCmdLeft=(board._DOWN,mod)
                    continue
                elif event.key==pygame.K_LEFT or event.key==pygame.K_a:
                    exCmdLeft=(board._LEFT,mod)
                    continue
                elif event.key==pygame.K_RIGHT or event.key==pygame.K_d:
                    exCmdLeft=(board._RIGHT,mod)

        return exCmdLeft


if __name__=='__main__':
    ex=False
    pygame.init()
    screen = pygame.display.set_mode((1024,768), pygame.FULLSCREEN, 8)
    while not ex:
        for event in pygame.event.get():    
            print("{} {} {}".format(event.type, event.type, event.type))
