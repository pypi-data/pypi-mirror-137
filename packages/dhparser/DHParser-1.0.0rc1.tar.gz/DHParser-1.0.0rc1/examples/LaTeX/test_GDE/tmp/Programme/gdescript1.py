#!/usr/bin/python
# -*- coding: utf-8 -*-

from decision_tools import *

path = "./"

raw  = [("lernen",          [("schwere Klausur", ("bestehen",)),
                             ("leichte Klausur", ("bestehen",))]),
        ("faulenzen",       [("schwere Klausur", ("durchfallen",)),
                             ("leichte Klausur", ("bestehen",))])]

raw2 = [("geh zur Küste", [("Regen", [("nach Hause", "gelangweilt"),
                                      ("Angeln gehen", [("Fische beißen", "erfreut"),
                                                        ("keine Fische", "frustriert")])]),
                           ("Sonnenschein",  [("sich sonnen", "erfreut")])] ),
        ("bleib daheim", "gelangweilt")]

raw3 = [("klagen", [("erhöhtes Angebot", [("prozessieren", [("Gewinn", (20000, "€")),
                                                            ("Verlust", (0, "€"))]),
                                          ("einigen", (10000, "€"))]),
                    ("altes Angebot",    [("prozessieren", [("Gewinn", (20000, "€")),
                                                            ("Verlust", (0, "€"))]),
                                          ("einigen", (5000, "€"))])]),
        ("nicht klagen", (5000, "€"))]

tut1 = [("Expertise",       [("positiv", [("bauen", (8750000, "€"))]),
                             ("negativ", [("nicht bauen", (-250000,"€"))])]),
        ("keine Expertise", [Tree.DECISION_NODE,
                             ("bauen", [("Öl gefunden", (9000000, "€")),
                                        ("kein Öl", (-1000000, "€"))]),
                             ("nicht bauen", (0, "€"))])]

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

tree = createTree(raw)
drawTree(tree, path+"Beispiel1_1.ps", gfx)
table = tableFromTree(tree)
texTable(table, path+"Beispiel1_1.tex", replaceStates="S")

tree = createTree(raw2)
drawTree(tree, path+"Beispiel1_2.ps", gfx)
table = tableFromTree(tree)
texTable(table, path+"Beispiel1_3.tex")
tree = treeFromTable(table)
drawTree(tree, path+"Beispiel1_4.ps", gfx)

tree = createTree(raw3)
drawTree(tree, path+"Loesung1_1.ps", gfx=gfx)
table = tableFromTree(tree)
texTable(table, path+"Loesung1_1.tex", replaceStates="S")

tree = createTree(tut1)
drawTree(tree, path+"Tutorium1_1.ps", gfx)
table = tableFromTree(tree)
texTable(table, path+"Tutorium1_1.tex", replaceStates="S")

gfx.waitUntilClosed()

