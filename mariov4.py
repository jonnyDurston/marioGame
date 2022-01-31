#Mario Clone

#Imports
from tkinter import *
from time import sleep
from pygame import mixer

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

    #Entity returns its height
    def getheight(self):
        return self.height

    #Entity returns its width
    def getwidth(self):
        return self.width

#Flag Class - based on Entity, but ends level when mario touches it
class Flag(Entity):
    #Initial setup
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.width=6
        self.height=64
        self.color="#00ff00"
        self.out="#00aa00"
        self.endsound = mixer.Sound(file="endsound.wav")
        self.nottouched=True

    #Returns true if x,y coords strictly inside entity
    def collided(self,x,y):
        if self.x<x and x<self.x+self.width and self.y<y and y<self.y+self.height:
            mixer.Channel(1).play(self.endsound)
            #mixer.Channel(1).stop()
            self.nottouched=False
            return True
        return False

#Coin Class - based on Entity but increases score and disappears when touched
class Coin(Entity):
    #Initial setup
    def __init__(self,x,y):
        self.x=x+4
        self.y=y+4
        self.width=8
        self.height=8
        self.color="#ffff00"
        self.out="#aaaa00"
        self.coinsound = mixer.Sound(file="coin.wav")
        self.touched=False

    #Returns true if x,y coords strictly inside entity
    def collided(self,x,y):
        if self.x<x and x<self.x+self.width and self.y<y and y<self.y+self.height:
            mixer.Channel(2).play(self.coinsound)
            self.touched=True
        return False

    #Returns whether coin has been collected or not
    def touched(self):
        return self.touched


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
        self.width = 10
        self.height = 15.9
        self.jumping = False
        self.image = PhotoImage(file="mario.gif")
        self.jumpsound = mixer.Sound(file="jumpsound.wav")
        self.jumpsound.set_volume(0.2)
        self.deathsound = mixer.Sound(file="death.wav")

    #Jumps - i.e sets y velocity
    def jump(self,event):
        if self.canjump:
            self.jumping = True
            self.canjump = False
            self.yv = -0.5
            mixer.Channel(0).play(self.jumpsound)

    #Stop Jumping
    def stopjump(self,event):
        self.jumping = False

    #Cycles through a list of entities and returns the first one it collides with
    def collision(self,entities,x,y):
        for entity in entities:
            if entity.collided(x,y):
                return (True,entity)
        return (False,"")

    #Update method - where marios x and y position are updated
    def update(self,entities):
        #Deals with jumping
        self.canjump = False
        if self.yv>-3 and self.yv<0 and self.jumping==True:
            self.yv-=0.5
        else:
            self.jumping=False
        #Adding effect of gravity
        if self.yv <2:
            self.yv += 0.1
        
        #Checking x collisions
        (c,b) = self.collision(entities,self.x+self.xv,self.y)
        if c:
            self.xv=0
            self.x=b.getxy()[0]+b.getwidth()+0.0001
        else:
            (c,b) = self.collision(entities,self.x+self.width+self.xv,self.y)
            if c:
                self.xv=0
                self.x=b.getxy()[0]-self.width-0.0001
            else:
                (c,b) = self.collision(entities,self.x+self.xv,self.y+self.height)
                if c:
                    self.xv=0
                    self.x=b.getxy()[0]+b.getwidth()+0.0001
                else:
                    (c,b) = self.collision(entities,self.x+self.width+self.xv,self.y+self.height)
                    if c:
                        self.xv=0
                        self.x=b.getxy()[0]-self.width-0.0001


        #Checking y collisions
        (c,b) = self.collision(entities,self.x,self.y+self.yv)
        if c:
            self.yv=0
            self.y=b.getxy()[1]+b.getheight()+0.0001
        else:
            (c,b) = self.collision(entities,self.x+self.width,self.y+self.yv)
            if c:
                self.yv=0
                self.y=b.getxy()[1]+b.getheight()+0.0001 
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
        if self.y>192+self.height:
            self.x=16.0001
            self.y=144
            self.xv=0
            self.yv=0
            self.campad=0
            mixer.Channel(0).play(self.deathsound)
            sleep(0.4)
            
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
  
    #Entity draws itself on the screen
    def display(self,canvas,camx):
        canvas.create_image(self.x-camx,self.y,image=self.image,anchor=NW)
    
        


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
    def display(self,entities,time,score):
        try:
            self.canvas.delete('all')
            displaylist = []
            for entity in entities:
                if entity.onscreen(self.camx):
                    displaylist.append(entity)
            for e in displaylist:
                e.display(self.canvas,self.camx)
            self.updatetimer(time)
            self.updatescore(score)
            self.root.update()
        except TclError:
            self.closed=True

    #Updates the timer on screen
    def updatetimer(self,time):
        self.canvas.create_text(32,16,fill="#000000",font="Courier 20",
                                text=str(int(time)))


    #Updates score on screen
    def updatescore(self,score):
        self.canvas.create_text(256,16,fill="#000000",font="Courier 20",
                                text=str(int(score)))
        

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
        self.gametime = 0
        self.score = 0
        self.gui = GUI()
        self.sounds()
        self.loadlevel(level)
        self.gui.root.bind("<Right>",self.mario.right)
        self.gui.root.bind("<Left>",self.mario.left)
        self.gui.root.bind("<KeyRelease-Right>",self.mario.stopright)
        self.gui.root.bind("<KeyRelease-Left>",self.mario.stopleft)
        self.gui.root.bind("<Up>",self.mario.jump)
        self.gui.root.bind("<KeyRelease-Up>",self.mario.stopjump)
        self.mainloop()

    #Do Sounds
    def sounds(self):
        mixer.pre_init(44100, -16, 2, 2048)
        mixer.init()
        music = mixer.Sound(file="music.wav")
        mixer.Channel(1).play(music)

    #Main running loop of game
    def mainloop(self):
        while self.gui.getquit()==False:
            self.gui.setcamx(self.mario.getxy()[0]-160+self.mario.getcampad())
            self.updateentities()
            self.gui.display(self.entities,self.gametime,self.score)
            if self.flag.nottouched:
                self.gametime+=0.01
            sleep(0.01)
        mixer.stop()

    #Loads in level from .txt file
    def loadlevel(self,level):
        self.entities = []
        self.blocks = []
        self.movables = []
        self.items = []
        leveltxt = open(level,"r")
        pixrows = leveltxt.readlines()
        y=0
        for pixrow in pixrows:
            x=0
            for pix in pixrow:
                if pix=="B":
                    obj = Entity(x,y,"#b5651d","#99ccff")#654321")
                    self.blocks.append(obj)
                elif pix=="M":
                    self.mario = Mario(x,y,"#ff0000","#880000")
                    self.movables.append(self.mario)
                elif pix=="F":
                    self.flag = Flag(x,y)
                    self.blocks.append(self.flag)
                elif pix=="C":
                    coin = Coin(x,y)
                    self.items.append(coin)
                x+=16
            y+=16
        self.entities.extend(self.blocks)
        self.entities.extend(self.movables)
        self.entities.extend(self.items)

    #Goes through each entity and gets it to move accordingly
    def updateentities(self):
        for entity in self.movables:
            ents = list(self.entities)
            for e in self.entities:
                if e.onscreen(self.gui.camx):
                    ents.append(e)
            ents.remove(entity)
            entity.update(ents)
        for item in self.items:
            if item.touched:
                self.score+=1
                print(self.score)
                self.items.remove(item)
                self.entities.remove(item)
                #del(item)
        

        

game = Game("1-3.txt")

