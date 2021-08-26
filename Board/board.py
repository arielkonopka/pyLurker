from LevelManager import *
import random
# board member types

EMPTYELEMENT = 0
PLAYER = -1
WALL = 1
BOX = 10

# blasters and lasers are done with subtype and rotatable fields
TURRET = 20

MAGNET = 30
TANK = 40

TOKEN=120
BOMB = 50
AMMO = 60
MISSILE=110
KEY = 70
DOOR = 80
TELEPORT = 90
MONSTER = 100
EXIT = 130

_DEFAULTAMMOUNT = 12

_PortingTime = 8

_MOD1=1
_MOD2=2
_mod3=4

_LEFT = 0
_UP = 1
_RIGHT = 2
_DOWN = 3
_NEUTRAL = 4

class boardMember():
    justTurned=False
    steppingOn=None #default empty object is the object the playaye stands on
    steppable=False
    instanceNo=0
    players=-1
    canShoot=0
    killed=0  #killed counter - used to detect if element is killed and for die animation
    type = EMPTYELEMENT
    direction = 0
    animPhase = 0
    moved = 0
    rotated = 0
    shot = 0
    shooting:int = 0
    changed=True
    canShoot = False
    movable = False
    killable = False
    magnetic = False
    canCollect = False
    objCollection:[] = []
    subType = 0
    rotatable = False
    destructable = True
    collectible = False
    #teleporting in and out 
    inPorting = 0
    outPorting = 0
    canKill=False

    #we need a 'smart' support for this
    #when the object is created, it is in changed state - which means it would be rendered
    #but when nothing is happening, the object should be set to False
    changed=True 
    
    __cntA=0
    __cntB=0
    __cntC=5
    animSpeed=4
    # constructor for the board member class
    # depending on the type, there will be different routing called to initialize all the parameters

    def __init__(self, type=EMPTYELEMENT, direction=_UP, subType=0, rotatable=False):
        # Elements to be initialized
        switch ={EMPTYELEMENT: self.empty,
                  PLAYER: self.player,
                  WALL: self.wall,
                  BOX: self.box,
                  AMMO: self.ammo,
                  KEY: self.key,
                  DOOR: self.door,
                  TURRET: self.turret,
                  TANK: self.tank,
                  BOMB: self.bomb,
                  TELEPORT: self.teleport,
                  MAGNET: self.magnet,
                  MONSTER: self.monster,
                  MISSILE: self.missile,
                  TOKEN:self.token,
                  EXIT:self.exit
                 }
        # basic initialization like type, subtype, direction and if the object can rotate, that is to create less object types for stuff like
        # turrets, tanks, magnets and other multilied types like enemies
        self.type = type
        self.subType = subType
        self.direction = direction
        self.rotatable = rotatable
        self.changed=True
        elementInit = switch.get(self.type)
        elementInit()
    


    def tick(self):
        self.__cntA=(self.__cntA+1) % self.animSpeed
        if self.__cntA==0:
            if self.killed>0:
                self.killed-=1
            if self.inPorting:
                self.inPorting-=1
                self.changed=True
            if self.outPorting>0:
                self.outPorting-=1
                self.changed=True
            if self.type!=PLAYER:
                self.animPhase=(self.animPhase+1) % 65535
                self.changed=True
               
        if self.shooting:
            if self.shooting>0:
                self.shooting-=1
        if self.shot>0:
            self.shot-=1
        if self.rotated>0:
            self.rotated-=1
        if self.moved>0:
            self.moved-=1

            
    def exit(self):
        self.killable=False
        self.destructable=True
        self.subType=0
        self.collectible=False
        self.movable=True

    def token(self):
        self.collectible=True


    # we now define standard settings for each object type
    def empty(self):
        self.steppable=True
        pass

    # we could merge the settings for wall and empty object, as they share almost all the same qualities
    def wall(self):
        self.destructable=False
        self.killable=False
        pass

    def door(self):
        self.destructable =True

    #it is similar to door, can be destroyed in an exlosion, but cannot be shot
    def teleport(self):
        self.destructable=True
        self.steppable=False
        self.killable=False
        self.collectible=False

    def missile(self):
        self.movable=True
        self.destructable=True
    #now magnet is like a wall, cannot be destroyed and so on
    def magnet(self):
        pass

    def bomb(self):
        self.killable=True
        self.destructable=True
        self.movable=True

    def turret(self):
        self.canShoot=True
        self.destructable =True
     
    def monster(self):
        self.canKill=True
        self.destructable=True
        self.killable=True


    def tank(self):
        # we inherit some setup from the turret
        self.turret()
        self.movable =True

    def player(self):
        self.movable =True
        self.killable =True
        self.magnetic =True
        self.canCollect =True
        self.objCollection =None
        boardMember.players+=1
        self.instanceNo=boardMember.players
    def box(self):
       # if self.subType==0:
       #     self.steppable=True
        self.movable =True
        self.destructable =True

    def ammo(self):
        self.destructable =True
        self.killable =True
        self.magnetic =True
        self.collectible=True
        self.shots =_DEFAULTAMMOUNT

    def key(self):
        self.destructable =True
        self.magnetic =True
        self.collectible=True





