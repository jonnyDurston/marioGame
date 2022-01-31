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

    def collide(self,xmin,xmax,ymin,ymax):
        if self.x+16>xmin and self.x<xmax and self.y+16>=ymin  and self.y<ymax:
            if self.x<=xmin+2 or self.x>=xmax-2:
                print("x collision")
                return "x"
            else:
                print("y collision")
                return "y"
            

    def display(self,canvas,camx):
        canvas.create_rectangle(self.x-camx,self.y,self.x-camx+16,self.y+16,
                                fill=self.color,outline=self.out)


#Mario Class
class Mario(Entity):
    def __init__(self,x,y,color,out):
        super(Mario,self).__init__(x+3,y,color,out)
        self.xv = 0
        self.yv = 0
        self.onground = True
        
    def right(self,event):
        self.xv=1
        print("RIGHT")

    def stopright(self,event):
        self.xv=0
        print("STOPRIGHT")

    def stopup(self,event):
        self.yv=0
        print("STOPUP")

    def update(self):
        self.x += self.xv
        self.y += self.yv

    def getxy(self):
        return (self.x,self.y)

    def setx(self,x):
        self.x=x

    def sety(self,y):
        self.y=y

    def jump(self,event):
        self.yv = 2

    def gravitate(self):
        if self.yv<1:
            self.yv=+0.1
    
        


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
        self.gui = GUI()
        self.gui.root.bind("<Right>",self.mario.right)
        self.gui.root.bind("<KeyRelease-Right>",self.mario.stopright)
        self.gui.root.bind("<Up>",self.mario.jump)
        self.mainloop()

    def mainloop(self):
        while self.gui.getquit()==False:
            self.gui.setcamx(self.mario.getxy()[0]-160)
            self.updateentities()
            self.gui.display(self.entities)
            sleep(0.04)

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
            (x,y)=entity.getxy()
            entity.update()
            self.collisions(entity,x,y)

    def collisions(self,entity,x,y):
        (xnew,ynew) = entity.getxy()
        ents = list(self.entities)
        ents.remove(entity)
        gravitate = True
        for collidable in ents:
            collision = collidable.collide(xnew,xnew+16,ynew,ynew+16)
            if collision == "x":
                entity.setx(x)
                entity.stopright("")
            elif collision == "y":
                entity.sety(y-(y%16))
                print(y,y%16)
                entity.stopup("")
                gravitate=False
        if gravitate:
            entity.gravitate()

        
        

game = Game("1-1.txt")

