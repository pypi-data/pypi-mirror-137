#!/usr/bin/python
# -*- coding: utf-8 -*-



from decision_tools import *

path = "/home/ecki/tmp/GDE/"
raw = []

raw.append([("Alternative 1 (A1)", ("r1")),
            ("Alternative 2 (A2)", ("r2"))])

raw.append([Tree.CHANCE_NODE, ("Zustand/Ereignis 1 (S1)", ("r1")),
                              ("Zustand/Ereignis 2 (S2)", ("r2"))])

raw.append([("X1", ("Baum 1")),
            ("X2", ("Baum 2"))])

raw.append([Tree.CHANCE_NODE, ("Y1", ("Baum 1")),
                              ("Y2", ("Baum 2"))])

raw.append([("Alternative 1", (" ")),
            ("Alternative 2", (" ")),
            ("Alternative 3", (" "))])

raw.append([("Alternative 1", (" ")),
            ("Alternative 2 oder 3", [Tree.DECISION_NODE, 
                                      ("Alternative 2", (" ")),
                                      ("Alternative 3", (" "))])])


#raw3 = [Tree.CHANCE_NODE, ("Zustand/Ereignis 1 (S1)", ("Resultat 1 (R1)")),
#                          ("Zustand/Ereignis 2 (S2)", ("Resultat 2 (R2)"))]

def drawTree(tree, fname="", gfx = None):
    if gfx:
        gfx.clear()
        plotTree(tree, gfx)
    if fname:
        psDrv = psGfx.Driver()
        tree.setGfx(psDrv)
        w, h = tree.fullSize()
        psDrv.setSize(w, h, False)
        plotTree(tree, psDrv)
        psDrv.save(fname)        


gfx = Compatibility.GetDriver().Window((1024, 600), "gdescript.py - Grafiken für GDE 1")

for i,r in enumerate(raw):
    tree = createTree(r)
    drawTree(tree, path+"Beispiel1b_%i.ps"%(i+1), gfx)


gfx.waitUntilClosed()

