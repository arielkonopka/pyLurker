import pygame
import random
import sys
import time
import pygame
from pygame import FULLSCREEN


#Sky will be used for the background
class sky:
    layers = None
    displaySize = None
    displayOffset = None
    displayFrame = False

    def __init__(self, size, offset=(0, 0), frame=False):
        self.displayFrame = frame
        self.displaySize = size
        self.displayOffset = offset
        self.layers=[[random.randint(0,size[0]) for i in range(size[0])] for j in range(0,4) ]

    def iterate(self, y):
        for plus in range(0,4):
            self.layers[plus][y] = (self.layers[plus][y] + 2+ plus ) % self.displaySize[0]

    def changeOffset(self,_offset):
        self.displayOffset=_offset

    def draw(self, _scrHndl):

        for y in range((self.displaySize[1]-1)):
            for x in range(0,4):
                pygame.draw.circle(_scrHndl, (90+(x+1)*40, 90+(x+1)*40, 90+(x+1)*30),
                               (self.layers[x][y] + self.displayOffset[0], y + self.displayOffset[1]), 1+x)
            self.iterate(y)
        if self.displayFrame:
            pygame.draw.line(_scrHndl, [50, 50, 255],
                             (self.displayOffset[0] - 2, self.displayOffset[1] - 2),
                             (self.displayOffset[0] - 2,
                              self.displayOffset[1] + self.displaySize[1] + 2), 4)
            pygame.draw.line(_scrHndl, [50, 50, 255],
                             (self.displayOffset[0] - 2, self.displayOffset[1] - 2),
                             (self.displayOffset[0] + self.displaySize[0],
                              self.displayOffset[1] - 2), 4)
            pygame.draw.line(_scrHndl, [50, 50, 255],
                             (self.displayOffset[0] + self.displaySize[0], self.displayOffset[1] + self.displaySize[1]+2),
                             (self.displayOffset[0] - 2,
                              self.displayOffset[1] + self.displaySize[1] + 2), 4)
            pygame.draw.line(_scrHndl, [50, 50, 255],
                             (self.displayOffset[0] + self.displaySize[0], self.displayOffset[1] + self.displaySize[1]+2),
                             (self.displayOffset[0] + self.displaySize[0],
                              self.displayOffset[1] + 2), 4)
