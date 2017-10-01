import pygame, os
MOBIMGLIST = {}
RootDir = str(__file__).split("\Pathgame.py")[0]
MobDir = RootDir + "\Mobs"
for folder in os.listdir(MobDir):
    try:
        MOBIMGLIST[folder[4]].append([])
    except KeyError:
        MOBIMGLIST[folder[4]] = []
        MOBIMGLIST[folder[4]].append([])
    for img in os.listdir(MobDir + '\\\\' + folder):
        MOBIMGLIST[folder[4]][int(folder[6])].append(img)
print(MOBIMGLIST)

##path to root dir: str(__file__).split("\Pathgame.py")[0]