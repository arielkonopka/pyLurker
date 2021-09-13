from LevelManager import *
import random
'''
This file contains two classes and handfull of constant values.
The classes are related to the game play board and are:
* boardMember
* board



'''


# board member types



EMPTYELEMENT = 0
PLAYER = -1
WALL = 1
BOX = 10

# blasters and lasers are done with subtype and rotatable fields
TURRET = 20
# magnetic Field generator
MAGNET = 30
# moving and shooting objects
TANK = 40
# tokens to be collected
TOKEN=120
REMAINS =121
BOMB = 50
AMMO = 60
MISSILE=110
# different subtipes of keys match different subtypes of doors
KEY = 70
DOOR = 80
# different subtypes of teleports connect to different type of a teleport.
TELEPORT = 90
# monsters all classes
MONSTER = 100
# exit, subclass 0 is inactive, subclass 1 is active
EXIT = 130
# this a class of objects containing other objects. for them the collect routine must be adjusted
STASH =140
SOFTWALL = 150
# constant values
_DEFAULTAMMOUNT = 12

_PortingTime = 8
_KillingTime = 8

_MOD1=1
_MOD2=2
_mod3=4

_LEFT = 0
_UP = 1
_RIGHT = 2
_DOWN = 3
_ExitOpen=1



class boardMember():
    '''
    boardMember class
        This is a class that let's using board members easy. Some methods are built in like:
        * various timers support
        * kill, restore, demolish methods

        Every object in the game board is a boardMember object     
    '''

    justTurned=False
    steppingOn=None #default empty object is the object the playaye stands on
    steppable=False
    instanceNo=0
    tokens=0
    players=-1
    playerNo=0
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
    destructable = False
    collectible = False
    #teleporting in and out 
    inPorting = 0
    outPorting = 0
    tokensCanGo=False
    canKill=False
    canTeleport=False
    canOpenDoors=False
    canPushObjects=False
    notifications=None
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
                  EXIT:self.exit,
                  REMAINS:self.remains,
                  SOFTWALL:self.softWall
                 }
        # basic initialization like type, subtype, direction and if the object can rotate, that is to create less object types for stuff like
        # turrets, tanks, magnets and other multilied types like enemies
        self.type = type
        self.subType = subType
        self.direction = direction
        self.rotatable = rotatable
        self.changed=True
        self.canTeleport=False
        self.canOpenDoors=False
        self.canPushObjects=False
        self.steppable=False
        self.demolished=0
        self.destructable=True
        self.killed=0
        self.instanceNo=boardMember.instanceNo
        self.visited=False
        self.notifications=None
        boardMember.instanceNo+=1

        elementInit = switch.get(self.type)
        elementInit()


    def restoreElement(self,killed=False):
        #print("{}".format(self.type))
        if self.canCollect==True and self.objCollection and killed: #we got ourselves a collector that died
            self.type=REMAINS
            self.killable=True
            self.destructable=True
            self.movable=False
            self.collectible=True
            self.canKill=False
            self.subType=0
            self.changed=True
            self.steppable=False
            self.canTeleport=False
            return True
        if self.type==TOKEN and boardMember.tokensCanGo:
            boardMember.tokens-=1
        elif self.type==PLAYER:
            boardMember.players-=1

        if self.steppingOn==None: # empty? fix let's fix that first
            self.steppingOn=boardMember(EMPTYELEMENT)
            self.steppingOn.steppingOn=boardMember(EMPTYELEMENT)
        self.type=self.steppingOn.type
        self.killable=self.steppingOn.killable
        self.animPhase=0
        self.animSpeed=self.steppingOn.animSpeed
        self.canCollect=self.steppingOn.canCollect
        self.canKill=self.steppingOn.canKill
        self.canShoot=self.steppingOn.canShoot
        self.changed=True
        self.collectible=self.steppingOn.collectible
        self.destructable=self.steppingOn.destructable
        self.direction=self.steppingOn.direction
        self.instanceNo=self.steppingOn.instanceNo
        self.playerNo=self.playerNo
        self.inPorting=self.steppingOn.inPorting
        self.killable=self.steppingOn.killable
        self.killed=self.steppingOn.killed
        self.magnetic=self.steppingOn.magnetic
        self.movable=self.steppingOn.movable
        self.objCollection=self.steppingOn.objCollection
        self.outPorting=self.steppingOn.outPorting
        self.subType=self.steppingOn.subType
        self.canPushObjects=self.steppingOn.canPushObjects
        self.canOpenDoors=self.steppingOn.canOpenDoors
        self.canTeleport=self.steppingOn.canTeleport
        self.steppable=self.steppingOn.steppable                #since it was already stepped on, no reason to copy the value
        #end the last bot not least, we can have a list of stepped on objects, and we do not want to forget it
        self.notifications=self.steppingOn.notifications
        self.steppingOn=self.steppingOn.steppingOn
        



    def kill(self,time_=_KillingTime):
        if self.killed>0 or self.killable==False:
            return False
        if self.type==BOMB:
            return self.demolish()
        if self.shot==1 or self.type!=BOMB:
            self.movable=False
            self.canKill=False #this is very important, will the burning remains of an object be able to kill?
            self.canShoot=False
            self.canOpenDoors=False
            self.killed=time_
            self.collectible=False
            self.steppable=False
            self.animPhase=0
            self.changed=True
        return False

    
    def demolish(self,time_=_KillingTime):
        if self.destructable==False or self.demolished>0 or self.shot>1:
            return False
        if self.type==BOMB and self.shot==0:
            self.shot=4
            return True
        self.type=SOFTWALL
        self.killed=time_
        self.demolished=time_
        self.movable=False
        self.canKill=False #this is very important, will the burning remains of an object be able to kill?
        self.canShoot=False
        self.canOpenDoors=False
        self.collectible=False
        self.steppable=False
        self.animPhase=0
        self.changed=True
        return True

    def collect(self,anotherMember): #we use collect to reach the exit. This is probably wrong, as there should be reachTheExit() method. Still since player enters the exit, it is actually collected by it
                                     # it is worth noting, that we kinda break the rules here, but collectible player would cause issues. I think it could be cool, if the
                                     # inactive player could be kidnapped by a monster, that had to be shot to retrieve it, that would cause problem with player collecting it, we would have to extend the controls to drop the player :)
                                     # now we do not allow that, but still it can happen with subtype manipulations :)
        if self.canCollect==False and self.type!=EXIT and self.subType!=_ExitOpen:
            return anotherMember # sorry element is not allowed to collect
        if anotherMember.collectible==True or (anotherMember.type==PLAYER and self.type==EXIT and self.subType==_ExitOpen):
            if anotherMember.canCollect==True:
                #oh, it seems w got ourselvs a collector
                if self.objCollection:
                    self.objCollection=self.objCollection+anotherMember.objCollection
                else:
                    self.objCollection=anotherMember.objCollection
            else:
                if self.objCollection:
                    self.objCollection.append(anotherMember)
                else:
                    self.objCollection=[anotherMember]
            self.changed = True
            return anotherMember.steppingOn
        return anotherMember




    def tick(self):
        if self.steppingOn!=None and self.steppingOn.type!=EMPTYELEMENT:
            self.steppingOn.tick()
        self.visited=False
        self.__cntA=(self.__cntA+1) % self.animSpeed
        if self.__cntA==0:
            #get the demolished animation and state done
            if self.demolished>0:
                self.steppable=False
                self.demolished-=1
                self.changed=True
                if self.demolished==0:
                    self.restoreElement(True)       
            #get the killed animation and state done
            if self.killed>0: 
                self.steppable=False
                self.killed-=1
                if self.killed==0:
                    self.restoreElement(True)
                self.changed=True
            if self.inPorting:
                self.steppable=False
                self.inPorting-=1
                self.changed=True
            if self.outPorting>0:
                self.steppable=False
                self.outPorting-=1
                if self.outPorting==0:
                    self.restoreElement()
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

    def softWall(self):
        self.movable=False
        self.killable=True
        self.steppingOn=boardMember(EMPTYELEMENT)



    def remains(self):
        self.killable=False
        self.destructable=True
        self.movable=True
        self.canKill=False

    def exit(self):
        self.killable=False
        self.destructable=True
        self.subType=0
        self.collectible=False
        self.canCollect=True
        self.movable=True
        self.steppingOn=boardMember(EMPTYELEMENT)
        
    def token(self):
        self.collectible=True
        self.steppingOn=boardMember(EMPTYELEMENT)
        boardMember.tokens+=1

    # we now define standard settings for each object type
    def empty(self):
        self.steppable=True
        self.destructable=True
        pass

    # we could merge the settings for wall and empty object, as they share almost all the same qualities
    def wall(self):
        self.destructable=False
        self.killable=False
        pass

    def door(self):
        self.open=False
        self.destructable =True
        self.steppingOn=boardMember(EMPTYELEMENT)
    #it is similar to door, can be destroyed in an exlosion, but cannot be shot
    def teleport(self):
        self.destructable=True
        self.steppable=False
        self.killable=False
        self.collectible=False
        self.steppingOn=boardMember(EMPTYELEMENT)

    def missile(self):
        self.movable=True
        self.destructable=True
        self.killable=True
        self.steppingOn=boardMember(EMPTYELEMENT)
    #now magnet is like a wall, cannot be destroyed and so on
    def magnet(self):
        pass

    def bomb(self):
        self.killable=True
        self.destructable=True
        self.movable=True
        self.steppingOn=boardMember(EMPTYELEMENT)
    def turret(self):
        self.canShoot=True
        self.destructable =True
        self.steppingOn=boardMember(EMPTYELEMENT)

    def monster(self):
        self.canKill=True
        self.destructable=True
        self.killable=True
        self.movable=True
        self.steppingOn=boardMember(EMPTYELEMENT)
        self.canCollect=True
        if self.subType==1:
            self.canTeleport=True
    def tank(self):
        # we inherit some setup from the turret
        self.turret()
        self.movable =True
        self.steppingOn=boardMember(EMPTYELEMENT)

    def player(self):
        self.canTeleport=True
        self.canOpenDoors=True
        self.canPushObjects=True
        self.movable =True
        self.killable =True
        self.magnetic =True
        self.canCollect =True
        self.objCollection =None
        boardMember.players+=1
        self.playerNo=boardMember.players
        self.steppingOn=boardMember(EMPTYELEMENT)
        self.movable=True
    def box(self):
       # if self.subType==0:
        self.steppable=False
        self.movable =True
        self.destructable =True
        self.steppingOn=boardMember(EMPTYELEMENT)

    def ammo(self):
        self.destructable =True
        self.killable =True
        self.magnetic =True
        self.collectible=True
        self.shots =_DEFAULTAMMOUNT
        self.steppingOn=boardMember(EMPTYELEMENT)

    def key(self):
        self.destructable =True
        self.magnetic =True
        self.collectible=True
        self.steppingOn=boardMember(EMPTYELEMENT)





