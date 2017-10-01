import pygame, sys, random, math, os
from pygame.locals import *
pygame.init()
DISPLAYHEIGHT = 600
DISPLAYLENGHT = 1200
DISPLAYSURF = pygame.display.set_mode((DISPLAYLENGHT, DISPLAYHEIGHT))
pygame.display.set_caption('Endless mobrun')
FPS = 30
fpsClock = pygame.time.Clock()
RootDir = str(__file__).split("\EndlessMobrunUpgraded.py")[0]

global AGE
AGE = 0

FRAMENUMB = 1

MOBLIST = []
SPLATLIST = []
WAVETIMER = 150
BASEMOBCOUNT = 5
MOBPERWAVE = 1
FASTCHANSE = 5
BIGCHANSE = 10
BASESPEED = 3
BASEHEALTH = 10
BASEGOLD = 10
SPEEDPERLV = 0.1
HEALTHPERLV = 10
GOLDPERLV = 4
SIZEMODIFIERLIST = {"Small":{"health":0.5, "speed":2, "gold":0.5, "size":(40, 70)},
                    "Normal":{"health":1, "speed":1, "gold":1, "size":(60, 90)},
                    "Big":{"health":4, "speed":0.5, "gold":4, "size":(80, 200)}}
MOBIMGLIST = {}
MobDir = RootDir + "\Mobs"
for folder in os.listdir(MobDir):
    MOBIMGLIST[folder] = []
    for subfolder in os.listdir(MobDir + '\\\\' + folder):
        MOBIMGLIST[folder].append([])
        for img in os.listdir(MobDir + '\\\\' + folder + '\\\\' + subfolder):
            MOBIMGLIST[folder][int(subfolder[4])].append(pygame.transform.scale(pygame.image.load(MobDir + '\\\\' + folder + '\\\\' + subfolder + '\\\\' + img), SIZEMODIFIERLIST[folder]["size"]))


CHOOSENGUN = 0
BASEGUNCOUNT = 1
GUNTURNSPEED = 2
GUNDAMAGE = 30
BASEGUNCHARGE = 50
SHOTLENGHT = 10
PROJLIST = []
GUNSIZEX = 100
GUNSIZEY = 50
PROJSIZEX = 70
PROJSIZEY = 20
EXPLSIZEX = 40
EXPLSIZEY = 40
GUNTYPHELIST = ["Bow", "Gun", "Laser"]
GUNTYPHEMODIFIERSLIST = {"Bow":{"reload":1, "damage":1, "turnspeed":1, "shotlenght":1, "type":"proj", "special":"cripple", "price":500, "description":"fast but not strong enoff"},
                         "Gun":{"reload":1.5, "damage":3, "turnspeed":0.5, "shotlenght":0.5, "type":"proj", "special":"explode", "price":1000, "description":"slow but strong"},
                         "Laser":{"reload":2, "damage":2, "turnspeed":2, "shotlenght":1.5, "type":"ray", "special":"ricoshet", "price":3000, "description":"slow charging but devastating on close distance"}}
GUNIMGLIST = {}
GunDir = RootDir + "\Guns"
for folder in os.listdir(GunDir):
    GUNIMGLIST[folder] = []
    for subfolder in os.listdir(GunDir + '\\\\' + folder):
        GUNIMGLIST[folder].append({"Weapon":[], "Projectile":[], "Explosion":[]})
        for img in os.listdir(GunDir + '\\\\' + folder + '\\\\' + subfolder + '\\\\' + "Weapon"):
            GUNIMGLIST[folder][int(subfolder[4])]["Weapon"].append(pygame.transform.scale(pygame.image.load(GunDir + '\\\\' + folder + '\\\\' + subfolder + '\\\\' + "Weapon" + '\\\\' + img), (GUNSIZEX, GUNSIZEY)))
        if GUNTYPHEMODIFIERSLIST[folder]["type"] == "proj":
            for img in os.listdir(GunDir + '\\\\' + folder + '\\\\' + subfolder + '\\\\' + "Projectile"):
                GUNIMGLIST[folder][int(subfolder[4])]["Projectile"].append(pygame.transform.scale(pygame.image.load(GunDir + '\\\\' + folder + '\\\\' + subfolder + '\\\\' + "Projectile" + '\\\\' + img), (PROJSIZEX, PROJSIZEY)))
            for img in os.listdir(GunDir + '\\\\' + folder + '\\\\' + subfolder + '\\\\' + "Explosion"):
                GUNIMGLIST[folder][int(subfolder[4])]["Explosion"].append(pygame.transform.scale(pygame.image.load(GunDir + '\\\\' + folder + '\\\\' + subfolder + '\\\\' + "Explosion" + '\\\\' + img), (EXPLSIZEX, EXPLSIZEY)))
print(GUNIMGLIST)


global GOLDAMOUNT
GOLDAMOUNT = 0


WHITE = (255,255,255)
BLUE = (0, 150, 255)
GREEN = (0, 255, 0)
targxcor = 1200
targycor = 300
targhealth = BASEHEALTH
aimed = 0
DispCord = 0
UpgradeOpen = 0
UpgradeGunOpen = 0
xmouse = 0
ymouse = 0



DeathImg = pygame.image.load(RootDir + "\\\\" + 'Death.png')
DEATHIMGLIST = []
SHIFTLIST = []
for i in range(0,30):
    if i <= 15:
        DEATHIMGLIST.append(pygame.transform.scale(DeathImg, (40 + i*2,40 + i*2)))
        SHIFTLIST.append(int(i*1.5))
    else:
        DEATHIMGLIST.append(pygame.transform.scale(DeathImg, (100 - i*2,100 - i*2)))
        SHIFTLIST.append(int(45 - int(i*1.5)))

TelImg = pygame.image.load(RootDir + "\\\\" + 'Teleport.png')
TELIMGLIST = []
for i in range(0,30):
    if i <= 15:
        TELIMGLIST.append(pygame.transform.rotate(pygame.transform.scale(TelImg, (40 + i*2,40 + i*2)), i*5))
    else:
        TELIMGLIST.append(pygame.transform.rotate(pygame.transform.scale(TelImg, (100 - i*2,100 - i*2)), 65 - i*5))




WALLPOS = DISPLAYLENGHT/4-20
WALLENGHT = 140
WallImg = pygame.image.load(RootDir + "\\\\" + 'Wall.png')
WallImg = pygame.transform.scale(WallImg, (50,WALLENGHT))