class board():
    playground:boardMember =None
    smell=None
    players=0
    sizeX =0
    sizeY =0
    exitAchived=False
    exitReady=False
    def __init__(self ,size):
        self.playground =[[boardMember() for i in range(0 ,size[1])] for j in range(0 ,size[0])]
        #the smells matrix, objects are tuples with type and strength of the smell
        self.smell=[[(0,0) for i in range(0 ,size[1])] for j in range(0 ,size[0])]
        self.sizeY =size[1]
        self.sizeX =size[0]
        for x in range(0,size[0]):
            for y in range(0,size[1]):
                self.playground[x][y].steppingOn=boardMember()
        boardMember.players=-1
        boardMember.instanceNo=-1
        

        
    def findNeighboors(self,x,y,result=None,theType=None ):
        """
        Return close neighborhood of the element, you can specify the type of objects you want to fetch, 
        the first element is always the element itself
        """
        if result==None:
            result=[(x,y,self.playground[x][y])]
        if x>0 and (self.playground[x-1][y].type==theType or theType==None):
            result.append((x-1,y,self.playground[x-1][y]))
        if y>0 and (self.playground[x][y-1].type==theType or theType==None):
            result.append((x,y-1,self.playground[x][y-1]))
        if y<self.sizeY-1 and (self.playground[x][y+1].type==theType or theType==None):
            result.append((x,y+1,self.playground[x][y+1]))
        if x<self.sizeX-1 and (self.playground[x+1][y].type==theType or theType==None):
            result.append((x+1,y,self.playground[x+1][y]))
        return result            


    def findNearestPlayer(self,x,y,iters=4):
        """ 
            Unlike the function's name, the routine will not find the nearest player, but it will find a player 
            using recurrent search, all steppable objects are ignored, no checks, if a field was already visited
        """
        
    
        if iters<0:
            return None
        neighs=self.findNeighboors(x,y)
        for cnt in range(1,len(neighs)):
            
            if neighs[cnt][2].type==PLAYER:
                    return (neighs[cnt][0],neighs[cnt][1])
            #we do not include walls, so walls in the vew will dramatically inpair the vision
            if neighs[cnt][2].steppable==False:
                continue
            player=self.findNearestPlayer(neighs[cnt][0],neighs[cnt][1],iters-1)
            if player!=None:
                return player
        return None

    def findNearPlayer(self,x,y,size,pType=PLAYER):
        """
        iterative function that searches for the player in the close neighboorhood
        """
        startX=x-size
        startY=y-size
        if startY<0:
            startY=0
        if startX<0:
            startX=0
        endX=x+size
        endY=y+size
        if endX>self.sizeX:
            endX=self.sizeX    
        if endY>self.sizeY:
            endY=self.sizeY;
        for x in range(startX,endX):
            for y in range(startY,endY):
                if self.playground[x][y].type==pType:
                    return (x,y)
        return None
    