class board():
    playground:boardMember =[None]
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
        boardMember.playerNo=-1
        boardMember.tokens=0

    def iterateMech(self,command):
        """
        Main game mechanics routine,
        first we let boardMember object to maintain their timers and other stuff.
        The switch variable works as a switch statement, that can be used multiple times with different context.
        To add a new object support, just add metod to the class board and then an entry to the dictionary switch:
        YOURTHING:self.yourMethod
        Of course, add YOURTHING constant somewhere in the module and self.yourMethod should be defined as:
            def yourMethod(self, x, y,cmd,stpd=False)
        stpd is set to True if the object being called is currently being stepped on, refer to the object as self.playground[x][y].steppingOn
        Thanks to that you can support a link between the stepped on and the stepping objects
        """

        # here we launch all the methods that are supposed to be run during mechanics update on a boardMember level
        # like timers, animation phases, outporting and killing of objects, restoring objects
        # consider this a timer tick
        for x in range(0,self.sizeX):
            for y in range(0,self.sizeY):
                self.playground[x][y].tick()

        # here we define methods that should be run on different elements, we do not define anything that can be already standard
        # like if we want an pushable object that kills, we simply can create it and not worry about it's mechanics
        switch ={
                  PLAYER :self.player ,
                  BOMB:self.bomb,
                  MONSTER:self.monster,
                  MISSILE:self.missile,
                  EXIT:self.exit,
                  BOX:self.box
                
                 }
   
        # smell degrading, we want the smell of the objects to degrade with time
        for x in range(0 ,self.sizeX):
            for y in range(0 ,self.sizeY):
                # decrease the smell of objects. Do not worry, the objects that smell will create new signal
                # therefore the old signal will fade away automagically
                if self.smell[x][y][1]>1:
                    self.smell[x][y]=(self.smell[x][y][0],self.smell[x][y][1]-1)
                elif self.smell[x][y][1]==1:
                    self.smell[x][y]=(0,0)
                # if the object recently moved, is in or out porting or dying, we do not move it again for a while
                if self.playground[x][y].steppingOn!=None and self.playground[x][y].steppingOn.type!=EMPTYELEMENT:
                    elementMech =switch.get(self.playground[x][y].steppingOn.type)
                    if elementMech: 
                        elementMech(x, y,command,True)
                if self.playground[x][y].moved==0 and self.playground[x][y].outPorting==0 and self.playground[x][y].inPorting==0 and self.playground[x][y].killed==0:    
                    elementMech =switch.get(self.playground[x][y].type)
                    if elementMech:
                        elementMech(x, y,command,False)
        #take care of all these counters

        
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

    def fnp(self,x,y,iters=4):
        if iters<0:
            return None
        if self.playground[x][y].type==PLAYER:
            return (x,y)
        if self.playground[x][y].visited == True:
            return None
        player=None
        self.playground[x][y].visited = True
        neighs=self.findNeighboors(x,y)
        for neigh in neighs:
            if neigh[2].type==PLAYER:
                return (neigh[0],neigh[1])
        neighs.remove(neighs[0])
        for neigh in neighs:
            #we do not include walls, so walls in the vew will dramatically inpair the vision
            if  neigh[2].steppable==True:
                player=self.fnp(neigh[0],neigh[1],iters-1)
            if player!=None:
                return player
        return None


    def findNearestPlayer(self,x,y,iters=8):
        """ 
            Unlike the function's name, the routine will not find the nearest player, but it will find a player 
            using recurrent search, all steppable objects are ignored, no checks, if a field was already visited
        """
        for x1 in range(0,self.sizeX):
            for y1 in range(0,self.sizeY):
                self.playground[x1][y1].visited=False
        return self.fnp(x,y,iters)

    
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
    
    def createOverObject(self,x,y,objectType,direction,subType=0,rotatable=False):
        newMember=boardMember(objectType,direction,subType,rotatable)
        newMember.moved=2
        newMember.steppingOn,self.playground[x][y]=self.playground[x][y],newMember
        