FieldImg = pygame.image.load(RootDir + "\\\\" + 'Field.jpg')
FieldImg = pygame.transform.scale(FieldImg, (int(DISPLAYLENGHT-DISPLAYLENGHT/4),DISPLAYHEIGHT))

CityImg1 = pygame.image.load(RootDir + "\\\\" + 'City1.png')
CityImg1 = pygame.transform.scale(CityImg1, (100,100))
CityImg2 = pygame.image.load(RootDir + "\\\\" + 'City2.png')
CityImg2 = pygame.transform.scale(CityImg2, (100,100))
CityImg3 = pygame.image.load(RootDir + "\\\\" + 'City3.png')
CityImg3 = pygame.transform.scale(CityImg3, (100,100))
CityBackImg = pygame.image.load(RootDir + "\\\\" + 'CityBack.jpg')
CityBackImg = pygame.transform.scale(CityBackImg, (int(DISPLAYLENGHT/4),DISPLAYHEIGHT))

UpdBakground = pygame.image.load(RootDir + "\\\\" + 'UpdBakground.jpg')
FONT = pygame.font.Font('freesansbold.ttf', 12)
BIGFONT = pygame.font.Font('freesansbold.ttf', 20)



## Mob class
class Mob(object):

    def __init__(self):
        self.xcor = 0
        self.ycor = 0
        self.teletime = 0
        self.deathtime = 0
        self.revxcor = 0
        self.revycor = 0
        self.targetby = 0
        self.MobImgList = MOBIMGLIST
        self.alive = 0
        self.curhealth = 10
        self.speed = 1
        self.xcor = 1000
        self.ycor = 500
        self.number = len(MOBLIST)

    def Spawn(self, size, health, speed, gold):
        self.curhealth = health
        self.maxhealth = health
        self.gold = gold
        self.speed = speed
        self.size = size
        self.alive = 1
        self.xcor = DISPLAYLENGHT - 20
        self.ycor = random.randrange(1, DISPLAYHEIGHT - 100, 1)
        self.image = random.randrange(0, len(MOBIMGLIST[self.size]), 1)

    def damage(self,damag):
        if damag < self.curhealth:
            self.curhealth -= damag
        else:
            self.curhealth = 0
            self.splatted = 1
            for splat in SPLATLIST:
                if splat.deathtime == 0 and splat.teletime == 0:
                    splat.splatspavn(30, 0, self.xcor + 30, self.ycor + 40)
                    self.splatted = 0
            if self.splatted == 1:
                SPLATLIST.append(Splat())
                SPLATLIST[len(SPLATLIST)-1].splatspavn(30, 0, self.xcor + 30, self.ycor + 40)
                self.splatted = 0
            self.alive = 2
            global GOLDAMOUNT
            GOLDAMOUNT += self.gold
            self.targetby = 0
        return self.curhealth

        ## Mob life cycle
    def live(self):
        ## Killed or hitted the wall
        if self.xcor <= WALLPOS+50:
            self.splatted = 1
            for splat in SPLATLIST:
                if splat.deathtime == 0 and splat.teletime == 0:
                    splat.splatspavn(0, 30, self.xcor + 30, self.ycor + 40)
                    self.splatted = 0
            if self.splatted == 1:
                SPLATLIST.append(Splat())
                SPLATLIST[len(SPLATLIST)-1].splatspavn(0, 30, self.xcor + 30, self.ycor + 40)
                self.splatted = 0
            self.alive = 3
            if GOLDAMOUNT > self.gold:
                GOLDAMOUNT -= self.gold
            else:
                GOLDAMOUNT = 0
            self.targetby = 0
        ## Move forward
        else:
            self.xcor -= self.speed
        ## Show health
        pygame.draw.line(DISPLAYSURF, (200, 0, 0), (self.xcor-1, self.ycor-3), (self.xcor+int((float(self.curhealth)/float(self.maxhealth))*49), self.ycor-3), 6)
        DISPLAYSURF.blit(MOBIMGLIST[self.size][self.image][int(FRAMENUMB/(FPS/len(MOBIMGLIST[self.size][self.image])))-1], (self.xcor, self.ycor))



class Splat(object):
    def __init__(self):
        pass

    def splatspavn(self, deathtime, teletime, revxcor, revycor):
        self.deathtime = deathtime
        self.teletime = teletime
        self.revxcor = revxcor
        self.revycor = revycor

    def splatwork(self):
        if self.deathtime > 0:
            DISPLAYSURF.blit(DEATHIMGLIST[self.deathtime-1], (self.revxcor - SHIFTLIST[self.deathtime-1], self.revycor - SHIFTLIST[self.deathtime-1]))
            self.deathtime -=1
        ## Wall hit animation
        elif self.teletime > 0:
            DISPLAYSURF.blit(TELIMGLIST[self.teletime-1], (self.revxcor - SHIFTLIST[self.teletime-1], self.revycor - SHIFTLIST[self.teletime-1]))
            self.teletime -= 1