#we take a tuple and set it as a board member
    def setBoardMember(self,x,y,member):
        """
        That is needed for loading of the level data, this is used to create a board member
        """
        if not member:
            return
        self.playground[x][y]=boardMember(member[0],member[1],member[2],member[3])
        self.playground[x][y].steppingOn=boardMember(EMPTYELEMENT)



    def iterateMech(self,command):
        """
        Main game mechanics routine
        """
        # here we define methods that should be run on different elements
        switch ={EMPTYELEMENT :self.empty ,
                  PLAYER :self.player ,
                  WALL :self.wall ,
                  BOX :self.box ,
                  AMMO :self.ammo ,
                  KEY :self.key ,
                  DOOR :self.door ,
                  TURRET :self.turret ,
                  TANK :self.tank,
                  BOMB:self.bomb,
                  TELEPORT:self.teleport,
                  MAGNET:self.magnet,
                  MONSTER:self.monster,
                  TOKEN:self.token,
                  MISSILE:self.missile,
                  EXIT:self.exit
                
                 }
  #      print(self.smell)         
        # here we launch all the methods that are supposed to be run during mechanics update
        for x in range(0,self.sizeX):
            for y in range(0,self.sizeY):
                self.playground[x][y].tick()
        for x in range(0 ,self.sizeX):
            for y in range(0 ,self.sizeY):
#decrease the smell of objects. Do not worry, the objects that smell will create new signal
#therefore the old signal will fade away automagically
                if self.smell[x][y][1]>1:
                    self.smell[x][y]=(self.smell[x][y][0],self.smell[x][y][1]-1)
                elif self.smell[x][y][1]==1:
                    self.smell[x][y]=(0,0)
      #if the object recently moved, we do not move it again for a while, but decrease the counter
                if self.playground[x][y].moved==0 and self.playground[x][y].outPorting==0 and self.playground[x][y].inPorting==0 and self.playground[x][y].killed==0:    
                    elementMech =switch.get(self.playground[x][y].type)
                    elementMech(x, y,command)
        #take care of all these counters
                if self.playground[x][y].outPorting==1 or self.playground[x][y].killed==1: #last frame, the object must go
                    self.restoreObject(x,y)
                    self.playground[x][y].changed=True
                    self.playground[x][y].outPorting=0
                    self.playground[x][y].killed=0

                                



#here we got the methods for board mechanics
#every method will control different object type
    def empty(self, x, y,cmd):
        pass


    def exit(self,x,y,cmd):
        if self.exitReady==True and self.playground[x][y].subType==0:
            self.playground[x][y].subType=1
            self.playground[x][y].steppable=False
            self.playground[x][y].destructable=False



#def createOverObject(self,x,y,objectType,direction,subType=0):
    def performTeleport(self,x,y,x1,y1):
        """
        Perform the teleportation of objects, no checking anything
        """
        step=self.playground[x1][y1]
        self.playground[x1][y1]=boardMember(PLAYER)

        self.playground[x1][y1].direction=self.playground[x][y].direction
        #we keep robot instance id, that will help us keep the controller
        self.playground[x1][y1].instanceNo=self.playground[x][y].instanceNo
        #we want to take the keys and other collectibles with us
        self.playground[x1][y1].objCollection=self.playground[x][y].objCollection

        self.playground[x1][y1].steppingOn=step
        self.playground[x1][y1].inPorting=_PortingTime
        self.playground[x][y].outPorting=_PortingTime

    def isNeighboorhoodSteppable(self,x,y):
        """
        This method will determine if the close neighborhood is steppable
        """
        neigh=self.findNeighboors(x,y)
        for n in neigh:
            if n[2].steppable==True:
                return True
        return False

    def findNextTeleport(self,x,y):
        """
        find next teleportation defice
        """
        lookedType=self.playground[x][y].subType
        if x>0:
            for nx in range(x+1,self.sizeX):
                if self.playground[nx][y].type==TELEPORT and self.playground[nx][y].subType==lookedType and self.isNeighboorhoodSteppable(nx,y):
                    return (nx,y)
            y+=1
        for ny in range(y,self.sizeY):
            for nx in range(0,self.sizeX):
                if self.playground[nx][ny].type==TELEPORT and self.playground[nx][ny].subType==lookedType and self.isNeighboorhoodSteppable(nx,ny):
                    return (nx,ny)
        #ok, start over to find the teleports that were before            
        for ny in range(0,y+1):
            for nx in range(0,self.sizeX):
                if self.playground[nx][ny].type==TELEPORT and self.playground[nx][ny].subType==lookedType and self.isNeighboorhoodSteppable(nx,ny):
                    return (nx,ny)
        return None # this should not happen in real life


    def teleportObject(self,x,y,x1,y1):
        """
        teleport object at x,y with a teleport at x1,y1, we find a teleport that is after or below, then we look from the start
        """

        nextTel=self.findNextTeleport(x1,y1)
        if nextTel==None:
            self.playground[x][y].inPorting=_PortingTime
            return False 
        neigh=self.findNeighboors(nextTel[0],nextTel[1],None,EMPTYELEMENT)
        choice=random.randint(1,len(neigh)-1)
        self.performTeleport(x,y,neigh[choice][0],neigh[choice][1])
            

        








