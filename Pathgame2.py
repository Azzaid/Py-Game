import pygame, sys, random, math, os
MOBIMGLIST = {}
RootDir = str(__file__).split("\Pathgame2.py")[0]
MobDir = RootDir + "\Mobs"
for folder in os.listdir(MobDir):
    try:
        MOBIMGLIST[folder[4]].append([])
    except KeyError:
        MOBIMGLIST[folder[4]] = []
        MOBIMGLIST[folder[4]].append([])
    for img in os.listdir(MobDir + '\\\\' + folder):
        MOBIMGLIST[folder[4]][int(folder[6])].append(pygame.image.load(MobDir + '\\\\' + folder + '\\\\' + img))
        if folder[4] == 1:
            MOBIMGLIST[folder[4]][int(folder[6])][len(MOBIMGLIST[folder[4]][int(folder[6])])-1] = pygame.transform.scale(MOBIMGLIST[folder[4]][int(folder[6])][len(MOBIMGLIST[folder[4]][int(folder[6])])-1], (20, 40))
        elif folder[4] == 2:
            MOBIMGLIST[folder[4]][int(folder[6])][len(MOBIMGLIST[folder[4]][int(folder[6])])-1] = pygame.transform.scale(MOBIMGLIST[folder[4]][int(folder[6])][len(MOBIMGLIST[folder[4]][int(folder[6])])-1], (20, 40))
        else:
            MOBIMGLIST[folder[4]][int(folder[6])][len(MOBIMGLIST[folder[4]][int(folder[6])])-1] = pygame.transform.scale(MOBIMGLIST[folder[4]][int(folder[6])][len(MOBIMGLIST[folder[4]][int(folder[6])])-1], (20, 40))

print(MOBIMGLIST)