class Mobwave(object):
    def __init__(self,BASESPEED, BASEHEALTH, BASEGOLD, SPEEDPERLV, HEALTHPERLV, GOLDPERLV, WAVETIMER, BASEMOBCOUNT, MOBPERWAVE, FASTCHANSE, BIGCHANSE):
        self.wavelevel = 1
        self.wavetimer = WAVETIMER
        self.timeto = 0
        self.basemobcount = BASEMOBCOUNT
        self.mobperwave = MOBPERWAVE
        self.fastchanse = FASTCHANSE
        self.bigchanse = BIGCHANSE
        self.basespeed = BASESPEED
        self.basehealth = BASEHEALTH
        self.basegold = BASEGOLD
        self.speedperlv = SPEEDPERLV
        self.healthperlv = HEALTHPERLV
        self.goldperlv = GOLDPERLV
        self.wavemobcount = 0
        self.wavemobhealth = 0
        self.normalmobs = 0
        self.fastmobs = 0
        self.bigmobs = 0

    def wavespavn(self):
        self.wavemobcount = 0
        self.wavemobhealth = 0
        self.normalmobs = 0
        self.fastmobs = 0
        self.bigmobs = 0
        self.i = 0
        while self.i < self.basemobcount + self.wavelevel*self.mobperwave:
            self.dice = random.randrange(-1, self.wavelevel, 1)
            if self.dice < self.fastchanse:
                self.i += 2
                self.size = "Normal"
                self.normalmobs += 1
            elif self.dice < self.bigchanse:
                self.i += 1
                self.size = "Small"
                self.fastmobs += 1
            else:
                self.i += 3
                self.size = "Big"
                self.bigmobs += 1
            try:
                MOBLIST[self.wavemobcount].Spawn(self.size, int((self.basehealth + self.healthperlv*self.wavelevel)*SIZEMODIFIERLIST[self.size]["health"]), int((self.basespeed + self.speedperlv*self.wavelevel)*SIZEMODIFIERLIST[self.size]["speed"]), int((self.basegold + self.goldperlv*self.wavelevel)*SIZEMODIFIERLIST[self.size]["gold"]))
                self.wavemobhealth += MOBLIST[self.wavemobcount].curhealth
                self.wavemobcount += 1
            except IndexError:
                MOBLIST.append(Mob())
                MOBLIST[self.wavemobcount].Spawn(self.size, int((self.basehealth + self.healthperlv*self.wavelevel)*SIZEMODIFIERLIST[self.size]["health"]), int((self.basespeed + self.speedperlv*self.wavelevel)*SIZEMODIFIERLIST[self.size]["speed"]), int((self.basegold + self.goldperlv*self.wavelevel)*SIZEMODIFIERLIST[self.size]["gold"]))
                self.wavemobhealth += MOBLIST[self.wavemobcount].curhealth
                self.wavemobcount += 1

    def wavework(self):
        if self.timeto > 0:
            TIME = BIGFONT.render("Time to next wave: " + str(int(self.timeto/30)) + "sec", True, (100, 100, 0), (255, 255, 255))
            DISPLAYSURF.blit(TIME, (600, 10))
            TIME = FONT.render("Enemies in wave: normal " + str(self.normalmobs) + "   fast " + str(self.fastmobs) + "   big " + str(self.bigmobs), True, (100, 100, 0), (255, 255, 255))
            DISPLAYSURF.blit(TIME, (600, 35))
            self.timeto -= 1
        elif self.wavemobcount == 0:
            if GOLDAMOUNT == 0:
                self.wavelevel -= 1
            elif self.killed > self.reached:
                self.wavelevel += 1
            self.wavespavn()
            self.killed = 0
            self.reached = 0
            self.timeto = self.wavetimer
        else:
            WAVEINFO = BIGFONT.render("WAVE LEVEL" + str(self.wavelevel), True, (100, 100, 0), (255, 255, 255))
            DISPLAYSURF.blit(WAVEINFO, (600, 10))
            WAVEINFO = FONT.render("Enemies alive: " + str(self.wavemobcount), True, (100, 100, 0), (255, 255, 255))
            DISPLAYSURF.blit(WAVEINFO, (600, 35))
            for mob in MOBLIST:
                if mob.alive == 1:
                    mob.live()
                elif mob.alive == 2:
                    self.wavemobcount -= 1
                    mob.alive = 0
                    self.killed += 1
                elif mob.alive == 3:
                    self.wavemobcount -= 1
                    mob.alive = 0
                    self.reached += 1