#we take a tuple and set it as a board member
    def setBoardMember(self,x,y,member):
        """
        That is needed for loading of the level data, this is used to create a board member
        """
        if not member:
            return
        self.createOverObject(x,y,member[0],member[1],member[2],member[3])
       # self.playground[x][y]=boardMember(member[0],member[1],member[2],member[3])
       # self.playground[x][y].steppingOn=boardMember(EMPTYELEMENT)


#def createOverObject(self,x,y,objectType,direction,subType=0):
    def performTeleport(self,x,y,x1,y1):
        """
        Perform the teleportation of objects, no checking anything
        """
        step=self.playground[x1][y1]
        self.playground[x1][y1],self.playground[x][y]=self.playground[x][y],self.playground[x1][y1]
        self.playground[x1][y1].steppingOn, self.playground[x][y].steppingOn=self.playground[x][y].steppingOn,self.playground[x1][y1].steppingOn

        self.playground[x1][y1].inPorting=_PortingTime
        self.playground[x][y].outPorting=_PortingTime
        self.playground[x][y].type=BOX

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
        find next teleportation device
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
        ob=self.playground[fromPos[0]][fromPos[1]].collect(self.playground[toPos[0]][toPos[1]])
        if ob==None:
            ob=boardMember()
        self.playground[toPos[0]][toPos[1]]=ob

