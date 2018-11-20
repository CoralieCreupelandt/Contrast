#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Measure your JND in contrast using a staircase method
"""

from __future__ import absolute_import, division, print_function

from psychopy import core, visual, gui, data, event
from psychopy.tools.filetools import fromFile, toFile
import time, numpy

try:  # try to get a previous parameters file
    expInfo = fromFile('lastParams.pickle')
except:  # if not there then use a default set
    expInfo = {'observer':'', 'refContrast':0} #Peut-être qu'on pourrait inserer ici de base la condition plutôt? Ou bien le niveau de contraste de base de qq chose? #Plutôt condition de base et créer boucle aléatoire avec les 4 niveaux différents pour commencer l'XP
dateStr = time.strftime("%b_%d_%H%M", time.localtime())  # add the current time

# present a dialogue to change params
dlg = gui.DlgFromDict(expInfo, title='JND Contrast Exp', fixed=['date'])
if dlg.OK:
    toFile('lastParams.pickle', expInfo)  # save params to file for next time
else:
    core.quit()  # the user hit cancel so exit

# make a text file to save data
fileName = expInfo['observer'] + dateStr
dataFile = open(fileName + '.txt', 'w')  ########## Ou mettre .csv?
dataFile.write('targetSide, oriIncrement, correct\n') ### A adapter   TargetSide devrait être TargetId, ConIncrement, correct\n'

# create the staircase handler
staircase = data.StairHandler(startVal=0.2, #Value ou stepsize? #D'après info sur internet, correspond à l'increment donc OK
    stepType='log',
    stepSizes=0.5, 
    minVal=0.03125, maxVal=0.2, #Dois-je mettre ça en step-size ou valeurs de contraste exactes?
    nUp=1, nDown=1,  # will home in on the 80% threshold
    nTrials=None) #Pas de nombre minimum de trials pour nous si!?

# create window and stimuli
globalClock = core.Clock()  # to keep track of time
trialClock = core.Clock()  # to keep track of time
win = visual.Window([800, 600], allowGUI=False, monitor='testMonitor', units='pix', color='grey') #1600 x 1200 at 60 Hz #Rajouter le contraste approprié
win.contrast = 0.0


foil = visual.GratingStim(win, sf=1, size=4, mask='gauss', ori=expInfo['refContrast'])
target = visual.GratingStim(win, sf=1,  size=4, mask='gauss', ori=expInfo['refContrast'])


fixation = visual.GratingStim(win, color='black', tex=None, mask='circle', size=0.2)


instruction = visual.TextStim(win, pos=[0,0], text='Instructions à venir')
instructionSuite = visual.TextStim(win, pos=[0, 0], text="Suite des instructions.") #% expInfo['refContrast'])



######### Peut-être à faire? Créer 4 carrés, créer une liste de ces formes et dire de chercher de façon aléatoire dans cette liste un des carrés et l'illuminer du coup. Non??
#squares = list(Square1, Square2, Square3, Square4)
#foil = squares
#target = un carré aléatoire parmi squares. Et si on fait apparaître target au-dessu de foil normalement il recouvrira l'autre. Mais problème pour luminance!!! Donc on peut en mettre que 1! #Donc faire une liste ou objet avec les 4 carrés. Définir d'abord aléatoirement la cible parmi ses carrés et dire que les "foils" se sont les 3 autres


#Taille des stimuli à changer selon conversions en pixels etc.
Square1 = visual.Rect(win=win, name='Square',
    width=(100, 100)[0], height=(100, 100)[1],
    ori=0, pos=(-200, +200),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1, depth=0.0, interpolate=True)
Square2 = visual.Rect(
    win=win, name='Square2',
    width=(100, 100)[0], height=(100, 100)[1],
    ori=0, pos=(200, 200),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1, depth=-1.0, interpolate=True)
Square3 = visual.Rect(
    win=win, name='Square3',
    width=(100, 100)[0], height=(100, 100)[1],
    ori=0, pos=(-200,-200),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb', 
    opacity=1, depth=-2.0, interpolate=True)
Square4 = visual.Rect(
    win=win, name='Square4',
    width=(100, 100)[0], height=(100, 100)[1],
    ori=0, pos=(200,-200),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1, depth=-3.0, interpolate=True)

# display instructions and wait
instruction.draw()
instructionSuite.draw()
fixation.draw()
win.flip()
# check for a keypress
event.waitKeys()

for thisIncrement in staircase:  # will step through the staircase
    # set location of stimuli
    targetSide = round(numpy.random.random()) * 2 - 1  # +1 = right, -1 = left     ###########Ou bien utiliser les fonctions de type random.choice([,]) --> Ont employé: targetSide= random.choice([-1,1])
    foil.setPos([-5 * targetSide, 0])
    target.setPos([5 * targetSide, 0])  # in other location

    # set orientation of probe
    foil.setContrast(expInfo['refContrast'] + thisIncrement) #Ici changer foil.setContrast(...)

    # draw all stimuli
    HStim = core.Clock()
    while HStim.getTime() < 0.5:
        foil.draw()
        target.draw()
        fixation.draw()
        win.flip()

    #core.wait(0.5)  # wait 500ms (use a loop of x frames for more accurate timing) #J'ai changé en boucle while mais il faut aussi changer en frames surtout!

    # blank screen
    fixation.draw()
    win.flip()

    # get response
    thisResp = None
    while thisResp is None:
        allKeys = event.waitKeys()
        for thisKey in allKeys:
            if ((thisKey == 'left' and targetSide == -1) or
                (thisKey == 'right' and targetSide == 1)):
                thisResp = 1  # correct
            elif ((thisKey == 'right' and targetSide == -1) or
                (thisKey == 'left' and targetSide == 1)):
                thisResp = 0  # incorrect
            elif thisKey in ['q', 'escape']:
                core.quit()  # abort experiment
        event.clearEvents('mouse')  # only really needed for pygame windows

    # add the data to the staircase so it can calculate the next level
    staircase.addResponse(thisResp)
    dataFile.write('%i	%.3f	%i\n' % (targetSide, thisIncrement, thisResp))

# staircase has ended
dataFile.close()
staircase.saveAsPickle(fileName)  # special python data file to save all the info

# give some output to user
print('reversals:')
print(staircase.reversalIntensities)
print('mean of final 6 reversals = %.3f' % numpy.average(staircase.reversalIntensities[-6:]))

win.close()
core.quit()

# The contents of this file are in the public domain.