## Gun class
class Gun (object):
    def __init__(self,GUNXPOS, GUNYPOS, GUNDAMAGE, BASEGUNCHARGE, GUNTURNSPEED, SHOTLENGHT, GunNum):
        self.GunXpos=GUNXPOS
        self.GunYpos=GUNYPOS
        self.ChargeToShoot = BASEGUNCHARGE
        self.GunTurnSpeed = GUNTURNSPEED
        self.GunDamage = GUNDAMAGE
        self.ShotLenght = SHOTLENGHT
        self.GunNum = GunNum
        self.targmob = MOBLIST[GunNum-1]
        self.shooting = 0
        self.curang = 0
        self.Guncharge = 0
        self.barrel = "Bow"
        self.smarttarg = 0
        self.cooptarg = 0
        self.BarrelsBought = ["Bow"]

    def gettarget(self):
        if self.smarttarg == 1:
            for cmob in MOBLIST:
             ##Target by angle and prox: cmob.xcor + math.fabs(math.atan2(self.GunYpos - cmob.ycor, cmob.xcor - self.GunXpos)*57.29 - self.curang)*0.1 < self.targmob.xcor
                if cmob.xcor < self.targmob.xcor and cmob.targetby == 0 and cmob.alive == 1:
                    self.targmob = cmob
            self.targmob.targetby = self.GunNum
            ##pygame.draw.line(DISPLAYSURF, (200, 0, 0), (self.targmob.xcor + 18, self.targmob.ycor + 60), (self.targmob.xcor + 18, self.targmob.ycor - 20), 2)
            ##pygame.draw.line(DISPLAYSURF, (200, 0, 0), (self.targmob.xcor + 60, self.targmob.ycor + 18), (self.targmob.xcor - 20, self.targmob.ycor + 18), 2)
            ##For targ dist
            ##math.sqrt((self.targxcor - self.targetmob.speed*iter2 - self.xcord)**2 + (self.targycor - self.ycord)**2)
        elif self.cooptarg == 1:
            for cmob in MOBLIST:
             ##Target by angle and prox: cmob.xcor + math.fabs(math.atan2(self.GunYpos - cmob.ycor, cmob.xcor - self.GunXpos)*57.29 - self.curang)*0.1 < self.targmob.xcor
                if cmob.xcor < self.targmob.xcor and cmob.targetby == 0 and cmob.alive == 1:
                    self.targmob = cmob
            self.targmob.targetby = self.GunNum
            ##pygame.draw.line(DISPLAYSURF, (200, 0, 0), (self.targmob.xcor + 18, self.targmob.ycor + 60), (self.targmob.xcor + 18, self.targmob.ycor - 20), 2)
            ##pygame.draw.line(DISPLAYSURF, (200, 0, 0), (self.targmob.xcor + 60, self.targmob.ycor + 18), (self.targmob.xcor - 20, self.targmob.ycor + 18), 2)
            ##For targ dist
            ##math.sqrt((self.targxcor - self.targetmob.speed*iter2 - self.xcord)**2 + (self.targycor - self.ycord)**2)
        else:
            for cmob in MOBLIST:
             ##Target by angle and prox: cmob.xcor + math.fabs(math.atan2(self.GunYpos - cmob.ycor, cmob.xcor - self.GunXpos)*57.29 - self.curang)*0.1 < self.targmob.xcor
                if cmob.xcor < self.targmob.xcor and cmob.targetby == 0 and cmob.alive == 1:
                    self.targmob = cmob
            self.targmob.targetby = self.GunNum
            ##pygame.draw.line(DISPLAYSURF, (200, 0, 0), (self.targmob.xcor + 18, self.targmob.ycor + 60), (self.targmob.xcor + 18, self.targmob.ycor - 20), 2)
            ##pygame.draw.line(DISPLAYSURF, (200, 0, 0), (self.targmob.xcor + 60, self.targmob.ycor + 18), (self.targmob.xcor - 20, self.targmob.ycor + 18), 2)
            ##For targ dist
            ##math.sqrt((self.targxcor - self.targetmob.speed*iter2 - self.xcord)**2 + (self.targycor - self.ycord)**2)

    def gunwork(self):
        ## Targeting
        if self.targmob.alive != 1:
            self.gettarget()

        ## Gun mechanism
        if self.shooting > 0:
            if GUNTYPHEMODIFIERSLIST[self.barrel]["type"] == "ray":
                pygame.draw.line(DISPLAYSURF, BLUE, (self.GunXpos+GUNSIZEX/2, self.GunYpos+GUNSIZEY/2), (self.lastshotxcor, self.lastshotycor), int((4+int(self.shotpower*5)) * self.shooting/self.ShotLenght))
            self.shooting -= 1
        else:
            self.targang = math.atan2(self.GunYpos + GUNSIZEY/2 - self.targmob.ycor - 25, self.targmob.xcor + 40 - self.GunXpos - GUNSIZEX/2)*57.29
            if math.fabs(self.targang - self.curang) > self.GunTurnSpeed:
                ##if self.GunNum == 2:
                    ##print(str(math.atan2(self.GunYpos - self.targmob.ycor, self.targmob.xcor - self.GunYpos)*57.29) + " minus " + str(self.curang) + "viil be" + str(math.fabs(math.atan2(self.GunYpos - self.targmob.ycor, self.targmob.xcor - self.GunYpos)*57.29 - self.targang)))
                if self.targang - self.curang > 0:
                    ##if self.GunNum == 2:
                        ##print("rotleft")
                    self.curang += self.GunTurnSpeed
                else:
                    ##if self.GunNum == 2:
                        ##print("rotright")
                    self.curang -= self.GunTurnSpeed
            else:
                ##if self.GunNum == 2:
                    ##print("jump")
                self.curang = self.targang
                if self.Guncharge >= self.ChargeToShoot and self.targmob.alive == 1:
                    print (GUNTYPHEMODIFIERSLIST[self.barrel]["type"])
                    if GUNTYPHEMODIFIERSLIST[self.barrel]["type"] == "ray":
                        self.shotpower = 2.3 - ((math.sqrt((self.targmob.xcor - self.GunXpos)**2 + (self.targmob.ycor - self.GunYpos)**2))/400)
                        ##print("distance " + str(math.sqrt((self.targmob.xcor - self.GunXpos)**2 + (self.targmob.ycor - self.GunYpos)**2)) + "   power " + str(self.shotpower))
                        pygame.draw.line(DISPLAYSURF, BLUE, (self.GunXpos+GUNSIZEX/2, self.GunYpos+GUNSIZEY/2), (self.targmob.xcor+25, self.targmob.ycor+40), 4+int(self.shotpower*5))
                        if self.shotpower > 1:
                            pygame.draw.line(DISPLAYSURF, WHITE, (self.GunXpos+GUNSIZEX/2, self.GunYpos+GUNSIZEY/2), (self.targmob.xcor+25, self.targmob.ycor+40), 3)
                        self.targmob.damage(int(self.GunDamage * self.shotpower))
                    elif  GUNTYPHEMODIFIERSLIST[self.barrel]["type"] == "proj":
                        iter1=2
                        iter2=0
                        while math.fabs(iter1 - iter2) > 0.5:
                            iter1 = math.sqrt((self.targxcor - self.targetmob.speed*iter2 - self.xcord)**2 + (self.targycor - self.ycord)**2)/projspeed
                            iter2 = math.sqrt((self.targxcor - self.targetmob.speed*iter1 - self.xcord)**2 + (self.targycor - self.ycord)**2)/projspeed
                        self.flytime = int(iter2)
                        self.targxcor = int(targxcor - self.targetmob.speed*self.flytime)
                        self.xspeed = int((self.targxcor - self.xcord)/self.flytime)
                        self.yspeed = int((self.targycor - self.ycord)/self.flytime)
                        shoted = 1
                        for shot in PROJLIST:
                            if shot.onfly == 0 and shot.explodetime == 0 and shoted == 1:
                                launch(GUNIMGLIST[self.barrel][AGE]["Projectile"], GUNIMGLIST[self.barrel][AGE]["Explosion"], "xcord", "ycord", targxcor, targycor, xspeed, yspeed, angle, damage, exploderad)
                                shot.launch(0, self.GunXpos+GUNSIZEX/2, self.GunYpos+GUNSIZEY/2, self.targmob.xcor+25, self.targmob.ycor+40, 20, self.targmob, self.GunDamage, PROJECTIMGLIST)
                                shoted = 0
                        if shoted == 1:
                            PROJLIST.append(projectile())
                            PROJLIST[len(PROJLIST)-1].launch(0, self.GunXpos+60, self.GunYpos+40, self.targmob.xcor, self.targmob.ycor, 20, self.targmob, self.GunDamage, PROJECTIMGLIST)
                            shoted = 0
                    self.shooting = self.ShotLenght
                    self.lastshotxcor = self.targmob.xcor+25
                    self.lastshotycor = self.targmob.ycor+40
                    self.Guncharge = 0
                else:
                    if self.Guncharge < self.ChargeToShoot:
                        self.Guncharge += 1
        ##pygame.draw.line(DISPLAYSURF, (0, 200, 0, 50), (self.GunXpos, self.GunYpos), (self.GunXpos+int(math.sqrt((self.targmob.xcor-self.GunXpos)**2 + (self.GunYpos - self.targmob.ycor)**2)*math.cos(math.fabs(math.atan2(self.GunYpos - self.targmob.ycor, self.targmob.xcor-self.GunXpos)))),    self.GunYpos-int(math.sqrt((self.targmob.xcor-self.GunXpos)**2 + (self.GunYpos - self.targmob.ycor)**2)*math.sin(math.atan2(self.GunYpos - self.targmob.ycor, self.targmob.xcor-self.GunXpos)))), 8)
        ##if self.GunNum == 2:
            ##print ("Gun: " + str(self.GunNum) + "   Gun angle: " + str(self.curang) + "   Target angle: " + str(math.atan2(self.GunYpos - self.targmob.ycor, self.targmob.xcor - self.GunXpos)*57.29))
        ##For shifting gun so center is immovable
        anglerad = math.fabs(self.curang/57.29)
        a = GUNSIZEX*math.cos(anglerad)
        b = GUNSIZEX*math.sin(anglerad)
        c = GUNSIZEY*math.cos(anglerad)
        d = GUNSIZEY*math.sin(anglerad)
        if self.curang >= 0:
            Y2 = self.GunYpos + b + c
            X2 = self.GunXpos + d
            Y1 = self.GunYpos
            X1 = self.GunXpos + a
            Yc = int(Y1 + (Y2 - Y1)/2)
            Xc = int(X2 + (X1 - X2)/2)
            dY = Yc - self.GunYpos - GUNSIZEY/2
            dX = Xc - self.GunXpos - GUNSIZEX/2
        else:
            Y2 = self.GunYpos + b + c
            X2 = self.GunXpos + a
            Y1 = self.GunYpos
            X1 = self.GunXpos + d
            Yc = int(Y1 + (Y2 - Y1)/2)
            Xc = int(X1 + (X2 - X1)/2)
            dY = Yc - self.GunYpos - GUNSIZEY/2
            dX = Xc - self.GunXpos - GUNSIZEX/2

        ##pygame.draw.line(DISPLAYSURF, (200, 0, 0), (self.GunXpos+GUNSIZEX/2, self.GunYpos+GUNSIZEY/2), (self.targmob.xcor +25, self.targmob.ycor +40), 4)
        DISPLAYSURF.blit(pygame.transform.rotate(GUNIMGLIST[self.barrel][AGE]["Weapon"][int(self.Guncharge/(self.ChargeToShoot/len(GUNIMGLIST[self.barrel][AGE]["Weapon"])))-1], self.curang), (self.GunXpos - dX, self.GunYpos - dY))
        NUMB = FONT.render(str(self.GunNum), True, (100, 100, 0), (255, 255, 255))
        DISPLAYSURF.blit(NUMB, (self.GunXpos, self.GunYpos))


    def gunidle(self):
        self.targang = 0
        self.shooting = 0
        if math.fabs(self.targang - self.curang) > self.GunTurnSpeed:
                if self.targang - self.curang > 0:
                    self.curang += self.GunTurnSpeed
                else:
                    self.curang -= self.GunTurnSpeed
        else:
            self.curang = self.targang
        anglerad = math.fabs(self.curang/57.29)
        a = GUNSIZEX*math.cos(anglerad)
        b = GUNSIZEX*math.sin(anglerad)
        c = GUNSIZEY*math.cos(anglerad)
        d = GUNSIZEY*math.sin(anglerad)
        if self.curang >= 0:
            Y2 = self.GunYpos + b + c
            X2 = self.GunXpos + d
            Y1 = self.GunYpos
            X1 = self.GunXpos + a
            Yc = int(Y1 + (Y2 - Y1)/2)
            Xc = int(X2 + (X1 - X2)/2)
            dY = Yc - self.GunYpos - GUNSIZEY/2
            dX = Xc - self.GunXpos - GUNSIZEX/2
        else:
            Y2 = self.GunYpos + b + c
            X2 = self.GunXpos + a
            Y1 = self.GunYpos
            X1 = self.GunXpos + d
            Yc = int(Y1 + (Y2 - Y1)/2)
            Xc = int(X1 + (X2 - X1)/2)
            dY = Yc - self.GunYpos - GUNSIZEY/2
            dX = Xc - self.GunXpos - GUNSIZEX/2
        DISPLAYSURF.blit(pygame.transform.rotate(GUNIMGLIST[self.barrel][AGE]["Weapon"][int(self.Guncharge/(self.ChargeToShoot/len(GUNIMGLIST[self.barrel][AGE])))-1], self.curang), (self.GunXpos - dX, self.GunYpos - dY))
        NUMB = FONT.render(str(self.GunNum), True, (100, 100, 0), (255, 255, 255))
        DISPLAYSURF.blit(NUMB, (self.GunXpos, self.GunYpos))

    def barrelswap(self, newbarrel):
        self.ChargeToShoot = self.ChargeToShoot/GUNTYPHEMODIFIERSLIST[self.barrel]["reload"]*GUNTYPHEMODIFIERSLIST[newbarrel]["reload"]
        self.GunDamage = self.GunDamage/GUNTYPHEMODIFIERSLIST[self.barrel]["damage"]*GUNTYPHEMODIFIERSLIST[newbarrel]["damage"]
        self.GunTurnSpeed = self.GunTurnSpeed/GUNTYPHEMODIFIERSLIST[self.barrel]["turnspeed"]*GUNTYPHEMODIFIERSLIST[newbarrel]["turnspeed"]
        self.ShotLenght = self.ShotLenght/GUNTYPHEMODIFIERSLIST[self.barrel]["shotlenght"]*GUNTYPHEMODIFIERSLIST[newbarrel]["shotlenght"]
        self.barrel = newbarrel