#I should create a method step on, but here it would make things a bit weird
    def moveObj(self,posFrom,posTo,direction,speed=3):
            self.playground[posFrom[0]][posFrom[1]],self.playground[posTo[0]][posTo[1]],self.playground[posTo[0]][posTo[1]].steppingOn=self.playground[posFrom[0]][posFrom[1]].steppingOn,self.playground[posFrom[0]][posFrom[1]],self.playground[posTo[0]][posTo[1]] 
            # This is an equivalent of same thing done in the restoreElement method, we could use it here, but we will not
            if self.playground[posTo[0]][posTo[1]]==None:
                self.playground[posTo[0]][posTo[1]]=boardMember()
            if self.playground[posFrom[0]][posFrom[1]]==None:
                self.playground[posFrom[0]][posFrom[1]]=boardMember()
            self.playground[posTo[0]][posTo[1]].moved=speed
            self.playground[posTo[0]][posTo[1]].justTurned=False
            self.playground[posTo[0]][posTo[1]].changed=True
            self.playground[posFrom[0]][posFrom[1]].changed=True
            self.playground[posTo[0]][posTo[1]].direction=direction
            self.playground[posTo[0]][posTo[1]].animPhase=(self.playground[posTo[0]][posTo[1]].animPhase+1) % 65535

    def pushObject(self,posFrom,posTo,posTo2,direction):

        self.moveObj(posTo,posTo2,direction)
        self.moveObj(posFrom,posTo,direction)


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
        self.playground[x][y].shoting=25
        if self.checkAmmo(x,y)==True:
            self.takeOneAmmo(x,y)
        else:
            return    
        direction=cmdTuple[0]        
        if direction==_UP and y>0:
            if self.playground[x][y-1].steppable==True:
                self.createOverObject(x,y-1,MISSILE,_UP)
            elif self.playground[x][y-1].killable==True:
                self.playground[x][y-1].kill()
            #shoot up
        elif direction==_DOWN and y<self.sizeY-1:
            if self.playground[x][y+1].steppable==True:
                self.createOverObject(x,y+1,MISSILE,_DOWN)
            elif self.playground[x][y+1].killable==True:
                self.playground[x][y+1].kill()   

            #shoot down
        elif direction==_LEFT and x>0:
            if self.playground[x-1][y].steppable==True:
                self.createOverObject(x-1,y,MISSILE,_LEFT)
            elif self.playground[x-1][y].killable==True:
                self.playground[x-1][y].kill()  

            #shoot Left
        elif direction==_RIGHT and x<self.sizeX-1:
            if self.playground[x+1][y].steppable==True:
                self.createOverObject(x+1,y,MISSILE,_RIGHT)
            elif self.playground[x+1][y].killable==True:
                self.playground[x+1][y].kill()    
            


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
           #     print("Open Doors")
                self.playground[x1][y1].open=True
                #self.playground[x1][y1].demolish() # doors are not killable and this trick would not work with them
                                                 # we could simply make them steppable, and make mosters not see through them
                                                 # thing to consider later 
                return True
        return False

    def walkObjectDirection(self,x,y,direction):
        """
        Walk an object in direction.
        This checks couple of variables, if object can move, teleport, open doors, push objects or collect other objects it checks it if is a player, and then it is allowed to go to the exit
        """
        if self.playground[x][y].movable==False:
            return False
        targetX=x
        targetY=y
        targetYY=y
        targetXX=x
        self.playground[x][y].direction=direction
        if direction==_UP and y>0:
            targetY=y-1
            if y>1:
                targetYY=y-2
        if direction==_DOWN and y<self.sizeY:
            targetY=y+1
            if y<self.sizeY-1:
                targetYY=y+2    
        if direction==_LEFT and x>0:
            targetX=x-1
            if x>1:
                targetXX=x-2
        if direction==_RIGHT and x<self.sizeX:
            targetX=x+1
            if x<self.sizeX-1:
                targetXX=x+2
        if targetX!=x or targetY!=y:
            if self.playground[targetX][targetY].steppable==True:
                self.moveObj((x,y),(targetX,targetY),direction)
                return True
            elif self.playground[targetX][targetY].type==TELEPORT and self.playground[x][y].canTeleport==True:
                self.teleportObject(x,y,targetX,targetY)
                return True
            elif self.playground[targetX][targetY].type==EXIT and self.playground[targetX][targetY].subType==1 and self.playground[x][y].type==PLAYER:
                self.collect((targetX,targetY),(x,y))
                self.exitAchived=True
                return True
            elif (targetXX!=x or targetYY!=y) and self.playground[targetX][targetY].movable==True and self.playground[targetXX][targetYY].steppable==True and self.playground[x][y].canPushObjects==True:
            #    print("pusz")
                self.pushObject((x,y),(targetX,targetY),(targetXX,targetYY),direction)
                return True
            elif self.playground[targetX][targetY].collectible==True and self.playground[x][y].canCollect==True:
                    self.collect((x,y),(targetX,targetY))
                    self.moveObj((x,y),(targetX,targetY),direction)
                    return True
            elif self.playground[targetX][targetY].type==DOOR and self.playground[x][y].canOpenDoors==True:
                if self.playground[targetX][targetY].open==True:
               #     print("Walk through doors")
                    self.moveObj((x,y),(targetX,targetY),direction)
                else:
                    self.openDoor(x,y,targetX,targetY)
                return True
        return False


    def monsterPlayerDetected(self,x,y,player):
        px=player[0]
        py=player[1]
        coin=random.randint(0,1)
        moved=False
        if coin==0:
            if px>x and moved==False:
            #move right
                moved=self.walkObjectDirection(x,y,_RIGHT)
            if px<x and moved==False:
            #move Left
                moved=self.walkObjectDirection(x,y,_LEFT)
            if py>y and moved==False:
                moved=self.walkObjectDirection(x,y,_DOWN)
            if py<y and moved==False:
                moved=self.walkObjectDirection(x,y,_UP)
        else:
            if py>y and moved==False:
                moved=self.walkObjectDirection(x,y,_DOWN)
            if py<y and moved==False:
                moved=self.walkObjectDirection(x,y,_UP)
            if px>x and moved==False:
                #move right
                moved=self.walkObjectDirection(x,y,_RIGHT)
            if px<x and moved==False:
                #move Left
                moved=self.walkObjectDirection(x,y,_LEFT)




  #  def monsterWalkDirection(self,x,y,directionList):
  #      for direction in directionList:
  #          if self.walkObjectDirection(x,y,direction)==True:
  #              return True
  #      return False

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
            player=self.findNearestPlayer(x,y,10)
        if player:
            moved=self.monsterPlayerDetected(x,y,player)
            if moved==True:
                return
        tst: bool=False
        tX:int = x
        tY:int = y
        if self.playground[x][y].direction==_DOWN:
            tX=x-1
            if tX<0:
                tX=x
        elif self.playground[x][y].direction==_UP:
            tX=x+1
            if tX>self.sizeX:
                tX=x
        elif self.playground[x][y].direction==_LEFT:
            tY=y-1
            if tY<0:
                tY=y
        elif self.playground[x][y].direction==_RIGHT:
            tY=y+1
            if tY>self.sizeY:
                tY=y
        tst:bool=False
         #if tX!=x or tY!=y:
        t=True
        for n in self.findNeighboors(x,y)[1:]:
            if n[2].steppable==False:
                t=False
                break
        if t==True:
            self.walkObjectDirection(x,y,self.playground[x][y].direction)
            return
        if self.playground[tX][tY].steppable==False:
            tst=self.walkObjectDirection(x,y,self.playground[x][y].direction)
            if not tst:
                    tst=self.walkObjectDirection(x, y, (self.playground[x][y].direction+3)%4)
            if tst:
                    return
        if not tst:
            for c in range(0,4):
                tst=self.walkObjectDirection(x,y,(self.playground[x][y].direction+1)%4)
             #   print(tst)
                if tst:
                    break
          #  tst = self.walkObjectDirection(x, y, (self.playground[x][y].direction+1)%4) #LURD
    
    def getStats(self):
        """
            This method collects basic statistics about the game, it will be used for gathering the stats
            it also calculates if the exit shouldd be reached, this of course can be overriden by the exit 
            control method
        """
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
        if tokens==boardMember.tokens:
            self.exitReady=True
        return (keys,ammo,tokens,boardMember.tokens,players)



    def getChangedBoxes(self):
        result=[]
        for x in range(0,self.sizeX):
            for y in range(0,self.sizeY):
                elem=self.playground[x][y]

            #    print(elem)
                if elem.direction==None:
                    elem.direction=_UP
                result.append((x,y,elem,self.smell[x][y]))
        return result

