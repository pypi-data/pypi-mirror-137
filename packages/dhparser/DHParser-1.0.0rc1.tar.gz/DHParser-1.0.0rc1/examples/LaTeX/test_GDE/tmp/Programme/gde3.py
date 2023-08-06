#!/usr/bin/python
# -*- coding: utf-8 -*-

from decision_tools import *

path = "/home/ecki/tmp/GDE/"
gfx = Compatibility.GetDriver().Window((1024, 600), "gdescript.py - Grafiken für GDE 1")

rawTree = [('Sozialismus', [(0.05, "Partei-Bonzen", 80),
                            (0.95, "Arbeiter", 30)]),
           ('Sozialstaat', [(0.05, "Unternehmer",     70),
                            (0.80, "Angestellte", 45),
                            (0.15, "Arbeitslose", 20)]),
           ('Freiwirtschaft', [(0.05, "Unternehmer", 100),
                               (0.60, "Angestellte", 50),
                               (0.30, "Arbeiter", 20),
                               (0.05, "Arbeitslose", 5)])]

myTable = array([["",                 "Oberschicht", "Mittelschicht", "Unterschicht"],
                 ["Sozialstaat"  ,  "70",          "45",            "20"],
                 ["Freiwirtschaft", "100",         "35",            "10"]], dtype=object)

altTable = array([["",                 "beste Position", "$\\cdots$", "schlechteste Position"],
                 ["Egalitär",          "20",             "$\\cdots$", "20"],
                 ['$\\hdots$',            "", "", ""],
                 ["Ausgewogen 1",      "85",             "$\\cdots$", "35"],
                 ['$\\hdots$',            "", "", ""],                 
                 ["Ausgewogen 2",      "35",             "$\\cdots$", "15"],     
                 ['$\\hdots$',            "", "", ""],                            
                 ["Ungleich",          "100",            "$\\cdots$", "0"]], dtype=object)

tree = createTree(rawTree)
drawTree(tree, path+"Beispiel3_1.ps", gfx)
table = tableFromTree(tree)
texTable(table, path+"Beispiel3_1.tex", replaceStrategies="A", replaceStates="S")
texTable(myTable, path+"Beispiel3_2.tex", replaceStrategies="")
texTable(altTable, path+"Beispiel3_3.tex", replaceStrategies="")

gfx.waitUntilClosed()