class projectile(object):
    def __init__(self):
        self.projThype = 0
        self.xcord = 0
        self.ycord = 0
        self.targxcor = 0
        self.targycor = 0
        self.xspeed = 0
        self.yspeed = 0
        self.flytime = 0
        self.explodetime = 0
        self.angle = 0
        self.onfly = 0

    def launch(self, projimg, explodeimg, xcord, ycord, targxcor, targycor, xspeed, yspeed, angle, damage, exploderad):
        self.projimg = projimg
        self.explodeimg = explodeimg
        self.xcord = xcord
        self.ycord = ycord
        self.targxcor = targxcor
        self.targycor = targycor
        self.exploderad = exploderad
        self.damage = damage
        self.onfly = 1
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.angle = angle

    def fly(self):
        if self.onfly > 0:
            DISPLAYSURF.blit(pygame.transform.rotate(self.projimg, self.angle), (self.xcord, self.ycord))
            self.ycord += self.yspeed
            self.xcord += self.xspeed
            for mob in MOBLIST:
                if mob.alive == 1:
                    if math.sqrt((self.xcord - mob.xcor)**2 + (self.ycord - mob.ycor)**2) < self.exploderad:
                        self.onfly = 0
                        mob.damage(self.damage)
                        self.explodetime = 10
        elif self.explodetime > 0:
            DISPLAYSURF.blit(pygame.transform.scale(self.explodeimg[int(self.explodetime/(10/len(self.explodeimg)))-1], (self.exploderad*(1 - self.explodetime*0.05),self.exploderad*(1 - self.explodetime*0.05))), (self.xcor, self.ycor))
            self.explodetime -= 1
        ##pygame.draw.line(DISPLAYSURF, (0, 100, 0), (self.targxcor - 10, self.targycor), (self.targxcor + 10, self.targycor), 2)
        ##pygame.draw.line(DISPLAYSURF, (0, 100, 0), (self.targxcor, self.targycor + 10), (self.targxcor, self.targycor - 10), 2)