#collect an object
    def collect(self,fromPos,toPos):
        if self.playground[fromPos[0]][fromPos[1]].objCollection:
            self.playground[fromPos[0]][fromPos[1]].objCollection.append(self.playground[toPos[0]][toPos[1]])
        else:
             self.playground[fromPos[0]][fromPos[1]].objCollection= [self.playground[toPos[0]][toPos[1]]]
        self.playground[toPos[0]][toPos[1]]=boardMember(EMPTYELEMENT)
        self.playground[toPos[0]][toPos[1]].changed=True
        newCollection=[]
        ammo=0
        hits=True
        #normalize ammo thing
        while hits==True:
            hits=False
            for x in self.playground[fromPos[0]][fromPos[1]].objCollection:
                if x.type==AMMO:
                    hits=True
                    ammo=ammo+x.shots
                    self.playground[fromPos[0]][fromPos[1]].objCollection.remove(x)
        if ammo>0:
            am=boardMember(AMMO)
            am.shots=ammo
            newCollection.append(am)
            self.playground[fromPos[0]][fromPos[1]].objCollection.append(am)  

    def moveObj(self,posFrom,posTo,direction,speed=3):
            self.playground[posFrom[0]][posFrom[1]],self.playground[posTo[0]][posTo[1]],self.playground[posTo[0]][posTo[1]].steppingOn=self.playground[posFrom[0]][posFrom[1]].steppingOn,self.playground[posFrom[0]][posFrom[1]],self.playground[posTo[0]][posTo[1]] 
            self.playground[posTo[0]][posTo[1]].moved=speed
            self.playground[posTo[0]][posTo[1]].justTurned=False
            self.playground[posTo[0]][posTo[1]].changed=True
            self.playground[posFrom[0]][posFrom[1]].changed=True
            self.playground[posTo[0]][posTo[1]].direction=direction
            self.playground[posTo[0]][posTo[1]].animPhase=(self.playground[posTo[0]][posTo[1]].animPhase+1) % 65535

    def pushObject(self,posFrom,posTo,posTo2,direction):
        self.moveObj(posTo,posTo2,direction)
        self.moveObj(posFrom,posTo,direction)

    def createOverObject(self,x,y,objectType,direction,subType=0):
        newMember=boardMember(objectType,direction)
        newMember.moved=2
        newMember.steppingOn,self.playground[x][y]=self.playground[x][y],newMember
        
    def restoreObject(self,x,y):
        if self.playground[x][y].steppingOn:
            self.playground[x][y]=self.playground[x][y].steppingOn
        else:    
            self.playground[x][y]=boardMember()

    def killObject(self,x,y,time_=4):
        if not self.playground[x][y].destructable:
            return
        if self.playground[x][y].killed>0: #element is already killed
            return 
       # if self.playground[x][y].type==EMPTYELEMENT:
       #     self.playground[x][y].type=BOX
        if self.playground[x][y].type==BOMB: 
            if self.playground[x][y].shot==0:
                self.playground[x][y].shot=6
        else:    
            self.playground[x][y].type=BOX
            #we set only killed, it should do the trick
            self.playground[x][y].killed=time_
            self.playground[x][y].collectible=False
            self.playground[x][y].movable=False
            self.playground[x][y].steppable=False
            self.playground[x][y].animPhase=0
            self.playground[x][y].changed=True

    def checkAmmo(self,x,y):
        if not self.playground[x][y].objCollection:
            return False
        for element in self.playground[x][y].objCollection:
            if element.type==AMMO and element.shots>0:
                return True
    def takeOneAmmo(self,x,y):
        if len(self.playground[x][y].objCollection)<=0:
            return False
        for element in self.playground[x][y].objCollection:
            if element.type==AMMO :
                if element.shots>1:
                    element.shots-=1
                    return True
                elif element.shots==1:
                    self.playground[x][y].objCollection.remove(element)
                    return True
        return False
    def shootObject(self,x,y):
        
        pass


