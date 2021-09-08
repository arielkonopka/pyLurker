# Board Module


Few notes on the Board Module.

# Classes

## boardMember
Board member is an experiment with responsibility shift for some tasks, so the board code could theoretically be a bit simpler.


## Board
This class is responsible for the whole game mechanics. While boardMember objects "know" what does it mean that they are being stepped on and off, the **board** class is responsible for iterating the board and performing most of the game logic.

### Movement

Movement is realized by stepping on objects, that are steppable. Method responsible is moveObj(self,posFrom,posTo,direction,speed).
Even better method for that is: walkObjectDirection(x,y,direction), as it checks various things like if the object that is to be moved is allowed to move at all and for most objects it is adviced to use it. 

Basically all objects are standing on an EMPTYELEMENT. When we want to move an object, we have to restore the object that is currently being stepped on and move the object to another location,
and adding previously standing object to our object (assign it to steppingOn variable in boardMember class). With this attitude we can also notice the object if is is being currently stepped on.
That can let us to build landmines or puzzles like sokoban. This of course implies a specific construction of the mechanics

Now we iterate through the board and perform two main actions:
* elementMech(x, y,command,True) - for the stepped object
* elementMech(x, y,command,False) - for the main object

So the object mechanic routine must be defined like this:
    def routine(self,posX,posY,command,isStepped):
        if isStepped:
            # perform actions for an object that is being stepped on
            return
        # the rest of the body