## Create list of guns
gunlist = []
for i in range(0,BASEGUNCOUNT):
    MOBLIST.append(Mob())
    gunlist.append(Gun((WALLPOS - GUNSIZEX/2), (DISPLAYHEIGHT/(BASEGUNCOUNT+1)*(i+1)), GUNDAMAGE, BASEGUNCHARGE, GUNTURNSPEED, SHOTLENGHT, i+1))


mobwave = Mobwave(BASESPEED, BASEHEALTH, BASEGOLD, SPEEDPERLV, HEALTHPERLV, GOLDPERLV, WAVETIMER, BASEMOBCOUNT, MOBPERWAVE, FASTCHANSE, BIGCHANSE)



## Main game screen function
def MainGame(DISPLAYSURF, WALLPOS, GOLDAMOUNT, MOBLIST, FONT, DispCord, xmouse, ymouse, MOBIMGLIST, mobwave):
    ##statik objects display
    DISPLAYSURF.blit(FieldImg, (DISPLAYLENGHT/4, 0))

    DISPLAYSURF.blit(CityBackImg, (0, 0))
    DISPLAYSURF.blit(CityImg1, (50, 100))
    DISPLAYSURF.blit(CityImg2, (70, 300))
    DISPLAYSURF.blit(CityImg3, (40, 400))

    for i in range(0,int(DISPLAYHEIGHT/WALLENGHT)+1):
        DISPLAYSURF.blit(WallImg, (WALLPOS, i*WALLENGHT+1))
    GOLD = FONT.render("GOLD: " + str(GOLDAMOUNT), True, (100, 100, 0), (255, 255, 255))
    DISPLAYSURF.blit(GOLD, (10, 10))
    UPGRADEBUTTON = FONT.render("UPGRADES", True, (100, 100, 0), (200, 200, 200))
    DISPLAYSURF.blit(UPGRADEBUTTON, (10, 25))

    ##Mob animation
    mobwave.wavework()

    ## Gun animation
    if mobwave.wavemobcount == 0 or mobwave.timeto > 0:
        for gun in gunlist:
            gun.gunidle()
    else:
        for gun in gunlist:
            gun.gunwork()
    ## Mob death animation
    for splat in SPLATLIST:
        if splat.deathtime > 0 or splat.teletime > 0:
            splat.splatwork()

    ## Projectile animation
    for shot in PROJLIST:
        if shot.onfly == 1 or shot.explodetime > 0:
            shot.fly()



## Update screen function
def UpgradeScreen(DISPLAYSURF, GOLDAMOUNT, FONT):
    ##statik objects display
    DISPLAYSURF.blit(UpdBakground, (0, 0))
    GOLD = FONT.render("GOLD: " + str(GOLDAMOUNT), True, (100, 100, 0), (255, 255, 255))
    DISPLAYSURF.blit(GOLD, (10, 10))
    BACKBUTTON = FONT.render("BACK", True, (100, 100, 0), (200, 200, 200))
    DISPLAYSURF.blit(BACKBUTTON, (1100, 10))
    UPGRADEGUN = BIGFONT.render("UPGRADE GUN", True, (100, 100, 0), (200, 200, 200))
    DISPLAYSURF.blit(UPGRADEGUN, (10, 50))



## Gun upgrade screen
def GunUpgradeScreen():
    DISPLAYSURF.blit(UpdBakground, (0, 0))

# Field map
    pygame.draw.rect(DISPLAYSURF, (100, 100, 100), (gunlist[CHOOSENGUN].GunXpos + 795, int(gunlist[CHOOSENGUN].GunYpos/1.5)+95, GUNSIZEX+10, GUNSIZEY+10))
    for gun in gunlist:
        DISPLAYSURF.blit(GUNIMGLIST[gun.barrel][AGE]["Weapon"][len(GUNIMGLIST[gun.barrel][AGE]["Weapon"])-1], (gun.GunXpos + 800, int(gun.GunYpos/1.5)+100))
        GUNINF = FONT.render(gun.barrel + "  Dam: " + str(gun.GunDamage) + "  Rel: " + str(round(30.0/gun.ChargeToShoot, 2)) + "  Turn: " + str(gun.GunTurnSpeed), True, (100, 100, 0), (255, 255, 255))
        DISPLAYSURF.blit(GUNINF, (gun.GunXpos + 750, int(gun.GunYpos/1.5) + 100 + GUNSIZEY + 5))

#gold amount
    GOLD = FONT.render("GOLD: " + str(GOLDAMOUNT), True, (100, 100, 0), (255, 255, 255))
    DISPLAYSURF.blit(GOLD, (10, 10))
#BACKBUTTON
    BACKBUTTON = FONT.render("BACK", True, (100, 100, 0), (200, 200, 200))
    DISPLAYSURF.blit(BACKBUTTON, (1100, 10))
#damage up
    UPGRADEDAMAGE = BIGFONT.render("UPGRADE GUN DAMAGE", True, (100, 100, 0), (200, 200, 200))
    DISPLAYSURF.blit(UPGRADEDAMAGE, (10, 40))
    UPGRADEDAMAGE = FONT.render("from: " + str(gunlist[CHOOSENGUN].GunDamage) + "   to: " + str(gunlist[CHOOSENGUN].GunDamage*2) + "   for " + str(gunlist[CHOOSENGUN].GunDamage*20/GUNTYPHEMODIFIERSLIST[gunlist[CHOOSENGUN].barrel]["damage"]) + " GOLD" , True, (100, 100, 0), (200, 200, 200))
    DISPLAYSURF.blit(UPGRADEDAMAGE, (10, 60))