#we do it in a function, so it would be easier to perform changes for other shooting objects
    def shootFromObject(self,x,y,cmdTuple):
        if self.playground[x][y].shooting!=0:
            return 
        self.playground[x][y].shoting=1080
        if self.checkAmmo(x,y)==True:
            self.takeOneAmmo(x,y)
        else:
            return    
        direction=cmdTuple[0]        
        if direction==_UP and y>0:
            if self.playground[x][y-1].steppable==True:
                self.createOverObject(x,y-1,MISSILE,_UP)
            elif self.playground[x][y-1].killable==True:
                self.killObject(x,y-1)    
            #shoot up
        elif direction==_DOWN and y<self.sizeY-1:
            if self.playground[x][y+1].steppable==True:
                self.createOverObject(x,y+1,MISSILE,_DOWN)
            elif self.playground[x][y+1].killable==True:
                self.killObject(x,y+1)    

            #shoot down
        elif direction==_LEFT and x>0:
            if self.playground[x-1][y].steppable==True:
                self.createOverObject(x-1,y,MISSILE,_LEFT)
            elif self.playground[x-1][y].killable==True:
                self.killObject(x-1,y)    

            #shoot Left
        elif direction==_RIGHT and x<self.sizeX-1:
            if self.playground[x+1][y].steppable==True:
                self.createOverObject(x+1,y,MISSILE,_RIGHT)
            elif self.playground[x+1][y].killable==True:
                self.killObject(x+1,y)    
            

    def missile(self,x,y,cmd_):
        if self.playground[x][y].movable==False:
            return

        myself=self.playground[x][y]
        target=None
        targetX=x
        targetY=y
        if myself.direction==_UP and y>0:
            targetY=y-1
        elif myself.direction==_DOWN and y<self.sizeY-1:
            targetY=y+1
        elif myself.direction==_LEFT and x>0:
            targetX=x-1
        elif myself.direction==_RIGHT and x<self.sizeX-1:
            targetX=x+1
        target=self.playground[targetX][targetY]
        if target.steppable==True:
            self.moveObj((x,y),(targetX,targetY),myself.direction)
        elif target.killable==True:
            self.restoreObject(x,y)
            self.killObject(targetX,targetY)
        else:
            self.killObject(x,y)
    def checkKeys(self,x,y,type=0):
        if self.playground[x][y].objCollection:
            for obj in self.playground[x][y].objCollection:
                if obj.type==KEY and obj.subType==type:
                    return True
    
    def openDoor(self,x,y,x1,y1):
        if not self.playground[x][y].objCollection:
            return False
        if self.playground[x][y].inPorting>0 or self.playground[x][y].killed>0:
            return False
        type_= self.playground[x1][y1].subType   
        for obj in self.playground[x][y].objCollection:
            if obj.type==KEY and obj.subType==type_:
                self.playground[x][y].objCollection.remove(obj)
                self.killObject(x1,y1,2)
                return True
        return False
    
    def monsterPlayerDetected(self,x,y,player):
        px=player[0]
        py=player[1]
        coin=random.randint(0,1)
        if coin==0:
            if px>x:
            #move right
                if self.playground[x+1][y].steppable==True:
                    self.moveObj((x,y),(x+1,y),_RIGHT,4)
                    return True
            if px<x:
            #move Left
                if self.playground[x-1][y].steppable==True:
                    self.moveObj((x,y),(x-1,y),_LEFT,4)
                    return True
            if py>y:
                if self.playground[x][y+1].steppable==True:
                    self.moveObj((x,y),(x,y+1),_DOWN,4)
                    return True
            if py<y:
                if self.playground[x][y-1].steppable==True:
                    self.moveObj((x,y),(x,y-1),_UP,4)
                    return True
        else:
            if py>y:
                if self.playground[x][y+1].steppable==True:
                    self.moveObj((x,y),(x,y+1),_DOWN,4)
                    return True
            if py<y:
                if self.playground[x][y-1].steppable==True:
                    self.moveObj((x,y),(x,y-1),_UP,4)
                    return True
            if px>x:
            #move right
                if self.playground[x+1][y].steppable==True:
                    self.moveObj((x,y),(x+1,y),_RIGHT,4)
                    return True
            if px<x:
            #move Left
                if self.playground[x-1][y].steppable==True:
                    self.moveObj((x,y),(x-1,y),_LEFT)
                    return True

    
    def monsterRandomTurn(self,x,y):
        direction=self.playground[x][y].direction
        coin=random.randint(0,1)
        if coin==0:
            if direction==_UP:
                direction=_RIGHT
            elif direction==_DOWN:
                direction=_LEFT
            elif direction==_LEFT:
                direction=_UP
            elif direction==_RIGHT:
                direction=_DOWN
        else:
            if direction==_UP:
                direction=_LEFT
            elif direction==_DOWN:
                direction=_RIGHT
            elif direction==_LEFT:
                direction=_DOWN
            elif direction==_RIGHT:
                direction=_UP
        self.playground[x][y].direction=direction
        self.playground[x][y].moved=2
        self.playground[x][y].justTurned=True

    def monster(self,x,y,cmd_):
        detectedSmell=self.smell[x][y]
        self.smell[x][y]=(MONSTER,100)
        if self.playground[x][y].subType<2:
            self.monsterVision(x,y,cmd_,detectedSmell)

        

