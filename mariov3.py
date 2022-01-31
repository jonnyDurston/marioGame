#Mario Clone

#Imports
from tkinter import *
from time import sleep

#Entity Class
class Entity(object):
    #Initial Setup
    def __init__(self,x,y,color,out):
        self.color=color
        self.out=out
        self.x=x
        self.y=y
        self.width=16
        self.height=16

    #Entity on screen returns True, otherwise False
    def onscreen(self,camx):
        if -self.width<=self.x-camx and self.x-camx<=320:
            return True
        return False

    #Returns true if x,y coords strictly inside entity
    def collided(self,x,y):
        if self.x<x and x<self.x+self.width and self.y<y and y<self.y+self.height:
            return True
        return False
            
    #Entity draws itself on the screen
    def display(self,canvas,camx):
        canvas.create_rectangle(self.x-camx,self.y,self.x-camx+self.width,self.y+self.height,
                                fill=self.color,outline=self.out)

    #Entity returns its x,y coordinates
    def getxy(self):
        return (self.x,self.y)


#Movable Class - based on Entity but can move
class Movable(Entity):
    #Initial Setup
    def __init__(self,x,y,color,out):
        super(Movable,self).__init__(x+0.1,y,color,out)
        self.xv = 0
        self.yv = 0

    #Move right
    def right(self,event):
        self.xv=1

    #Move left
    def left(self,event):
        self.xv=-1

    #Stop left velocity
    def stopleft(self,event):
        if self.xv ==-1:
            self.xv=0

    #Stop right velocity
    def stopright(self,event):
        if self.xv ==1:
            self.xv=0

    #Moves entity by x and y velocities
    def update(self,event):
        self.x+=self.xv
        self.y+=self.yv


#Mario Class - based on Movable but adjusts camera and can collision detect
class Mario(Movable):
    #Initial Setup
    def __init__(self,x,y,color,out):
        super(Mario,self).__init__(x,y,color,out)
        self.campad = 0
        self.canjump = False
        self.width = 12
        self.height = 15

    #Jumps - i.e sets y velocity
    def jump(self,event):
        if self.canjump:
            self.yv = -3
            self.canjump = False

    #Cycles through a list of entities and returns the first one it collides with
    def collision(self,entities,x,y):
        for entity in entities:
            if entity.collided(x,y):
                return (True,entity)
        return (False,"")

    #Update method - where marios x and y position are updated
    def update(self,entities):
        self.canjump = False
        #Adding effect of gravity
        if self.yv <3:
            self.yv += 0.1
        
        #Checking x collisions
        (c,b) = self.collision(entities,self.x+self.xv,self.y)
        if c:
            self.xv=0
            self.x=b.getxy()[0]+self.width+0.0001
        else:
            (c,b) = self.collision(entities,self.x+self.width+self.xv,self.y)
            if c:
                self.xv=0
                self.x=b.getxy()[0]-self.width-0.0001
            else:
                (c,b) = self.collision(entities,self.x+self.xv,self.y+self.height)
                if c:
                    self.xv=0
                    self.x=b.getxy()[0]+self.width+0.0001
                else:
                    (c,b) = self.collision(entities,self.x+self.width+self.xv,self.y+self.height)
                    if c:
                        self.xv=0
                        self.x=b.getxy()[0]-self.width-0.0001


        #Checking y collisions
        (c,b) = self.collision(entities,self.x,self.y+self.yv)
        if c:
            self.yv=0
            self.y=b.getxy()[1]+self.height+0.0001
            print(b)
        else:
            (c,b) = self.collision(entities,self.x+self.width,self.y+self.yv)
            if c:
                self.yv=0
                self.y=b.getxy()[1]+self.height+0.0001 
            else:
                (c,b) = self.collision(entities,self.x,self.y+self.height+self.yv)
                if c:
                    self.yv=0
                    self.y=b.getxy()[1]-self.height-0.0001
                    self.canjump=True
                else:
                    (c,b) = self.collision(entities,self.x+self.width,self.y+self.height+self.yv)
                    if c:
                        self.yv=0
                        self.y=b.getxy()[1]-self.height-0.0001
                        self.canjump=True

        #TEMP
        if self.y>260:
            self.x=16.0001
            self.y=144
            self.xv=0
            self.yv=0
            self.campad=0
            
        #Do motion
        self.campadupdate()
        self.x += self.xv
        self.y += self.yv

    #Updates padding on camera
    def campadupdate(self):
        if self.xv == 1 and self.campad>-32:
            self.campad -= 1
        elif self.xv == -1 and self.campad<32:
            self.campad += 1

    #Gets the current padding on the camera
    def getcampad(self):
        return self.campad


    
        


#Screen Class
class GUI(object):
    #Initial setup
    def __init__(self):
        self.root = Tk()

        self.loadwidgets()

        self.keybindings()

        self.camx = 0
        self.closed = False

    #Loads canvas onto screen
    def loadwidgets(self):
        self.canvas = Canvas(self.root,height=192,width=320,bg="#99ccff")
        self.canvas.grid(column=0,row=0)

    #Displays all entities on screen
    def display(self,entities):
        self.canvas.delete('all')
        displaylist = []
        for entity in entities:
            if entity.onscreen(self.camx):
                displaylist.append(entity)
        for e in displaylist:
            e.display(self.canvas,self.camx)
        self.root.update()

    #Binds escape to quit
    def keybindings(self):
        self.root.bind("<Escape>",self.quit)
        
    #Sets x position of camera
    def setcamx(self,x):
        self.camx = x

    #Closes game
    def quit(self,event):
        self.closed=True
        self.root.destroy()

    #Returns if True if the window has been closed
    def getquit(self):
        return self.closed
                    
#Game Class
class Game(object):
    #Initial Setup
    def __init__(self,level):
        self.loadlevel(level)
        self.gui = GUI()
        self.gui.root.bind("<Right>",self.mario.right)
        self.gui.root.bind("<Left>",self.mario.left)
        self.gui.root.bind("<KeyRelease-Right>",self.mario.stopright)
        self.gui.root.bind("<KeyRelease-Left>",self.mario.stopleft)
        self.gui.root.bind("<Up>",self.mario.jump)
        self.mainloop()

    #Main running loop of game
    def mainloop(self):
        while self.gui.getquit()==False:
            self.gui.setcamx(self.mario.getxy()[0]-160+self.mario.getcampad())
            self.updateentities()
            self.gui.display(self.entities)
            sleep(0.01)

    #Loads in level from .txt file
    def loadlevel(self,level):
        self.entities = []
        self.blocks = []
        self.movables = []
        leveltxt = open(level,"r")
        pixrows = leveltxt.readlines()
        y=0
        for pixrow in pixrows:
            x=0
            for pix in pixrow:
                if pix=="B":
                    obj = Entity(x,y,"#b5651d","#654321")
                    self.blocks.append(obj)
                elif pix=="M":
                    self.mario = Mario(x,y,"#ff0000","#880000")
                    self.movables.append(self.mario)
                x+=16
            y+=16
        self.entities.extend(self.blocks)
        self.entities.extend(self.movables)

    #Goes through each entity and gets it to move accordingly
    def updateentities(self):
        for entity in self.movables:
            ents = list(self.entities)
            for e in self.entities:
                if e.onscreen(self.gui.camx):
                    ents.append(e)
            ents.remove(entity)
            entity.update(ents)

        

        
        

game = Game("1-2.txt")