# reload up
    if gunlist[CHOOSENGUN].ChargeToShoot/GUNTYPHEMODIFIERSLIST[gunlist[CHOOSENGUN].barrel]["reload"] > 10:
        UPGRADERELOAD = BIGFONT.render("UPGRADE GUN RELOAD", True, (100, 100, 0), (200, 200, 200))
        DISPLAYSURF.blit(UPGRADERELOAD, (10, 80))
        UPGRADERELOAD = FONT.render("from: " + str(round(30.0/gunlist[CHOOSENGUN].ChargeToShoot, 2)) + "/s   to: " + str(round(30.0/(gunlist[CHOOSENGUN].ChargeToShoot-5), 2)) + "/s   for " + str(((55 - gunlist[CHOOSENGUN].ChargeToShoot/GUNTYPHEMODIFIERSLIST[gunlist[CHOOSENGUN].barrel]["reload"])**2)*8) + " GOLD" , True, (100, 100, 0), (200, 200, 200))
        DISPLAYSURF.blit(UPGRADERELOAD, (10, 100))
    else:
        UPGRADERELOAD = BIGFONT.render("GUN RELOAD MAXED", True, (100, 100, 0), (200, 200, 200))
        DISPLAYSURF.blit(UPGRADERELOAD, (10, 80))
        UPGRADERELOAD = FONT.render("on:" + str(round(30.0/gunlist[CHOOSENGUN].ChargeToShoot, 2)) + "/s" , True, (100, 100, 0), (200, 200, 200))
        DISPLAYSURF.blit(UPGRADERELOAD, (10, 100))
#turnspeed up
    if gunlist[CHOOSENGUN].GunTurnSpeed/GUNTYPHEMODIFIERSLIST[gunlist[CHOOSENGUN].barrel]["turnspeed"] < 5:
        UPGRADESPEED = BIGFONT.render("UPGRADE GUN TURN SPEED", True, (100, 100, 0), (200, 200, 200))
        DISPLAYSURF.blit(UPGRADESPEED, (10, 120))
        UPGRADESPEED = FONT.render("from: " + str(gunlist[CHOOSENGUN].GunTurnSpeed) + "grad/s   to: " + str(gunlist[CHOOSENGUN].GunTurnSpeed + 1) + "grad/s   for " + str(((gunlist[CHOOSENGUN].GunTurnSpeed/GUNTYPHEMODIFIERSLIST[gunlist[CHOOSENGUN].barrel]["turnspeed"])**2)*200) + " GOLD" , True, (100, 100, 0), (200, 200, 200))
        DISPLAYSURF.blit(UPGRADESPEED, (10, 140))
    else:
        UPGRADESPEED = BIGFONT.render("GUN TURN SPEED MAXED", True, (100, 100, 0), (200, 200, 200))
        DISPLAYSURF.blit(UPGRADESPEED, (10, 120))
        UPGRADESPEED = FONT.render("on:" + str(gunlist[CHOOSENGUN].GunTurnSpeed) + "grad/s" , True, (100, 100, 0), (200, 200, 200))
        DISPLAYSURF.blit(UPGRADESPEED, (10, 140))
# More guns
    if len(gunlist) < 5:
        UPGRADECOUNT = BIGFONT.render("ADD NEW GUN", True, (100, 100, 0), (200, 200, 200))
        DISPLAYSURF.blit(UPGRADECOUNT, (10, 160))
        UPGRADECOUNT = FONT.render("for " + str((len(gunlist)**2)*2000) + " GOLD" , True, (100, 100, 0), (200, 200, 200))
        DISPLAYSURF.blit(UPGRADECOUNT, (10, 180))
    else:
        UPGRADECOUNT = BIGFONT.render("GUN COUNT MAXED", True, (100, 100, 0), (200, 200, 200))
        DISPLAYSURF.blit(UPGRADECOUNT, (10, 160))
        UPGRADECOUNT = FONT.render("on:" + str(len(gunlist)), True, (100, 100, 0), (200, 200, 200))
        DISPLAYSURF.blit(UPGRADECOUNT, (10, 180))
# barrels
    for guntype in GUNTYPHELIST:
        if guntype not in gunlist[CHOOSENGUN].BarrelsBought:
            BARREL = BIGFONT.render("Buy " + guntype + " barrel", True, (100, 100, 0), (200, 200, 200))
            DISPLAYSURF.blit(BARREL, (10, 400))
            BARREL = FONT.render(GUNTYPHEMODIFIERSLIST[guntype]["description"] + "for: " + str(GUNTYPHEMODIFIERSLIST[guntype]["price"]) + " GOLD", True, (100, 100, 0), (200, 200, 200))
            DISPLAYSURF.blit(BARREL, (10, 420))
            DISPLAYSURF.blit(GUNIMGLIST[guntype][AGE]["Weapon"][len(GUNIMGLIST[guntype][AGE]["Weapon"])-1], (10, 440))
            break
    i = 0
    for guntype in gunlist[CHOOSENGUN].BarrelsBought:
            BARREL = BIGFONT.render("Intstall " + guntype + " barrel", True, (100, 100, 0), (200, 200, 200))
            DISPLAYSURF.blit(BARREL, (500, 20 + i*(GUNSIZEY+40)))
            BARREL = FONT.render(GUNTYPHEMODIFIERSLIST[guntype]["description"], True, (100, 100, 0), (200, 200, 200))
            DISPLAYSURF.blit(BARREL, (500, 40 + i*(GUNSIZEY+40)))
            DISPLAYSURF.blit(GUNIMGLIST[guntype][AGE]["Weapon"][len(GUNIMGLIST[guntype][AGE]["Weapon"])-1], (500, 50 + i*(GUNSIZEY+40)))
            i += 1



