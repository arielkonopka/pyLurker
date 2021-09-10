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

    def getLevelObject(self,levelNo,xPos,yPos):
        '''
        This method will help with translating a marker to a boardElement
        '''
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
            # we got lists here, so we could easily calculate the subtype
        translator={board.PLAYER:['@'],
                    board.MONSTER:['M','m','N','n'],
                    board.WALL:['#','%','W','w'],
                    board.BOX:['*','<'],
                    board.AMMO:['!'],
                    board.BOMB:['~','`'],
                    board.KEY:['&','+'],
                    board.TOKEN:['$'],
                    board.DOOR:['D','d'],
                    board.EXIT:['X'],
                    board.MAGNET:['a'], # we fix the direction with corrections, if necessary, default is 0 which is left
                    board.TANK:['}'],   # we fix the directions with corrections, if necessary, default is 0 which is left
                    board.TURRET:['>'], # we fix the direction with the corrections, if necessary, default is 0 which is left
                    board.TELEPORT:['T','t','1','2','3','4','5','6','7','8','9','0']
        }
        for eClass in translator:
            subtype=0
            for mrks in translator.get(eClass):
                if marker==mrks:
                    return self.applyCorrections((eClass,0,subtype,False),level,(xPos,yPos))
                subtype+=1
        return(board.EMPTYELEMENT,0,0,False)
        

    def applyCorrections(self,element,level,position):
        corrections=level['LevelObjectCorrections']
        if corrections==None:
            return element
        for cor in corrections:
            if position[0]==cor[0] and position[1]==cor[1]:
                element[1]=cor[2]
                element[2]=cor[3]
                element[3]=cor[4]
                break
        return element



   


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