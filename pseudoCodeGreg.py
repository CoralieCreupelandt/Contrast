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
from random import randint
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



## Help Functions
####################################################
def createSquare(position, win, luminosity=1):
    square = visual.Rect(win=win, name='Square',
                width=(100, 100)[0], height=(100, 100)[1],
                ori=0, pos=(-200, +200),
                lineWidth=1, lineColor=[1, 1, 1], lineColorSpace='rgb',
                fillColor=[1, 1, 1], fillColorSpace='rgb',
                opacity=1, depth=0.0, interpolate=True)
    square.contrast = luminosity
    return square

####################################################

def launchExpe(tab):

    #preparation des carres necessaires
    randomFirstIndex = randint(0,tab.length)
    basicValue = tab[randomFirstIndex]
    del tab[randomFirstIndex]
    if(basicValue==15):
        carres = tableauDeCarres15
    elif(basicValue==18.9):
        carres = tableauDeCarres18

    # elif(basicValue==23):
    #     carres = tableauDeCarres23
    # elif (basicValue == 29):
    #     carres = tableauDeCarres29
    # elif (basicValue == 37):
    #     carres = tableauDeCarres37

    i = 0
    #if one of the counters reach 4, we stop (or actually if the tester reaches the hardest test and succeed we could also stop?)
    tableauDeFails = [0, 0, 0, 0, 0, 0, 0]
    actualDifficulty = 0
    basicContrast = carres[0].contrast

    while(True):


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
            carres[squareIndex].contrast =  ContrastTest[actualDifficulty] #setLuminosity(tableauDeSteps[actualDifficulty])
            # suppose setLuminosity will multiply its luminosity by the argument
            w.flip()

        carres[squareIndex].contrast=basicContrast
        carres[1].draw()
        carres[2].draw()
        carres[4].draw()
        carres[5].draw()
        w.flip()

        H = core.Clock()
        resp = event.waitKeys(keyList=['1', '2', '4', '5'])[0]
        rt = H.getTime() * 1000

        if(resp==squareIndex):

            if(actualDifficulty==6): #already reached the top
                dataFile.write(str(basicValue) + "     " + str(ContrastTest[actualDifficulty]) + "     " + "1" + "       " + str(ContrastTest[6]) + "\n")
                return #6
            else:
                dataFile.write(str(basicValue) + "     " + str(ContrastTest[actualDifficulty]) + "     " + "1" + "       " + "-" + "\n")
                actualDifficulty = actualDifficulty + 1  # good resp

        else:
            tableauDeFails[actualDifficulty] = tableauDeFails[actualDifficulty] + 1  #new fail#
            for x in tableauDeFails:
                if x>=4:
                    dataFile.write(str(basicValue) + "     " + str(ContrastTest[actualDifficulty]) + "     " + "0" + "       " + str(ContrastTest[actualDifficulty-1]) + "\n")
                    return #actualDifficulty

            dataFile.write(str(basicValue) + "     " + str(ContrastTest[actualDifficulty]) + "     " + "0" + "       " + "-" + "\n")
            actualDifficulty=actualDifficulty-1 #diminue la difficulte

            if (actualDifficulty==-1):
                cross = visual.TextStim(w, text="YOU ARE TOO BAD", color="white", height=30, font="Courier")
                cross.draw()
                w.flip()
                actualDifficulty=0
        i=i+1


## PARAMETRES
####################################################
numSs = metadata[0]
nomExp = "Pokorny-Steady"
output = nomExp + "_Ps" + str(numSs) + "_" + time.strftime("%Y-%m-%d_%Hh%M") + ".csv"

## ECRITURE FICHIER D'OUTPUT
####################################################
fileName = output
dataFile = open(fileName + '.csv', 'w')
dataFile.write('baseValue       contrastValue     exactitude      seuil\n')

## CARRES ET AUTRES OBJETS UTILES
####################################################

w = visual.Window([800,600],color="grey",units='pix')

#nom des carres contient les luminesence en int round inferieur
carre15TopLeft=createSquare((-200,200),w,0.9)
carre15TopRight=createSquare((200,200),w,0.9)
carre15BotLeft=createSquare((-200,-200),w,0.9)
carre15BotRight=createSquare((200,-200),w,0.9)

carre18TopLeft=createSquare((-200,200),w, 0.5)
carre18TopRight=createSquare((200,200),w,0.5)
carre18BotLeft=createSquare((-200,-200),w,0.5)
carre18BotRight=createSquare((200,-200),w,0.5)



tableauDeCarres15 = [None, carre15BotLeft, carre15BotRight, None, carre15TopLeft, carre15TopRight]
tableauDeCarres18= [None, carre18BotLeft, carre18BotRight, None, carre18TopLeft, carre18TopRight]



# tableauDeCarres23= [None, carre23BotLeft, carre23BotRight, None, carre23TopLeft, carre23TopRight]
# tableauDeCarres29= [None, carre29BotLeft, carre29BotRight, None, carre29TopLeft, carre29TopRight]
# tableauDeCarres37= [None, carre37BotLeft, carre37BotRight, None, carre37TopLeft, carre37TopRight]

#disposition to match 1 2 4 5 keys disposition

tableauDeBasicValues = [15, 18.9] #[15.0, 18.9, 23.8, 29.9, 37.7]
tableauDeSteps = [1.585, 1.259, 1.122, 1.06, 1.0288, 1.0145, 1.007]
contrastTestInversed = [0.415, 0.741, 0.878, 0.94, 0.9712, 0.9855, 0.993]
ContrastTest = [0.585, 0.259, 0.122, 0.06, 0.0288, 0.0145, 0.007]
globalClock = core.Clock() #measurement of the total experiment

## EXPE
####################################################

# check for a keypress
event.waitKeys()

while (len(tableauDeBasicValues) >0):
    launchExpe(tableauDeBasicValues)











