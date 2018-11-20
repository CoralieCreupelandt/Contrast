#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Measure your JND in orientation using a staircase method
"""

####################################################
## Ceci est un pseudo code bien degueu ecrit vite fait !
####################################################

from __future__ import absolute_import, division, print_function

from psychopy import core, visual, gui, data, event
from psychopy.tools.filetools import fromFile, toFile
import time, numpy, sys, random
import pandas as pd

GUI = gui.Dlg(title="Steady_Pedestal")
GUI.addField('Numero Ss:')
GUI.addField('Age:')
GUI.show()
if GUI.OK:
    metadata = GUI.data
else:
    sys.exit("user cancelled")

## PARAMETRES
####################################################
numSs = metadata[0]
nomExp = "data_expCS"
output = nomExp + "_Ps" + str(numSs) + "_" + time.strftime("%Y-%m-%d_%Hh%M") + ".csv"

## ECRITURE FICHIER D'OUTPUT
####################################################
fileName = numSs+ dateStr
dataFile = open(fileName + '.csv', 'w')
dataFile.write('baseValue	actualValue exactitude  seuil\n')
d = pd.read_csv(fileName+".csv", sep=';')

## VALUES
####################################################
d["initValue"]=0
d["actualValue"]=0
d["exactitude"]=0
d["seuil"]=0

## CARRES ET AUTRES OBJETS UTILES
####################################################
#creation des 20 carres (4 positions pour chacune des 5 initValue)

w = visual.Window([800,600],color="black",units='pix')

#nom des carres contient les luminesence en int round inferieur
carre15TopLeft=blablabla
carre15TopRight=blablabla
carre15BotLeft=blablabla
carre15BotRight=blablabla

carre18TopLeft=blablabla
carre18TopRight=blablabla
carre18BotLeft=blablabla
carre18BotRightt=blablabla

tableauDeCarres15 = [None, carre15BopLeft, carre15BopRight, None, carre15TotLeft, carre15TotRight]
tableauDeCarres18= [None, carre18BopLeft, carre18BopRight, None, carre18TotLeft, carre18TotRight]
tableauDeCarres23= [None, carre23BopLeft, carre23BopRight, None, carre23TotLeft, carre23TotRight]
tableauDeCarres29= [None, carre29BopLeft, carre29BopRight, None, carre29TotLeft, carre29TotRight]
tableauDeCarres37= [None, carre37BopLeft, carre37BopRight, None, carre37TotLeft, carre37TotRight]
#disposition to match 1 2 4 5 keys disposition

tableauDeBasicValues = [15.0, 18.9, 23.8, 29.9, 37.7]
tableauDeSteps = [1.585, 1.259, 1.122, 1.06, 1.0288, 1.0145, 1.007]
globalClock = core.Clock() #measurement of the total experiment

## EXPE
####################################################

# check for a keypress
event.waitKeys()

while (len(tableauDeBasicValues) >0):
    launchExpe(tableauDeBasicValues)




def launchExpe(tab):

    #preparation des carres necessaires
    randomFirstIndex = math.random(0,tab.length)
    basicValue = tab[randomFirstIndex]
    del tab[randomIndex]
    if(basicValue==15):
        carres = tableauDeCarres15
    elif(basicValue==18):
        carres = tableauDeCarres18
    elif(basicValue==23):
        carres = tableauDeCarres23
    elif (basicValue == 29):
        carres = tableauDeCarres29
    elif (basicValue == 37):
        carres = tableauDeCarres37

    i = 0
    #if one of the counters reach 4, we stop (or actually if the tester reaches the hardest test and succeed we could also stop?)
    tableauDeFails = [0, 0, 0, 0, 0, 0, 0]
    continuer = True
    actualDifficulty = 0

    while(continuer):


        HISI = core.Clock()
        while HISI.getTime() < 1.2:
            carres[0].draw()
            carres[1].draw()
            carres[2].draw()
            carres[3].draw()
            w.flip()


        while HISI.getTime() < 0.033:
            carres[1].draw()
            carres[2].draw()
            carres[4].draw()
            carres[5].draw()
            numbers = [1, 2, 4, 5]
            index = random.randint(0, 3)
            squareIndex = numbers[index]
            carres[squareIndex].setLuminosity(tableauDeSteps[actualDifficulty])  # suppose setLuminosity will multiply its luminosity by the argument
            w.flip()

        HISI = core.Clock()
        resp = event.waitKeys(keyList=['1', '2', '4', '5'])[0]
        rt = H.getTime() * 1000

        if(resp==squareIndex):

            d.initValue[i] = basicValue
            d.actualValue[i] = basicValue * tableauDeSteps[actualDifficulty]
            d.exactitude[i] = 1
            actualDifficulty = actualDifficulty + 1  # good resp

            if(actualDifficulty==7): #already reached the top
                continuer = False
                d.seuil[i]=6
                return #6
        else:
            # bad resp
            tableauDeFails[actualDifficulty]= tableauDeFails[actualDifficulty]+1
            d.initValue[i] = basicValue
            d.actualValue[i] = basicValue * tableauDeSteps[actualDifficulty]
            d.exactitude[i] = 1
            actualDifficulty=actualDifficulty-1 #diminue la difficulte

            for x in tableauDeFails:
                if x>=4:
                    continuer=False #seuil trouve
                    d.seuil[i]=actualDifficulty #difficulte précédente celle faisant 4 fails
                    return #actualDifficulty

        i=i+1






