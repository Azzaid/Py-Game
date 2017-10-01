import pygame, sys, random, math
from pygame.locals import *
pygame.init()
DISPLAYHEIGHT = 600
DISPLAYLENGHT = 1200
DISPLAYSURF = pygame.display.set_mode((DISPLAYLENGHT, DISPLAYHEIGHT))
pygame.display.set_caption('Endless mobrun')
FPS = 30
fpsClock = pygame.time.Clock()
pygame.key.set_repeat(300, 100)
FONT = pygame.font.Font('freesansbold.ttf', 12)

MOBXPOS = 800
MOBYPOS = 200
GUNSIZEX = 100
GUNSIZEY = 50
X = 300
Y = 200 - GUNSIZEY/2
GUNCENTRX = X + GUNSIZEX/2
GUNCENTRY = Y + GUNSIZEY/2

GunImg = pygame.image.load('D:\Puthon\My lern progr\BestIdleGameEver\BigGun.gif')
GunImg = pygame.transform.scale(GunImg, (GUNSIZEX,GUNSIZEY))
LaserImg = pygame.image.load('D:\Puthon\My lern progr\BestIdleGameEver\LaserCan.png')
LaserImg = pygame.transform.scale(LaserImg, (GUNSIZEX,GUNSIZEY))
Coord = pygame.image.load('D:\Puthon\My lern progr\BestIdleGameEver\Cd.png')
Coord = pygame.transform.scale(Coord, (GUNSIZEX,GUNSIZEY))

y1=300
x1=300
y2=300
x2=500
y3=100
x3=500
DispCord= 0
angle = 0
## main game screen
while True:
    DISPLAYSURF.fill((110, 100, 100))
    if DispCord == 1:
        COORDS = FONT.render("xmouse: " + str(xmouse) + "   ymouse: " + str(ymouse), True, (100, 100, 100), (10, 10, 10))
        DISPLAYSURF.blit(COORDS, (1000, 10))
    ##pygame.draw.line(DISPLAYSURF, (200, 0, 0), (x1, y1), (x2, y2), 2)
    ##pygame.draw.line(DISPLAYSURF, (200, 0, 0), (x2, y2), (x3, y3), 2)
    ##pygame.draw.line(DISPLAYSURF, (0, 200, 0, 50), (x1, y1), (x1+int(math.sqrt((x2-x1)**2 + (y2-y3)**2)*math.cos(math.fabs(math.atan2(x2-x1,y2-y3)))), y1-int(math.sqrt((x2-x1)**2 + (y2-y3)**2)*math.sin(math.fabs(math.atan2(x2-x1,y2-y3))))), 8)
    ##pygame.draw.line(DISPLAYSURF, (0, 200, 0), (x1, y1), (x3, y3), 4)
    angle = (math.atan2(Y + GUNSIZEY/2 - MOBYPOS, MOBXPOS - X - GUNSIZEX/2))*57.29
    print(angle)
    anglerad = math.fabs(math.atan2(Y + GUNSIZEY/2 - MOBYPOS, MOBXPOS - X - GUNSIZEX/2))
    a = GUNSIZEX*math.cos(anglerad)
    b = GUNSIZEX*math.sin(anglerad)
    c = GUNSIZEY*math.cos(anglerad)
    d = GUNSIZEY*math.sin(anglerad)
    if angle >= 0:
        Y2 = Y + b + c
        X2 = X + d
        Y1 = Y
        X1 = X + a
        Yc = int(Y1 + (Y2 - Y1)/2)
        Xc = int(X2 + (X1 - X2)/2)
        dY = Yc - Y - GUNSIZEY/2
        dX = Xc - X - GUNSIZEX/2
    else:
        Y2 = Y + b + c
        X2 = X + a
        Y1 = Y
        X1 = X + d
        Yc = int(Y1 + (Y2 - Y1)/2)
        Xc = int(X1 + (X2 - X1)/2)
        dY = Yc - Y - GUNSIZEY/2
        dX = Xc - X - GUNSIZEX/2
    ##DISPLAYSURF.blit(pygame.transform.rotate(Coord, angle), (X-dX , Y-dY))
    pygame.draw.line(DISPLAYSURF, (200, 0, 0), (X+GUNSIZEX/2, Y+GUNSIZEY/2), (MOBXPOS, MOBYPOS), 4)
    DISPLAYSURF.blit(pygame.transform.rotate(LaserImg, angle), (X-dX , Y-dY))
    pygame.draw.circle(DISPLAYSURF, (0, 200, 0), (X+GUNSIZEX/2, Y+GUNSIZEY/2), 4, 0)
    pygame.draw.line(DISPLAYSURF, (200, 0, 0), (X, Y), (X-dX, Y-dY), 4)
    pygame.draw.circle(DISPLAYSURF, (200, 0, 0), (MOBXPOS, MOBYPOS), 8, 0)
    
    
## Control mechanic                                    
    for event in pygame.event.get():
        if pygame.mouse.get_pressed()[0]:
            DispCord = 1
            xmouse = pygame.mouse.get_pos()[0]
            ymouse = pygame.mouse.get_pos()[1]
        if pygame.key.get_pressed()[pygame.K_UP]:
            MOBYPOS -=5
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            MOBYPOS +=5
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            MOBXPOS -=5
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            MOBXPOS +=5
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.display.update()
    fpsClock.tick(FPS)