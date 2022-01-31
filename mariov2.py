#Mario Clone

#Imports
from tkinter import *
from time import sleep

#Entity Class
class Entity(object):
    def __init__(self,x,y,color,out):
        self.color=color
        self.out=out
        self.x=x
        self.y=y

    def onscreen(self,camx):
        if -16<=self.x-camx and self.x-camx<=320:
            return True
        return False

    def collided(self,x,y):
        if self.x<x and x<self.x+16 and self.y<y and y<self.y+16:
            return True
        return False
            

    def display(self,canvas,camx):
        canvas.create_rectangle(self.x-camx,self.y,self.x-camx+16,self.y+16,
                                fill=self.color,outline=self.out)

    
    def getxy(self):
        return (self.x,self.y)


#Mario Class
class Mario(Entity):
    def __init__(self,x,y,color,out):
        super(Mario,self).__init__(x+0.1,y,color,out)
        self.xv = 0
        self.yv = 0
        self.canjump = False
        
    def right(self,event):
        self.xv=1

    def left(self,event):
        self.xv=-1

    def jump(self,event):
        if self.canjump:
            self.yv = -3
            self.canjump = False

    def stopleft(self,event):
        if self.xv ==-1:
            self.xv=0

    def stopright(self,event):
        if self.xv ==1:
            self.xv=0

    def stopup(self,event):
        self.yv=0
        print("STOPUP")

    def update(self,entities):

        #Adding effect of gravity
        if self.yv <3:
            self.yv += 0.1
        
        #Checking x collisions
        (c,b) = self.collision(entities,self.x+self.xv,self.y)
        if c:
            self.xv=0
            self.x=b.getxy()[0]+16.0001
        else:
            (c,b) = self.collision(entities,self.x+16+self.xv,self.y)
            if c:
                self.xv=0
                self.x=b.getxy()[0]-16.0001
            else:
                (c,b) = self.collision(entities,self.x+self.xv,self.y+16)
                if c:
                    self.xv=0
                    self.x=b.getxy()[0]+16.0001
                else:
                    (c,b) = self.collision(entities,self.x+16+self.xv,self.y+16)
                    if c:
                        self.xv=0
                        self.x=b.getxy()[0]-16.0001


        #Checking y collisions
        (c,b) = self.collision(entities,self.x,self.y+self.yv)
        if c:
            self.yv=0
            self.y=b.getxy()[1]+16.0001
            print(b)
        else:
            (c,b) = self.collision(entities,self.x+16,self.y+self.yv)
            if c:
                self.yv=0
                self.y=b.getxy()[1]+16.0001 
            else:
                (c,b) = self.collision(entities,self.x,self.y+16+self.yv)
                if c:
                    self.yv=0
                    self.y=b.getxy()[1]-16.0001
                    self.canjump=True
                else:
                    (c,b) = self.collision(entities,self.x+16,self.y+16+self.yv)
                    if c:
                        self.yv=0
                        self.y=b.getxy()[1]-16.0001
                        self.canjump=True
                        
        #Do motion
        self.x += self.xv
        self.y += self.yv
        

    def collision(self,entities,x,y):
        for entity in entities:
            if entity.collided(x,y):
                return (True,entity)
        return (False,"")

    def getnewxy(self):
        return (self.x+self.xv,self.y+self.yv)

    def setx(self,x):
        self.x=x

    def sety(self,y):
        self.y=y

    
        


#Screen Class
class GUI(object):
    def __init__(self):
        self.root = Tk()

        self.loadwidgets()

        self.keybindings()

        self.camx = 0
        self.closed = False

    def loadwidgets(self):
        self.canvas = Canvas(self.root,height=192,width=320,bg="#99ccff")
        self.canvas.grid(column=0,row=0)

    def display(self,entities):
        self.canvas.delete('all')
        displaylist = []
        for entity in entities:
            if entity.onscreen(self.camx):
                displaylist.append(entity)
        for e in displaylist:
            e.display(self.canvas,self.camx)
        self.root.update()

    def keybindings(self):
        self.root.bind("<Escape>",self.quit)

    def setcamx(self,x):
        self.camx = x

    def quit(self,event):
        self.closed=True
        self.root.destroy()

    def getquit(self):
        return self.closed
                    
#Game Class
class Game(object):
    def __init__(self,level):
        self.loadlevel(level)
        self.collidedold=[]
        self.gui = GUI()
        self.gui.root.bind("<Right>",self.mario.right)
        self.gui.root.bind("<Left>",self.mario.left)
        self.gui.root.bind("<KeyRelease-Right>",self.mario.stopright)
        self.gui.root.bind("<KeyRelease-Left>",self.mario.stopleft)
        self.gui.root.bind("<Up>",self.mario.jump)
        self.mainloop()

    def mainloop(self):
        while self.gui.getquit()==False:
            self.gui.setcamx(self.mario.getxy()[0]-160)
            self.updateentities()
            self.gui.display(self.entities)
            sleep(0.02)

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

    def updateentities(self):
        for entity in self.movables:
            ents = list(self.entities)
            for e in self.entities:
                if e.onscreen(self.gui.camx):
                    ents.append(e)
            ents.remove(entity)
            entity.update(ents)

        

        
        

game = Game("1-1.txt")

