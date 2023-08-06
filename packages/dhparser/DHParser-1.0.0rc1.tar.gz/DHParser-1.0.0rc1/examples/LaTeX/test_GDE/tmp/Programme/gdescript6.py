#!/usr/bin/python
# -*- coding: utf-8 -*-

from decision_tools import *

path = "/home/ecki/tmp/GDE/"

tut1 = [("Expertise",       [(0.4, "positiv", [("bauen", (8750000, "€"))]),
                             (0.6, "negativ", [("nicht bauen", (-250000,"€"))])]),
        ("keine Expertise", [Tree.DECISION_NODE,
                             ("bauen", [(0.4, "Öl gefunden", (9000000, "€")),
                                        (0.6, "kein Öl", (-1000000, "€"))]),
                             ("nicht bauen", (0, "€"))])]

tut2 = [("Expertise",       [(0.4, "positiv", (8750000, "€")),
                             (0.6, "negativ", (-250000,"€"))]),
        ("keine Expertise", [Tree.DECISION_NODE,
                             ("bauen", (3000000, "€")),
                             ("nicht bauen", (0, "€"))])]

tut3 = [("Expertise",       (3350000, "€")),
        ("keine Expertise", (3000000, "€"))]

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

tree = createTree(tut1)
drawTree(tree, path+"Beispiel6_3A.ps", gfx)
table = tableFromTree(tree)
texTable(table, path+"Beispiel6_3A.tex", replaceStates="S")

tree = createTree(tut2)
drawTree(tree, path+"Beispiel6_3B.ps", gfx)
table = tableFromTree(tree)
texTable(table, path+"Beispiel6_3B.tex", replaceStates="S")

tree = createTree(tut3)
drawTree(tree, path+"Beispiel6_3C.ps", gfx)
table = tableFromTree(tree)
texTable(table, path+"Beispiel6_3C.tex", replaceStates="S")

gfx.waitUntilClosed()