##CORE GAME CYCLE
while True:
    if UpgradeOpen == 1:
        if UpgradeGunOpen == 1:
            GunUpgradeScreen()
        else:
            UpgradeScreen(DISPLAYSURF, GOLDAMOUNT, FONT)
    else:
        MainGame(DISPLAYSURF,WALLPOS, GOLDAMOUNT, MOBLIST, FONT, DispCord, xmouse, ymouse, MOBIMGLIST, mobwave)
    ## For debug
    if DispCord == 1:
        COORDS = FONT.render("xmouse: " + str(xmouse) + "   ymouse: " + str(ymouse) + "   upgradeopen " + str(UpgradeOpen), True, (0, 100, 100), WHITE)
        DISPLAYSURF.blit(COORDS, (600, 580))
    if FRAMENUMB == 30:
        FRAMENUMB = 1
    else:
        FRAMENUMB += 1


        ## Control mechanic
    for event in pygame.event.get():
        if pygame.mouse.get_pressed()[0]:
                DispCord = 1
                xmouse = pygame.mouse.get_pos()[0]
                ymouse = pygame.mouse.get_pos()[1]
            # For debug
                if pygame.mouse.get_pos()[0] > 1100 and pygame.mouse.get_pos()[0] < 1200 and pygame.mouse.get_pos()[1] > 500 and pygame.mouse.get_pos()[1] < 600:
                    GOLDAMOUNT += 10000
                    print(GUNTYPHEMODIFIERSLIST[GUNTYPHELIST[len(gunlist[CHOOSENGUN].BarrelsBought)-1]])
            # open upgrade menu
                if UpgradeOpen == 0:
                    if pygame.mouse.get_pos()[0] > 9 and pygame.mouse.get_pos()[0]<81 and pygame.mouse.get_pos()[1] > 26 and pygame.mouse.get_pos()[1] < 37:
                        UpgradeOpen = 1
            # in upgrade menu
                else:
                    # back button
                    if pygame.mouse.get_pos()[0] > 1100 and pygame.mouse.get_pos()[0] < 1136 and pygame.mouse.get_pos()[1] > 10 and pygame.mouse.get_pos()[1] < 22:
                        if UpgradeGunOpen == 1:
                            UpgradeGunOpen = 0
                        else:
                            UpgradeOpen = 0
                    # in gun upgrade menu
                    if UpgradeGunOpen == 1:
                        #damage up
                        if pygame.mouse.get_pos()[0] > 10 and pygame.mouse.get_pos()[0] < 262 and pygame.mouse.get_pos()[1] > 40 and pygame.mouse.get_pos()[1] < 80 and GOLDAMOUNT>=gunlist[CHOOSENGUN].GunDamage*20:
                            GOLDAMOUNT -= gunlist[CHOOSENGUN].GunDamage*20
                            gunlist[CHOOSENGUN].GunDamage = gunlist[CHOOSENGUN].GunDamage*2
                        #reload up
                        if pygame.mouse.get_pos()[0] > 10 and pygame.mouse.get_pos()[0] < 262 and pygame.mouse.get_pos()[1] > 80 and pygame.mouse.get_pos()[1] < 120 and gunlist[CHOOSENGUN].ChargeToShoot > 10 and GOLDAMOUNT>=((55 - gunlist[CHOOSENGUN].ChargeToShoot)**2)*8:
                            GOLDAMOUNT -= ((55 - gunlist[CHOOSENGUN].ChargeToShoot)**2)*8
                            gunlist[CHOOSENGUN].ChargeToShoot -= 5
                        #speed up
                        if pygame.mouse.get_pos()[0] > 10 and pygame.mouse.get_pos()[0] < 262 and pygame.mouse.get_pos()[1] > 120 and pygame.mouse.get_pos()[1] < 160 and gunlist[CHOOSENGUN].GunTurnSpeed < 5 and GOLDAMOUNT>=(gunlist[0].GunTurnSpeed**2)*200:
                            GOLDAMOUNT -= (gunlist[CHOOSENGUN].GunTurnSpeed**2)*200
                            gunlist[CHOOSENGUN].GunTurnSpeed += 1
                        #more guns
                        if pygame.mouse.get_pos()[0] > 10 and pygame.mouse.get_pos()[0] < 262 and pygame.mouse.get_pos()[1] > 160 and pygame.mouse.get_pos()[1] < 200 and len(gunlist) < 5 and GOLDAMOUNT>=(len(gunlist)**2)*2000:
                            gunlist.append(Gun(100, 100, GUNDAMAGE, BASEGUNCHARGE, GUNTURNSPEED, SHOTLENGHT, len(gunlist)+1))
                            MOBLIST.append(Mob())
                            BASEGUNCOUNT += 1
                            for gun in gunlist:
                                gun.GunXpos = (WALLPOS - GUNSIZEX/2)
                                gun.GunYpos = (DISPLAYHEIGHT/(BASEGUNCOUNT+1)*(gun.GunNum))
                        # add barrel type
                        if pygame.mouse.get_pos()[0] > 10 and pygame.mouse.get_pos()[0] < 262 and pygame.mouse.get_pos()[1] > 400 and pygame.mouse.get_pos()[1] < 440 and len(gunlist[CHOOSENGUN].BarrelsBought) < len(GUNTYPHELIST) and GOLDAMOUNT>=GUNTYPHEMODIFIERSLIST[GUNTYPHELIST[len(gunlist[CHOOSENGUN].BarrelsBought)-1]]["price"]:
                            GOLDAMOUNT -= (gunlist[CHOOSENGUN].GunTurnSpeed**2)*200
                            gunlist[CHOOSENGUN].BarrelsBought.append(GUNTYPHELIST[len(gunlist[CHOOSENGUN].BarrelsBought)])
                        #choose gun
                        for gun in gunlist:
                            if pygame.mouse.get_pos()[0] > gun.GunXpos + 800 and pygame.mouse.get_pos()[0] < gun.GunXpos + 800 + GUNSIZEX and pygame.mouse.get_pos()[1] > int(gun.GunYpos/1.5)+100 and pygame.mouse.get_pos()[1] < int(gun.GunYpos/1.5)+100 + GUNSIZEY:
                                CHOOSENGUN = gun.GunNum - 1
                        #choose barrel
                        i = 0
                        for guntype in gunlist[CHOOSENGUN].BarrelsBought:
                                if pygame.mouse.get_pos()[0] > 500 and pygame.mouse.get_pos()[0] < 760 and pygame.mouse.get_pos()[1] > (20 + i*(GUNSIZEY+40)) and pygame.mouse.get_pos()[1] < (50 + GUNSIZEY + i*(GUNSIZEY+40)):
                                    gunlist[CHOOSENGUN].barrelswap(guntype)
                                i += 1

                    if pygame.mouse.get_pos()[0] > 10 and pygame.mouse.get_pos()[0] < 162 and pygame.mouse.get_pos()[1] > 50 and pygame.mouse.get_pos()[1] < 70:
                        UpgradeGunOpen = 1
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(FPS)