##################################################################################################

# here we got the methods for board mechanics
# every method will control different object type
    def exit(self,x,y,cmd,stpd=False):
        if stpd:
            return False
        if self.exitReady==True and self.playground[x][y].subType==0:
            self.playground[x][y].subType=_ExitOpen
            self.playground[x][y].steppable=False
            self.playground[x][y].destructable=False

    def box(self,x,y,cmd,stpd=False):
        if stpd:
            return False
        if self.playground[x][y].subType==0:
            return False # we are normal box, no additional logic neede
        objFound=None
        bFound=(0,0)
        closedLeft=False
        closedUp=False
        for nx in range(x-1,-1,-1):
            if self.playground[nx][y].steppable:
                continue
            if self.playground[nx][y].type==BOX and self.playground[nx][y].subType==1:
                bFound=(nx,y)
                closedLeft=True
                break
            if self.playground[nx][y].killable==True: 
                if objFound:
                    objFound.append(self.playground[nx][y])
                else:
                    objFound=[self.playground[nx][y]]
                continue
            else:
                break
        if closedLeft==True:
            self.playground[x][y].animSpeed=2
            self.playground[bFound[0]][bFound[1]].animSpeed=2
            if objFound:
                self.playground[x][y].direction=_LEFT
                self.playground[bFound[0]][bFound[1]].direction=_RIGHT
                for ob in objFound:
                    if ob.killed==0:
                        ob.kill()
                        #ob.demolish()

        
        else:
            self.playground[x][y].animSpeed=3
        objFound=None
        for ny in range(y-1,-1,-1):
            if self.playground[x][ny].steppable:
                continue
            if self.playground[x][ny].type==BOX and self.playground[x][ny].subType==1:
                closedUp=True
                bFound=(x,ny)
                break
            if self.playground[x][ny].killable==True:
                if objFound:
                    objFound.append(self.playground[x][ny])
                else:
                    objFound=[self.playground[x][ny]]
                continue
            else:
                break


        if closedUp:
            self.playground[x][y].animSpeed=2
            self.playground[bFound[0]][bFound[1]].animSpeed=2
            if objFound:
                self.playground[x][y].direction=_DOWN
                self.playground[bFound[0]][bFound[1]].direction=_UP
                for ob in objFound:
                    if ob.killed==0:
                        ob.kill()
                        #ob.demolish()
        else:
            self.playground[x][y].animSpeed=3
            #self.playground[bFound[0]][bFound[1]].animSpeed=3
        
        






    def monster(self,x,y,cmd_,stpd=False):
        if stpd:
            return False
        detectedSmell=self.smell[x][y]
        self.smell[x][y]=(MONSTER,100)
        if self.playground[x][y].subType<2:
            self.monsterVision(x,y,cmd_,detectedSmell)




    def missile(self,x,y,cmd_,stpd=False):
        if stpd:
            return False
  
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
            self.playground[x][y].restoreElement()
            self.playground[targetX][targetY].kill()
            self.playground[targetX][targetY].kill()
        else:
            self.playground[x][y].demolish()
            #we kill the messile, if it cannot move any further
        






    def player(self, x, y,cmd_,stpd=False):
        if stpd:
            self.playground[x][y].steppingOn.kill()
            return
        """
        Player control routine (x,y,(leftControl(direction,mod),rightControl(direction,mod)))
            It is quite simple, it adds smell to the smell matrix, 
            * checks if player should be killed, if so, kills it
            * checks if player shoots 

        """
        self.smell[x][y]=(PLAYER,100)
        neigh=self.findNeighboors(x,y)
        for n in neigh:
            if n[2].canKill==True:
                self.playground[x][y].kill()
                return
        if not cmd_:
            return
        if not cmd_[self.playground[x][y].playerNo]:
            return
        cmdTupple=cmd_[self.playground[x][y].playerNo]        
        cmd=cmdTupple[0]
#        print("{} -> {}".format(cmd,self.playground[x][y].playerNo))
        if cmdTupple[1]>0 and self.playground[x][y].playerNo +1>0:
            if self.playground[x][y].shooting==0:
                self.shootFromObject(x,y,cmdTupple)
                self.playground[x][y].shooting=15
                self.playground[x][y].moved=5
            return

        self.walkObjectDirection(x,y,cmd)

    def bomb(self, x, y,cmd,stpd=False):
        if stpd:
            return False

        if self.playground[x][y].shot==1:
          
            self.playground[x][y].demolish()
            if x>0:
                self.playground[x-1][y].demolish()
                if y>0:
                    self.playground[x-1][y-1].demolish()
                if y<self.sizeY-1:
                    self.playground[x-1][y+1].demolish()                
            if x<self.sizeX+1:
                self.playground[x+1][y].demolish()
                if y>0:
                    self.playground[x+1][y-1].demolish()
                if y<self.sizeY-1:
                    self.playground[x+1][y+1].demolish()
            if y>0:
                self.playground[x][y-1].demolish()
            if y<self.sizeY-1:
                self.playground[x][y+1].demolish()


 
    

if __name__=="__main__":
  pass