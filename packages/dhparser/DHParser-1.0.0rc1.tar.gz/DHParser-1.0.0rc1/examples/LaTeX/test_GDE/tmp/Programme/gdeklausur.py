#!/usr/bin/python
# -*- coding: utf-8 -*-

from decision_tools import *

path = "/home/ecki/tmp/GDE/"

#tut  = [("Expertise",       [(0.4, "positiv", [("bauen", (8750000, "€"))]),
#                             (0.6, "negativ", [("nicht bauen", (-250000,"€"))])]),
#        ("keine Expertise", [Tree.DECISION_NODE,
#                             ("bauen", [(0.4, "Öl gefunden", (9000000, "€")),
#                                        (0.6, "kein Öl", (-1000000, "€"))]),
#                             ("nicht bauen", (0, "€"))])]

baum = [("Alternative 1", [(0.2, "Ereignis 1", (1000, "€")),
                           (0.8, "Ereignis 2", [("Handlung A", (400, "€")),
                                                ("Handlung B", ([(0.5, "Ereignis A", (200, "€")),
                                                                 (0.5, "Ereigbnis B", (800, "€"))]))])]),
        ("Alternative 2", [(0.3, "Ereignis alpha", (600, "€")),
                           (0.5, "Ereignis beta", (400, "€")),
                           (0.2, "Ereignis gamma", (1000, "€"))])]

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

tree = createTree(baum)
drawTree(tree, path+"Klausur.ps", gfx)
table = tableFromTree(tree)
texTable(table, path+"Klausur_Table.tex", replaceStates="S")


gfx.waitUntilClosed()

