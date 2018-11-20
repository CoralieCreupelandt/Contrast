#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Measure your JND in orientation using a staircase method
"""

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

## LISTE EXTERNES
####################################################
# Items expérimentaux
d = pd.read_csv('Steady_Pedestal.csv', sep=';')
d["rts"]=0
d["touche"]=""
d["exactitude"]=0
# ajout metadata
d["numSs"] = int(metadata[0])
d["age"] = int(metadata[1])
d["lat"] = str(metadata[2])

# Items d'entrainement
e = pd.read_csv('liste_practice.csv', sep = ';')

# make a text file to save data
fileName = expInfo['observer'] + dateStr
dataFile = open(fileName + '.txt', 'w')
dataFile.write('targetSide	oriIncrement	correct\n')

# create window and stimuli
globalClock = core.Clock()  # to keep track of time
trialClock = core.Clock()  # to keep track of time
win = visual.Window([800, 600], allowGUI=False, monitor='testMonitor', units='deg')
foil = visual.GratingStim(win, sf=1, size=4, mask='gauss', ori=expInfo['refOrientation'])
target = visual.GratingStim(win, sf=1,  size=4, mask='gauss', ori=expInfo['refOrientation'])
fixation = visual.GratingStim(win, color='black', tex=None, mask='circle', size=0.2)
message1 = visual.TextStim(win, pos=[0, + 3],
    text='Hit a key when ready.')
message2 = visual.TextStim(win, pos=[0, -3],
    text="Then press left or right to identify the %.1fdegree probe." % expInfo['refOrientation'])

# create the staircase handler
staircase = data.StairHandler(startVal=20.0,
    stepType='lin',
    stepSizes=[8, 4, 4, 2, 2, 1, 1],  # reduce step size every two reversals
    minVal=0, maxVal=90,
    nUp=1, nDown=3,  # will home in on the 80% threshold
    nTrials=50)

# display instructions and wait
message1.draw()
message2.draw()
fixation.draw()
win.flip()
# check for a keypress
event.waitKeys()

for thisIncrement in staircase:  # will step through the staircase
    # set location of stimuli
    targetSide = round(numpy.random.random()) * 2 - 1  # +1 = right, -1 = left
    foil.setPos([-5 * targetSide, 0])
    target.setPos([5 * targetSide, 0])  # in other location

    # set orientation of probe
    foil.setOri(expInfo['refOrientation'] + thisIncrement)

    # draw all stimuli
    foil.draw()
    target.draw()
    fixation.draw()
    win.flip()

    core.wait(0.5)  # wait 500ms (use a loop of x frames for more accurate timing)

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
