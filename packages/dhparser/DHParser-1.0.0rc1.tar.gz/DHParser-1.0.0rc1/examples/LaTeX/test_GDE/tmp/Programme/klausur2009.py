#!/usr/bin/python
# -*- coding: utf-8 -*-

from decision_tools import *

path = "./"

raw = [("Expertise", [(0.626, "positiv", [("bauen", [(0.905, "Öl", (39, "Mio €")),
                                                     (0.095, "kein Öl", (-11, "Mio €"))
                                                    ]),
                                          ("nicht bauen", (-1, "Mio €"))
                                          ]),

                      (0.374, "negativ", [("bauen", [(0.081, "Öl", (39, "Mio €")),
                                                     (0.919, "kein Öl", (-11, "Mio €"))
                                                    ]),
                                          ("nicht bauen", (-1, "Mio €")) 
                                         ])
                      ]


       ),
       ("keine Exp.", [Tree.DECISION_NODE,
                       ("bauen", [(0.6, "Öl", (40, "Mio €")),
                                  (0.4, "kein Öl", (-10, "Mio €"))
                                 ]),
                       ("nicht bauen", (0, "€")) 
                      ]
       )
      ]


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


gfx = Compatibility.GetDriver().Window((1024, 600), "Klausur_Loesung2009.py")

tree = createTree(raw)
drawTree(tree, path+"Klausur_2009.ps", gfx)


gfx.waitUntilClosed()

