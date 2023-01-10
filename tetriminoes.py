import pygame

class tetrimino(object):
    def __init__(self, color, gcolor, minoList, rotList):
        self.color=color
        self.gColor=gcolor
        self.minoList=minoList
        self.rotList=rotList
        self.reset()

    def reset(self):
        self.face=0
        max=-10
        for i in range(4):
            if self.minoList[0][i][0]>max:
                max=self.minoList[0][i][0]
        width=max+1

        self.x=((10-width)//2)
        self.ghostY=0
        
        self.y=21

        self.dropAnchor=-1000
        self.shiftAnchor=0
        self.lockAnchor=0

        self.rotated=False
        self.das=False
        self.noMove=True
        self.startLock=False

    def update(self, colorList, time, keys, hardDrop):
        self.setAnchors(keys,time)
        self.erase(colorList)
        

        if (keys[pygame.K_SPACE] and not hardDrop) or (time-self.lockAnchor>=500 and self.startLock):
            self.y=self.ghostY
            lockDown=True
            self.startLock=False
        
        else:
            self.drop(colorList, time)
            lockDown=False
        
        if keys[pygame.K_a] or keys[pygame.K_d]:
            self.shift(colorList,self.shiftAnchor,time,keys)

        if (keys[pygame.K_j] or keys[pygame.K_k]) and self.color!=(255,255,0):
            if not self.rotated:
                self.rotate(colorList, keys)
                if self.startLock:
                    self.lockAnchor=time
            self.rotated=True
        
        self.setGhost(colorList)
        self.draw(colorList)
        return lockDown

    def setAnchors(self, keys, time):
        #das arr
        if (self.das and (time-self.shiftAnchor)>=100) or (not(self.das) and (time-self.shiftAnchor)>=40):
            self.shiftAnchor=time
            self.das=False

        #drop
        if (keys[pygame.K_s] and (time-self.dropAnchor)>=25) or (not(keys[pygame.K_s]) and (time-self.dropAnchor)>=1000):
            self.dropAnchor=time

        #move or no move, das
        if (keys[pygame.K_a] or keys[pygame.K_d]) and self.noMove:
            self.das=True
            self.noMove=False
            self.shiftAnchor=time
        
        if not(keys[pygame.K_a] or keys[pygame.K_d]):
            self.das=False
            self.noMove=True

        #rotate bool
        if not(keys[pygame.K_j] or keys[pygame.K_k]) and self.rotated:
            self.rotated=False

        #start lockdown
        if self.ghostY==self.y and not self.startLock:
            self.startLock=True
            self.lockAnchor=time
        elif self.ghostY!=self.y and self.startLock:
            self.startLock=False
            self.dropAnchor=time+1

    def drop(self, colorList,  time):
        if time==self.dropAnchor and self.y!=self.ghostY:
            for i in range(4):
                minoX=self.x+self.minoList[self.face][i][0]
                minoY=(self.y-1)+self.minoList[self.face][i][1]
                if colorList[minoY][minoX]!=(0,0,0) or minoY<0:
                    break
                if i==3:
                    self.y-=1

    def shift(self, colorList, anchor, time, keys):
        if keys[pygame.K_d]:
            direction=1
        elif keys[pygame.K_a]:
            direction=-1
        
        if (anchor==time):
            next=self.x+direction
            move=True
            for i in range(4):
                minoX=next+self.minoList[self.face][i][0]
                minoY=self.y+self.minoList[self.face][i][1]
                if minoX<0 or minoX>9:
                    move=False
                elif colorList[minoY][minoX]!=(0,0,0):
                    move=False
            if move:
                self.x=next
    
    def rotate(self, colorList, keys):
        if keys[pygame.K_j]:
            n=-1
            m=0
        elif keys[pygame.K_k]:
            n=1
            m=1

        next=self.face+n
        if next<0:
            next=3
        elif next>3:
            next=0

        canRotate=False

        for i in range(5):
            rotX=self.rotList[self.face][m][i][0]
            rotY=self.rotList[self.face][m][i][1]
            for j in range(4):
                minoX=self.x+self.minoList[next][j][0]+rotX
                minoY=self.y+self.minoList[next][j][1]+rotY
                if minoX<=9 and minoX>=0 and minoY<=21 and minoY>=0:
                    if colorList[minoY][minoX]!=(0,0,0):
                        break
                else:
                    break
                if j==3:
                    canRotate=True
            if canRotate:
                self.face=next
                self.x+=rotX
                self.y+=rotY
                break

    def erase(self, colorList):
        for i in range(4):
            minoX=self.x+self.minoList[self.face][i][0]
            minoY=self.y+self.minoList[self.face][i][1]
            minoGY=self.ghostY+self.minoList[self.face][i][1]
            colorList[minoY][minoX]=(0,0,0)
            if(colorList[minoGY][minoX]==self.gColor):
                colorList[minoGY][minoX]=(0,0,0)

    def setGhost(self, colorList):
        self.ghostY=0
        checkY=0
        while checkY!=self.y:
            for i in range(4):
                minoX=self.x+self.minoList[self.face][i][0]
                minoY=checkY+self.minoList[self.face][i][1]
                if colorList[minoY][minoX]!=(0,0,0) or minoY<0:
                    self.ghostY=checkY+1
                    break
            checkY+=1

    def lockDown(self, heightList):
        minoX=self.x+self.hSpan[0]
        for i in range(len(self.vSpan)):
            heightList[minoX+i]+=self.vSpan[i]

    def draw(self, colorList):
        #ghost piece
        for i in range(4):
            minoX=self.x+self.minoList[self.face][i][0]
            minoY=self.ghostY+self.minoList[self.face][i][1]
            colorList[minoY][minoX]=self.gColor
        #piece
        for i in range(4):
            minoX=self.x+self.minoList[self.face][i][0]
            minoY=self.y+self.minoList[self.face][i][1]
            colorList[minoY][minoX]=self.color


iMino=[[[0,-1],[1,-1],[2,-1],[3,-1]],[[2,0],[2,-1],[2,-2],[2,-3]],[[0,-2],[1,-2],[2,-2],[3,-2]],[[1,0],[1,-1],[1,-2],[1,-3]]]

oMino=[[[0,0],[0,-1],[1,0],[1,-1]]]

tMino=[[[1,0],[0,-1],[1,-1],[2,-1]],[[1,0],[1,-1],[2,-1],[1,-2]],[[0,-1],[1,-1],[2,-1],[1,-2]],[[1,0],[0,-1],[1,-1],[1,-2]]]

jMino=[[[0,0],[0,-1],[1,-1],[2,-1]],[[2,0],[1,0],[1,-1],[1,-2]],[[0,-1],[1,-1],[2,-1],[2,-2]],[[1,0],[1,-1],[1,-2],[0,-2]]]

lMino=[[[2,0],[0,-1],[1,-1],[2,-1]],[[1,0],[1,-1],[1,-2],[2,-2]],[[2,-1],[1,-1],[0,-1],[0,-2]],[[0,0],[1,0],[1,-1],[1,-2]]]

sMino=[[[1,0],[0,-1],[1,-1],[2,0]],[[1,0],[1,-1],[2,-1],[2,-2]],[[2,-1],[1,-1],[1,-2],[0,-2]],[[0,0],[0,-1],[1,-1],[1,-2]]]

zMino=[[[0,0],[1,0],[1,-1],[2,-1]],[[2,0],[2,-1],[1,-1],[1,-2]],[[0,-1],[1,-1],[1,-2],[2,-2]],[[1,0],[1,-1],[0,-1],[0,-2]]]


iRotN=[[[0,0],[-1,0],[2,0],[-1,2],[2,-1]],[[0,0],[-2,0],[1,0],[-2,-1],[1,2]]]
iRotE=[[[0,0],[2,0],[-1,0],[2,1],[-1,-2]],[[0,0],[-1,0],[2,0],[-1,2],[2,-1]]]
iRotS=[[[0,0],[1,0],[-2,0],[1,-2],[-2,1]],[[0,0],[2,0],[-1,0],[2,1],[-1,-2]]]
iRotW=[[[0,0],[-2,0],[1,0],[-2,-1],[1,2]],[[0,0],[1,0],[-2,0],[1,-2],[-2,1]]]
iRotList=[iRotN,iRotE,iRotS,iRotW]

tRotN=[[[0,0],[1,0],[1,1],[50,50],[1,-2]],[[0,0],[-1,0],[-1,1],[50,50],[-1,-2]]]
tRotE=[[[0,0],[1,0],[1,-1],[0,2],[1,2]],[[0,0],[1,0],[1,-1],[0,2],[1,2]]]
tRotS=[[[0,0],[-1,0],[50,50],[0,-2],[-1,-2]],[[0,0],[1,0],[50,50],[0,-2],[1,-2]]]
tRotW=[[[0,0],[-1,0],[-1,-1],[0,2],[-1,2]],[[0,0],[-1,0],[-1,-1],[0,2],[-1,2]]]
tRotList=[tRotN,tRotE,tRotS,tRotW]

jlszRotN=[[[0,0],[1,0],[1,1],[0,-2],[1,-2]],[[0,0],[-1,0],[-1,1],[0,-2],[-1,-2]]]
jlszRotE=[[[0,0],[1,0],[1,-1],[0,2],[1,2]],[[0,0],[1,0],[1,-1],[0,2],[1,2]]]
jlszRotS=[[[0,0],[-1,0],[-1,1],[0,-2],[-1,-2]],[[0,0],[1,0],[1,1],[0,-2],[1,-2]]]
jlszRotW=[[[0,0],[-1,0],[-1,-1],[0,2],[-1,2]],[[0,0],[-1,0],[-1,-1],[0,2],[-1,2]]]
jlszRotList=[jlszRotN,jlszRotE,jlszRotS,jlszRotW]

oRotList=[]





class iPiece(tetrimino):
    def __init__(self):
        tetrimino.__init__(self,(0,255,255), (0,128,128), iMino, iRotList)

class oPiece(tetrimino):
    def __init__(self):
        tetrimino.__init__(self,(255,255,0), (128,128,0), oMino, oRotList)

class tPiece(tetrimino):
    def __init__(self):
        tetrimino.__init__(self,(192,0,192), (96,0,96), tMino, tRotList)

class jPiece(tetrimino):
    def __init__(self):
        tetrimino.__init__(self,(0,0,255), (0,0,128), jMino, jlszRotList)

class lPiece(tetrimino):
    def __init__(self):
        tetrimino.__init__(self,(255,165,0), (128,83,0), lMino, jlszRotList)

class sPiece(tetrimino):
    def __init__(self):
        tetrimino.__init__(self,(0,255,0), (0,128,0), sMino, jlszRotList)

class zPiece(tetrimino):
    def __init__(self):
        tetrimino.__init__(self,(255,0,0), (128,0,0), zMino, jlszRotList)


