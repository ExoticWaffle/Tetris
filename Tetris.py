import pygame
import os
import random
from tetriminoes import *
os.environ['SDL_VIDEO_CENTERED']='1'
pygame.init()

screenWidth=640
screenHeight=760
win=pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Tetris")

class grid(object):
    def __init__(self):
        self.colorList=[]
        for r in range(22):
            self.colorList.append([(0,0,0)]*10)

    def draw(self):
        x,y,size=160,688,32
        
        for r in range(22):
            for c in range(10):
                pygame.draw.rect(win,self.colorList[r][c],(x+size*c,y-size*r,size,size))

        y+=size
        for i in range(11):
            pygame.draw.line(win,(64,64,64),(x+size*i,y),(x+size*i,y-size*20),2)
        for i in range(21):
            pygame.draw.line(win,(64,64,64),(x,y-size*i),(x+size*10,y-size*i),2)
        for i in range(11):
            pygame.draw.line(win,(0,0,0),(x+size*i,y-size*20),(x+size*i,y-size*24),2)
        for i in range(3):
            pygame.draw.line(win,(0,0,0),(x,y-size*(21+i)),(x+size*10,y-size*(21+i)),2)

    def getColorList(self):
        return self.colorList

    def setColorList(self, colorList):
        self.colorList=colorList

class gameManager(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.matrix=grid()
        self.nextPieces=[]
        self.pieceGen()
        self.piece=self.getNextPiece()
        self.holdPiece=tetrimino((0,0,0),(0,0,0),[[[0,0],[0,0],[0,0],[0,0]]],[[[[0]]]])
        self.held, self.lockDown, self.hardDrop, self.restarted, self.topOut=False, False, False, False, False

        self.clearCount, self.pieceCount, self.apm, self.pps=0,0,0,0

    def update(self, time, keys):
        colorList=self.matrix.getColorList()
        
        if keys[pygame.K_F4] and not self.restarted:
            self.reset()
            self.restarted=True
            colorList=[]
            for r in range(22):
                colorList.append([(0,0,0)]*10)
        
        if not keys[pygame.K_F4] and self.restarted:
            self.restarted=False
        
        if not self.topOut:
            if keys[pygame.K_c] and not self.held:
                self.piece.erase(colorList)
                temp=self.holdPiece
                self.holdPiece=self.piece
                if temp.color!=(0,0,0):
                    temp.reset()
                    self.piece=temp
                else:
                    self.piece=self.getNextPiece()
        
            if not keys[pygame.K_c] and self.held:
                self.held=False
            elif keys[pygame.K_c]:
                self.held=True
                
            if not keys[pygame.K_SPACE] and self.hardDrop:
                self.hardDrop=False
    
            self.lockDown=self.piece.update(colorList,time,keys,self.hardDrop)

            if(self.lockDown):
                self.elimination(colorList)
                if self.piece.y>=20:
                    self.topOut=self.topOutCheck(colorList)
                if self.topOut:
                    print("topout")
                else:
                    self.piece=self.getNextPiece()
                self.hardDrop=True

            self.erase()
            self.pieceGen()
            self.display()
        self.matrix.setColorList(colorList)
        self.matrix.draw()

        
    def pieceGen(self):
        if len(self.nextPieces)<14:
            ip,op,tp,jp,lp,sp,zp=iPiece(), oPiece(), tPiece(), jPiece(), lPiece(), sPiece(), zPiece()
            bag=[ip,op,tp,jp,lp,sp,zp]
            random.shuffle(bag)
            self.nextPieces.extend(bag)

    def elimination(self, colorList):
        rows=22
        line=0
        lineClear=False
        linesCleared=0
        for r in range(rows):
            for c in range(10):
                if colorList[line][c]==(0,0,0):
                    break
                if c==9:
                    colorList.pop(line)
                    colorList.append([(0,0,0)]*10)
                    lineClear=True
                    line-=1
                    rows-=1
                    linesCleared+=1
            line+=1

    def topOutCheck(self, colorList):
        for i in range(4):
            minoY1=self.piece.y+self.piece.minoList[self.piece.face][i][1]
            minoX2=self.nextPieces[0].x+self.nextPieces[0].minoList[0][i][0]
            minoY2=self.nextPieces[0].y+self.nextPieces[0].minoList[0][i][1]

            if colorList[minoY2][minoX2]!=(0,0,0):
                return True
        for i in range(4):
            minoY1=self.piece.y+self.piece.minoList[self.piece.face][i][1]

            if minoY1<20:
                return False
        return True
        
        


    def display(self):
        #next
        x,y,size=512,112,24
        for i in range(5):
            piece=self.nextPieces[i]
            if piece.color==(0,255,255):
                y-=size/2
                x=512
            elif piece.color==(255,255,0):
                x=512+size
            else:
                x=512+(size/2)

            for j in range(4):
                minoX=x+(size*piece.minoList[0][j][0])
                minoY=y-(size*piece.minoList[0][j][1])
                pygame.draw.rect(win,piece.color,(minoX,minoY,size,size))
                pygame.draw.rect(win,(0,0,0),(minoX,minoY,size,size),1)
            
            if piece.color==(0,255,255):
                y+=size/2
            y+=80
        
        #hold
        x,y,size=32,112,24
        if self.holdPiece.color==(0,255,255):
            y-=size/2
        elif self.holdPiece.color==(255,255,0):
            x=32+size
        else:
            x=32+(size/2)

        for j in range(4):
            minoX=x+(size*self.holdPiece.minoList[0][j][0])
            minoY=y-(size*self.holdPiece.minoList[0][j][1])
            pygame.draw.rect(win,self.holdPiece.color,(minoX,minoY,size,size))
            pygame.draw.rect(win,(0,0,0),(minoX,minoY,size,size),1)

    def erase(self):
        pygame.draw.rect(win, (0,0,0), (510, 100, 100, 500))
        pygame.draw.rect(win, (0,0,0), (30, 100, 100, 100))

    def getNextPiece(self):
        return self.nextPieces.pop(0)

game=gameManager()
clock=pygame.time.Clock()
run=True
hardDrop=False

while run:
    clock.tick(60)
    time=pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    
    keys=pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run=False

    game.update(time, keys)

    pygame.display.update()


pygame.quit()
