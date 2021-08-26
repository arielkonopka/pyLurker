import json
import os
import sys
from Board import board


class lvlManger():
    filename=''
    def __init__(self, fname):
        self.filename=fname
        self.loadLvlSet()

    def getLevel(self,levelNo):
        if levelNo > self.__levelSet['NumberOfLevels']:
            return None
        level = self.__levelSet['Levels'][levelNo]
        return level

    def getLevelsNo(self):
        if not self.__levelSet:
            return -1
        return self.__levelSet['NumberOfLevels']



    def getSize(self,levelNo):
        level=self.getLevel(levelNo)
        if level:
            return (level['Width'],level['Height'])
        else:
            return None

    def loadLvlSet(self,fname=None):
        if not fname:
            fname=self.filename
        with open(fname, 'r') as infile:
            self.__levelSet = json.load(infile)

    def saveLvlSet(self):
        pass

    def getLevelObject(self,levelNo,xPos, yPos):
        #do not try to process nulls
        if not self.__levelSet:
            return None
        level=self.getLevel(levelNo)
        #missing level data
        if not level:
            return None
        if len(level['LevelData'])-1<yPos:
            return None
        line = level['LevelData'][yPos]
        if len(line)-1<xPos:
            return None
        marker=line[xPos]
        switch={
            '@':self.makePlayer,
            'M':self.makeMonster,
            'm':self.makeMonster,
            'N':self.makeMonster,
            'n':self.makeMonster,
            '#':self.makeWall,
            '*':self.makeBox,
            ' ':self.makeEmpty,
            '<':self.makeBox,
            '!':self.makeAmmo,
            '%':self.makeWall,
            '~':self.makeBomb,
            '`':self.makeBomb,
            '&':self.makeKey,
            '$':self.makeToken,
            'D':self.makeDoor,
            'd':self.makeDoor,
            '7':self.makeKey,
            'X':self.makeExit,
            'T':self.makeTeleport,
            't':self.makeTeleport
            }
        objType=switch.get(marker)
        if objType:
            return objType(marker)
        else:
            return self.makeEmpty(None)   

    def makeTeleport(self,marker):
        if marker=='T':
            return(board.TELEPORT,0,0,False)
        else:
            return(board.TELEPORT,0,1,False)

    def makeMonster(self,marker):
        monsterList=['M','m','N','n']
        stype=monsterList.index(marker)
        print("{}->{}".format("Monster",stype))
        return(board.MONSTER,0,stype,False)

    def makeExit(self,marker):
        """
            in This case subtype will indicate if the exit is open or not
        """
        return(board.EXIT,0,0,False)

    def makeDoor(self,marker):
        if marker=='D':
            return(board.DOOR,0,0,False) 
        else:
           # print("subtype1")
            return(board.DOOR,1,1,False)

    def makeToken(self,marker):
        return(board.TOKEN,0,0,False)

    def makeKey(self,marker):
        if marker=='&':
            return(board.KEY,0,0,False)
        else:
            return(board.KEY,0,1,False)

    def makeBomb(self,marker):
        switch={'~':0,'`':1}
#        print('bomb: {}'.format(switch.get(marker)))
        return(board.BOMB,0,switch.get(marker),False)

    def makePlayer(self,marker):
        return (board.PLAYER, 0, 0, False)
    def makeWall(self,marker):
        switch={'#':0,'%':1}
        return (board.WALL,switch.get(marker),switch.get(marker),False)
    def makeBox(self,marker):
        switch={'*':0,'<':1}
        return (board.BOX,0,switch.get(marker),False)
    def makeEmpty(self,marker):
        return(board.EMPTYELEMENT,0,0,False)
    def makeAmmo(self,marker):
        return(board.AMMO,0,0,False)












    def getRealSize(self,levelNo):
        level=self.getLevel(levelNo)
        if not level:
            return None
        return (len(level['LevelData'][0]),len(level['LevelData']))

    def createBoardObject(self,levelNo,skinName="GNU Robbo",skinDefFile='/home/c/PycharmProjects/pythonProject/Data/skins/skin.json'):
        self.loadLvlSet()
        level = self.getLevel(levelNo)
        size = self.getSize(levelNo)
        MyPlayground = board.board(size)
        # we fill the objects in the
        for y in range(0, size[1]):
            for x in range(0, size[0]):
                lO = self.getLevelObject(levelNo, x, y)
                MyPlayground.setBoardMember(x, y, lO)
        return MyPlayground


if __name__=='__main__':
    myLevel=lvlManger('/home/c/PycharmProjects/pythonProject/LevelData/Levels.json')
    print(os.getcwd())
    myLevel.loadLvlSet()
    level=myLevel.getLevel(0)
    size=myLevel.getRealSize(0)
    if not size:
        sys.exit()

    for y in range(0,size[1]):
        line=level['LevelData'][y]
        for x in range(0,len(line)):
            print(line[x],end='')
        print('')

    print(myLevel.getRealSize(0))
    print(myLevel.getLevelObject(0,0,0))