#here we will contain the monster logic
    def monsterVision(self,x,y,cmd_,detectedSmell=(0,0)):
        """
        This is a routine of a monster that can see, there are two types of mosters like that
        one sees through the walls and other objects
        the other cannot see through the wall
        """
        if self.playground[x][y].subType==0:
            player=self.findNearPlayer(x,y,6,PLAYER)
        else:
            player=self.findNearestPlayer(x,y,6)
        if player:
            moved=self.monsterPlayerDetected(x,y,player)
            if moved==True:
                return
#        neighs=self.findNeighboors(x,y)
#        for e in neighs:
#            if e[2].type==PLAYER:
#                self.killObject(e[0],e[1])
        coin=random.randint(0,10)
        direction=self.playground[x][y].direction
        if direction==_UP:
            if coin>6 and self.playground[x][y].justTurned==False:
                if y>0 and y<self.sizeY-1 and x>0 and x<self.sizeX-1:
                    if self.playground[x-1][y+1].steppable==False and self.playground[x+1][y+1].steppable==False and (self.playground[x-1][y].steppable==True or self.playground[x+1][y].steppable==True):
                        self.monsterRandomTurn(x,y)
                        return     
            if y>0 and self.playground[x][y-1].steppable==True:
                self.moveObj((x,y),(x,y-1),_UP,6)
            else:
                #we can't go up anymore
               self.monsterRandomTurn(x,y)
        if direction==_DOWN:
            if coin>6 and y>0 and y<self.sizeY-1 and x>0 and x<self.sizeX-1 and self.playground[x][y].justTurned==False:
                if self.playground[x-1][y-1].steppable==False and self.playground[x+1][y-1].steppable==False and (self.playground[x-1][y].steppable==True or self.playground[x+1][y].steppable==True):
                    self.monsterRandomTurn(x,y)
                    return     

            if y<self.sizeY-1 and self.playground[x][y+1].steppable==True:
                self.moveObj((x,y),(x,y+1),_DOWN,6)
            else:
                #we can't go up anymore
               self.monsterRandomTurn(x,y)
        if direction==_LEFT:
            if coin>6 and y>0 and y<self.sizeY-1 and x>0 and x<self.sizeX-1 and self.playground[x][y].justTurned==False:
                if self.playground[x+1][y-1].steppable==False and self.playground[x+1][y+1].steppable==False and (self.playground[x][y-1].steppable==True or self.playground[x][y+1].steppable==True):
                    self.monsterRandomTurn(x,y)
                    return     

            if x>0 and self.playground[x-1][y].steppable==True:
                self.moveObj((x,y),(x-1,y),_LEFT,6)
            else:
                #we can't go up anymore
               self.monsterRandomTurn(x,y)
        if direction==_RIGHT:
            if coin>6 and y>0 and y<self.sizeY-1 and x>0 and x<self.sizeX-1 and self.playground[x][y].justTurned==False:
                if self.playground[x-1][y-1].steppable==False and self.playground[x-1][y+1].steppable==False and (self.playground[x][y-1].steppable==True or self.playground[x][y+1].steppable==True):
                 self.monsterRandomTurn(x,y)
                 return     
            if x<self.sizeX-1 and self.playground[x+1][y].steppable==True:
                self.moveObj((x,y),(x+1,y),_RIGHT,6)
            else:
                #we can't go up anymore
               self.monsterRandomTurn(x,y)
            




    def player(self, x, y,cmd_):
        self.smell[x][y]=(PLAYER,100)
        neigh=self.findNeighboors(x,y)
        for n in neigh:
            if n[2].canKill==True:
                self.killObject(x,y)
                return
        if not cmd_:
            return
        if not cmd_[self.playground[x][y].instanceNo]:
            return
        cmdTupple=cmd_[self.playground[x][y].instanceNo]        
        print("{} {}".format(cmdTupple[1],self.playground[x][y].instanceNo+1))
        cmd=cmdTupple[0]
        if cmdTupple[1]>0 and self.playground[x][y].instanceNo +1>0:
            print(cmdTupple)
            if self.playground[x][y].shooting==0:
                self.shootFromObject(x,y,cmdTupple)
                self.playground[x][y].shooting=15
                self.playground[x][y].moved=5
            return
        #teleportation
        if self.playground[x][y].outPorting:
            self.playground[x][y].moved,self.playground[x][y].outPorting=self.playground[x][y].outPorting,self.playground[x][y].outPorting-1
            self.playground[x][y].subType=1

            return
        elif self.playground[x][y].inPorting:
            self.playground[x][y].moved,self.playground[x][y].inPorting=self.playground[x][y].inPorting,self.playground[x][y].inPorting-1
            self.playground[x][y].subType=2
            return
        self.playground[x][y].subType=0
        if cmd==_UP and y>0:
            if self.playground[x][y-1].steppable==True:
                self.moveObj((x,y),(x,y-1),cmd)
            elif self.playground[x][y-1].type==TELEPORT:
                self.teleportObject(x,y,x,y-1)
            elif self.playground[x][y-1].type==EXIT and self.playground[x][y-1].subType==1:
                self.collect((x,y-1),(x,y))
                self.exitAchived=True
            elif self.playground[x][y-1].movable==True and y>1 and self.playground[x][y-2].steppable==True:
                self.pushObject((x,y),(x,y-1),(x,y-2),_UP)
            elif self.playground[x][y-1].collectible==True:
                    self.collect((x,y),(x,y-1))
                    self.moveObj((x,y),(x,y-1),cmd)
            elif y>1 and self.playground[x][y-1].type==DOOR:
                self.openDoor(x,y,x,y-1)

        if cmd==_DOWN and y<self.sizeY-1:
          #  print(">{}".format(cmd))
            if self.playground[x][y+1].steppable==True:
                self.moveObj((x,y),(x,y+1),_DOWN)
            elif self.playground[x][y+1].type==TELEPORT:
                self.teleportObject(x,y,x,y+1)
            elif self.playground[x][y+1].type==EXIT and self.playground[x][y+1].subType==1:
                self.collect((x,y+1),(x,y))
                self.exitAchived=True
            elif self.playground[x][y+1].movable==True and y<self.sizeY-2 and self.playground[x][y+2].steppable==True:
                self.pushObject((x,y),(x,y+1),(x,y+2),_DOWN)
            elif self.playground[x][y+1].collectible==True:
                self.collect((x,y),(x,y+1))
                self.moveObj((x,y),(x,y+1),_DOWN)
            if y<self.sizeY-2 and self.playground[x][y+1].type==DOOR:
                self.openDoor(x,y,x,y+1)
        if cmd==_LEFT and x>0:
            if  self.playground[x-1][y].steppable==True:
                self.moveObj((x,y),(x-1,y),_LEFT)
            elif self.playground[x-1][y].type==TELEPORT:
                self.teleportObject(x,y,x-1,y)
            elif self.playground[x-1][y].type==EXIT and self.playground[x-1][y].subType==1:
                self.collect((x-1,y),(x,y))
                self.exitAchived=True
            elif self.playground[x-1][y].movable==True and x>1 and self.playground[x-2][y].steppable==True:
                self.pushObject((x,y),(x-1,y),(x-2,y),_LEFT)
            elif self.playground[x-1][y].collectible==True:
                self.collect((x,y),(x-1,y))
                self.moveObj((x,y),(x-1,y),_LEFT)
            elif x>2 and self.playground[x-1][y].type==DOOR:
                self.openDoor(x,y,x-1,y)
        if cmd==_RIGHT and x<self.sizeX-1:
            if self.playground[x+1][y].steppable==True:
                self.moveObj((x,y),(x+1,y),_RIGHT)
            elif self.playground[x+1][y].type==TELEPORT:
                self.teleportObject(x,y,x+1,y)
            elif self.playground[x+1][y].type==EXIT and self.playground[x+1][y].subType==1:
                self.collect((x+1,y),(x,y))
                self.exitAchived=True
            elif self.playground[x+1][y].movable==True and x<self.sizeX-2 and self.playground[x+2][y].steppable==True:
                self.pushObject((x,y),(x+1,y),(x+2,y),_RIGHT)
            elif self.playground[x+1][y].collectible==True:
                self.collect((x,y),(x+1,y))
                self.moveObj((x,y),(x+1,y),_RIGHT)
            elif x<self.sizeX-2 and self.playground[x+1][y].type==DOOR:
                self.openDoor(x,y,x+1,y)    


      
      
    def token(self,x,y,cmd):
        pass
    def wall(self, x, y,cmd):
        pass

    def box(self, x, y,cmd):
        pass

    def ammo(self, x, y,cmd):
        pass

    def key(self, x, y,cmd):
        
        pass

    def door(self, x, y,cmd):
        pass

    def turret(self, x, y,cmd):
        pass

    def tank(self, x, y,cmd):
        pass

    def bomb(self, x, y,cmd):
        if self.playground[x][y].shot==1:
            self.playground[x][y].type=BOX
            self.killObject(x,y)
            if x>0 and self.playground[x-1][y].destructable==True:
                self.killObject(x-1,y)
                if y>0 and self.playground[x-1][y-1].destructable==True:
                    self.killObject(x-1,y-1)
                if y<self.sizeY-1 and self.playground[x-1][y+1].destructable==True:
                    self.killObject(x-1,y+1)                
            if x<self.sizeX+1:
                self.killObject(x+1,y)
                if y>0 and self.playground[x+1][y-1].destructable==True:
                    self.killObject(x+1,y-1)
                if y<self.sizeY-1 and self.playground[x+1][y+1].destructable==True:
                    self.killObject(x+1,y+1)                
            if y>0 and self.playground[x][y-1].destructable==True:
                self.killObject(x,y-1)
            if y<self.sizeY-1 and self.playground[x][y+1].destructable==True:
                self.killObject(x,y+1)

        

    def teleport(self, x, y,cmd):
        pass

    def magnet(self, x, y,cmd):
        pass

 
    def getStats(self):
        ammo=0
        keys=0
        tokens=0
        tokensRemaining=0
        players=0
        for x in range(0,self.sizeX):
            for y in range(0,self.sizeY):                
                if self.playground[x][y].type==PLAYER:
                    players+=1
                    if self.playground[x][y].objCollection:
                        for z in self.playground[x][y].objCollection:
                    #    print(z)
                            if z.type==KEY:
                                keys+=1
                            if z.type==AMMO:
                                ammo+=z.shots
                            if z.type==TOKEN:
                                tokens+=1              
                elif self.playground[x][y].type==TOKEN:
                    tokensRemaining+=1
        if tokensRemaining==0:
            self.exitReady=True
        return (keys,ammo,tokens,tokensRemaining,players)                                                    



    def getChangedBoxes(self):
        result=[]
        for x in range(0,self.sizeX):
            for y in range(0,self.sizeY):
                elem=self.playground[x][y]
                if elem.direction==None:
                    elem.direction=_UP
                result.append((x,y,elem.type,elem.direction,elem.animPhase,elem.subType,self.smell[x][y],elem.outPorting,elem.inPorting,elem.killed))
        return result


if __name__=="__main__":
  pass