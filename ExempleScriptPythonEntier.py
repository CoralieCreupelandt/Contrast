
## INITIALISATION
####################################################
import pandas as pd
import time, random, sys
from psychopy import visual, core, event, gui

## METADATA
####################################################
GUI = gui.Dlg(title="tache_CS")
GUI.addField('Numero Ss:')
GUI.addField('Age:')
GUI.addField('Lateralite:', choices=["droite","gauche"])
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
d = pd.read_csv('liste.csv', sep=';')
d["rts"]=0
d["touche"]=""
d["exactitude"]=0
# ajout metadata
d["numSs"] = int(metadata[0])
d["age"] = int(metadata[1])
d["lat"] = str(metadata[2])

# Items d'entrainement
e = pd.read_csv('liste_practice.csv', sep = ';')

## RANDOMISATION
####################################################
d = d.ix[random.sample(list(d.index), len(d))]
d.index = range(len(d))

## OUVERTURE DE LA FENETRE
####################################################
w = visual.Window([800,600],color="black",units='pix')

## OBJETS PSYCHOPY
####################################################

cross = visual.TextStim(w, text="+", color="white", height=30, font="Courier")
isi = visual.Rect(w, size=[800,600], fillColor="black",lineColor="black")
consigne = visual.ImageStim(w, image = 'consigne.png', size=[750,563])
fin = visual.ImageStim(w, image = 'end.png')
pause = visual.ImageStim(w, image = 'pause.png')
fb = visual.TextStim(w, text="X", color="red", height=80, font="Arial")
go = visual.ImageStim(w, image = 'go.png')

## CONSIGNE
####################################################
consigne.draw()
w.flip()
event.waitKeys(keyList=["space"])

## ENTRAINEMENT
####################################################
for j in range(e.shape[0]):

    # isi
    HISI = core.Clock()
    while HISI.getTime() < 0.5:
        isi.draw()
        w.flip()
    
    # croix de fixation
    HCROSS = core.Clock()
    while HCROSS.getTime() < 0.5:
        cross.draw()
        w.flip()
    
    # stimulus
    stim = visual.TextStim(w, text=e.Items[j], color="white",height=30)
    stim.draw()
    w.flip()
    
    # attente de la réponse
    resp = event.waitKeys(keyList=['c','n'])[0]
    
    if (resp == "c" and e.Condition[j] == "animal") or (resp == "n" and e.Condition[j] == "objet"):
        continue
    else:
        HFB = core.Clock()
        while HFB.getTime() < 0.5:
            fb.draw()
            w.flip()
    
## GO
####################################################
go.draw()
w.flip()
event.waitKeys(keyList=["space"])

## BOUCLE ESSAI
####################################################
for i in range(d.shape[0]):

    # isi
    HISI = core.Clock()
    while HISI.getTime() < 0.5:
        isi.draw()
        w.flip()

    # croix de fixation
    HCROSS = core.Clock()
    while HCROSS.getTime() < 0.5:
        cross.draw()
        w.flip()

    # stimulus
    stim = visual.TextStim(w, text=d.Items[i], color="white",height=30)
    stim.draw()
    w.flip()

    # lancement du chrono + attente de reponse
    H = core.Clock()
    resp = event.waitKeys(keyList=['c','n'])[0]
    rt = H.getTime()*1000

    # enregistrement VD
    d.rts[i] = rt
    d.touche[i] = resp
    if (resp == "c" and d.Condition[i] == "animal") or (resp == "n" and d.Condition[i] == "objet"):
        d.exactitude[i]=100
    else:
        d.exactitude[i]=0

    # feedback si erreur        ##############SOUCI ICI QUELQUE PART DANS LE FEEDBACK???
    HFB = core.Clock()
    while HFB.getTime() < 0.5:
        fb.draw()
        w.flip()

    # exportation des données
    d.to_csv(output, index=False, header=True, sep="\t")

    # pause
    if i == 3:
        pause.draw()
        w.flip()
        event.waitKeys(keyList=["space"])

## MESSAGE FIN
####################################################
fin.draw()
w.flip()
event.waitKeys(keyList=["space"])

## FERMETURE
####################################################
w.close()
core.quit()