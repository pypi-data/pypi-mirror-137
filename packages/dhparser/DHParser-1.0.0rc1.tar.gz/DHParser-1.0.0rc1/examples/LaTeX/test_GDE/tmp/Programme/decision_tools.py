# -*- coding: utf-8 -*-

from numpy import array, zeros
from PyPlotter import Gfx, Compatibility, psGfx

###############################################################################
#
# Classes for drawing an evaluating decision trees
#
##############################################################################

class Entity(object):
    """Represents one entity in a decision tree, which can be
    a leaf, a branch or a tree."""
    MAX_EXPECTED_UITILITY_RULE = "expected utility rule"
    MAX_MIN_RULE               = "maxmin rule"
    pen = Gfx.Pen(color = Gfx.BLACK)
    def __init__(self):
        self.width = -1
        self.height = -1
        self.adjustedWidth = -1        
        self.fullWidth = -1
        self.fullHeight = -1
        self.gfx = None
        self.rule = Entity.MAX_EXPECTED_UITILITY_RULE
        self.descendants = []
    def setGfx(self, gfx):
        """Sets the graph driver of this entity and all sub-entities 
        to be used for size calculation and plotting. 'gfx' must be of 
        type PyPlotter.Gfx.Driver."""
        self.gfx = gfx
        # invalidate width and height fields:
        self.width = -1
        self.height = -1
        self.adjustedWidth = -1
        self.fullWidth = -1
        self.fullHeight = -1        
        for entity in self.descendants: entity.setGfx(gfx)
    def setRule(self, rule):
        """Sets the evaluation rule for this entity and all sub-
        entities."""
        assert rule in [Entity.MAX_EXPECTED_UITILITY_RULE, Entity.MAX_MIN_RULE]
        self.rule = rule
        for entity in self.descendants: entity.setRule(rule)
    def size(self):
        """Returns the size (width, height) of this entitiy only,
        subentities excluded. 'width' and 'height' define the required space 
        for plotting the entity with the current graph driver.
        Also sets the entity variables 'width' and 'height' to these
        values, if 'gfx' has changed from the last time when the size
        method was called."""
        raise NotImplementedError
    def _adjustWidth(self):
        """Adjusts the 'width' of all branches in the tree so that branches
        on the same level have the same adjusted width."""
        def traverse(dic, entity, level):
            dic.setdefault(level, []).append(entity)
            for desc in entity.descendants:  traverse(dic, desc, level+1)
        if self.adjustedWidth < 0:
            d = {}; traverse(d, self, 0)
            for k in d.iterkeys():
                maxW = max([e.size()[0] for e in d[k] if isinstance(e, Branch)]+[0])
                for e in d[k]:
                    if isinstance(e, Branch): e.adjustedWidth = maxW
                    else: e.adjustedWidth = e.size()[0]
        assert self.adjustedWidth >= 0
        return self.adjustedWidth       
    def fullSize(self):
        """Returns the entire size (width, height) of the entity and all
        its sub-entities. 
        """
        if self.fullWidth < 0:
            width, height = self.size()            
            width = self._adjustWidth()
            hh, ww = 0, 0
            for entity in self.descendants:
                w, h = entity.fullSize()
                ww = max(w, ww)
                hh += h
            self.fullHeight = max(hh, height)
            self.fullWidth = width + ww
        return (self.fullWidth, self.fullHeight)
    def plot(self, x, y):
        """Plots the entity, at Position (x,y) where (x,y) is the
        position where the last branch of the tree ended.""" 
        raise NotImplementedError
    def evaluate(self):
        """Returns the value of the entity. How the value is determined
        depends on the kind of entity and the rule used"""
        raise NotImplementedError
        

def resultStr(description, value, unit):
    s = description
    if value or value == 0:
        if description: s+= " ("
        if unit in ["$", "€", "£", "¥"]:
            s += unit+" "+str(value)
        else:
            s += str(value)+" "+unit
        if description: s += ")"
    return s    
        
class Leaf(Entity):
    """A leaf represents one possible outcome of the decision tree.
    It is defined by its description, a utility value and, optionally,
    a unit like for example "$" or "€"."""
    pen = Gfx.Pen(color = Gfx.BLACK, fweight = Gfx.BOLD)
    def __init__(self, description, value = "", unit = ""):
        Entity.__init__(self)
        self.description = description
        self.value       = value
        self.unit        = unit
    def __str__(self):
        return resultStr(self.description, self.value, self.unit)
    def _class_invariants(self):
        assert not self.descendants     
    def size(self):
        if self.width < 0:
            self.width, self.height = self.gfx.getTextSize(str(self)+ "  ")
        return (self.width, self.height)
    def plot(self, x, y):
        h = self.size()[1]
        self.gfx.applyPen(self.pen)
        blank, dummy = self.gfx.getTextSize(" ")
        self.gfx.writeStr(x+blank, y-h/2, str(self))
    def evaluate(self):
        if self.value: return self.value
        else: return 0

    
class Branch(Entity):
    """A branch represents on option in a decision tree. It is characterized
    by a description, a probability value in case the branch follows a
    state node and an outcome, which can be either a leaf or another subtree.
    """  
    def __init__(self, description, outcome, probability = -1.0):
        Entity.__init__(self)
        self.description = description
        assert isinstance(outcome, Tree) or isinstance(outcome, Leaf)
        self.descendants = [outcome]
        self.probability = probability
        self._pstrtmpl = "p=%1.3f    "
    def __str__(self):
        s = ""
        if self.probability >= 0.0:
            s += self._pstrtmpl % self.probability
        s += self.description
        return s 
    def _class_invariants(self):
        assert len(self.descendants) == 1
        assert isinstance(self.descendants[0], Tree) or \
               isinstance(self.descendants[0], Leaf)         
    def size(self):
        """Returns the size (width, height) of this entitiy only,
        subentities excluded."""
        if self.width < 0:
            self.width, self.height = self.gfx.getTextSize("  "+str(self))
            self.height = self.height*2 + self.height/4
        return (self.width, self.height)
    def plot(self, x, y):
        self.gfx.applyPen(self.pen)
        self.gfx.drawLine(x, y, x+self.adjustedWidth-1, y)
        dx = self.gfx.getTextSize(" ")[0]
        if self.probability >= 0.0:
            self.gfx.setFont(self.gfx.fontType, Gfx.SMALL, Gfx.PLAIN)
            offset, dummy = self.gfx.getTextSize(self._pstrtmpl % 0.0)            
            self.gfx.writeStr(x+dx, y+2, self._pstrtmpl % self.probability)
            self.gfx.applyPen(self.pen)
        else: offset = 0
        self.gfx.writeStr(x+dx+offset, y+1, self.description)
        self.descendants[0].plot(x+self.adjustedWidth-1, y)
    def evaluate(self):
        p = self.probability
        if p < 0.0: p = 1.0
        return p*self.descendants[0].evaluate()    
    
    
class Tree(Entity):
    DECISION_NODE = "decision node"
    CHANCE_NODE   = "chance node"
    def __init__(self, branches, treeType):
        Entity.__init__(self)
        self.treeType = treeType
        self.descendants = branches
        self._class_invariants()
        self._leftWidth = 0
        self._rightWidth = 0
    def _class_invariants(self):
        assert len(self.descendants) >= 1
        for entity in self.descendants:
            assert isinstance(entity, Branch)
    def size(self):
        if self.width < 0:
            w, h = self.gfx.getTextSize("   ")
            self._leftWidth = w
            self._rightWidth = w
            w, h = self.gfx.getTextSize("Fg")
            self.width = self._leftWidth + self._rightWidth
            self.height = h
        return (self.width, self.height)
    def plot(self, x, y):
        self._adjustWidth()
        self.gfx.applyPen(self.pen)
        self.gfx.drawLine(x, y, x+self._leftWidth-1, y)
        hl = [branch.fullSize()[1] for branch in self.descendants]
        hsum = sum(hl)
        y1 = y; y2 = y + hsum // 2
        x1 = x+self._leftWidth-1
        x2 = x1+self._rightWidth
        for i, branch in enumerate(self.descendants):
            y2 -= hl[(i)]//2            
            self.gfx.drawLine(x1, y1, x2, y2)
            branch.plot(x2, y2)             
            y2 -= hl[(i)]//2 
        xx = x + self._leftWidth
        if self.treeType == Tree.DECISION_NODE:
            d = min(self._leftWidth, self._rightWidth)*4//4
            self.gfx.setColor(Gfx.WHITE)
            self.gfx.fillRect(xx-d//2, y-d//2, d, d)
            self.gfx.setColor(self.pen.color)
            self.gfx.drawRect(xx-d//2, y-d//2, d, d)
        else:
            r = min(self._leftWidth*2//3, self._rightWidth*2//4)
            self.gfx.setColor(Gfx.WHITE)
            self.gfx.fillCircle(xx, y, r)
            self.gfx.setColor(self.pen.color)
            self.gfx.drawCircle(xx, y, r)
    def evaluate(self):
        vl = [branch.evaluate for branch in self.descendants]
        if self.treeType == Tree.DECISION_NODE or \
           self.rule == Entity.MAX_EXPECTED_UITILITY_RULE:
            return max(vl)
        else:
            return min(vl)

###############################################################################
#
# Utility functions
#
###############################################################################

def flip(treeType):
    """Retruns Tree.DECISION_NODE if 'treeType' is Tree.CHANCE_NODE and
    vice versa."""
    if treeType == Tree.DECISION_NODE:
        return Tree.CHANCE_NODE
    elif treeType == Tree.CHANCE_NODE:
        return Tree.DECISION_NODE
    else: raise AssertionError, "Unknown tree type: "+str(treeType) 

def createTree(nestedList, treeType = Tree.DECISION_NODE):
    """Returns a decision tree compsoed of 'Tree', 'Branch' and 'Leaf' objects
    that is created from the nested list 'nestedList'."""
    assert nestedList
    if isinstance(nestedList, tuple): # branch
        link = nestedList[-1]
        if isinstance(link, tuple):
            if len(link) == 3:
                outcome = Leaf(link[0], link[1], link[2])
            elif len(link) == 2:
                if isinstance(link[0], str):
                    outcome = Leaf(link[0], link[1], "")
                elif isinstance(link[1], str):
                    outcome = Leaf("", link[0], link[1])
                else: raise AssertionError, "Illegal Leaf specification: " + str(link)
            elif len(link) == 1:
                if isinstance(link[0], str):  
                    outcome = Leaf(link[0], "", "")
                else: 
                    outcome = Leaf("", link[0], "")
            else: raise AssertionError, "Leaf specification too long or too short: "+str(link)
        elif isinstance(link, list):
            outcome = createTree(link, treeType)
        else:
            if isinstance(link, str):
                outcome = Leaf(link, "", "")
            else:
                outcome = Leaf("", link, "")
        if len(nestedList) == 2:
            return Branch(nestedList[0], outcome, -1.0)
        else:
            return Branch(nestedList[1], outcome, nestedList[0])
    elif isinstance(nestedList, list): # tree
        if nestedList[0] in [Tree.DECISION_NODE, Tree.CHANCE_NODE]:
            nl = nestedList[1:]
            tt = nestedList[0]
        else:
            nl = nestedList
            tt = treeType
        branches = [createTree(it, flip(tt)) for it in nl]
        return Tree(branches, tt)
    else:
        raise AssertionError, "Neither tree nor branch: "+str(nestedList)

            
def treeFromTable(table):
    """Returns a decision tree that is corresponding to the decision 'table'.
    'table' must be a numpy.array with data type 'object'. The first row (but
    the first element) contains the 'states'. The first column (but the first 
    element) contains the strategies. Strategies are always strings that 
    contain a description of the strategy. States are either strings or
    tuples (probability, string). The fields staring from the second row
    and the second columns contain the outcomes for the respective strategies
    and states. An outcome can be either a string or a tuple 
    (description, value) or a tuple (description, value, unit).
    """
    strategies = table[1:,0]
    states = table[0,1:]
    boughs = []
    for i,s in enumerate(strategies):
        branches = []
        for k,a in enumerate(states):
            if isinstance(a, tuple):
                if isinstance(a[0], str): description, p = a
                else: p, description = a
            else:
                p = -1.0
                description = a
            entry = table[i+1,k+1]
            if isinstance(entry, str): t = (entry, "", "")
            elif len(entry) == 2: t = (entry[0], entry[1], "")
            else: t = entry
            leaf = Leaf(t[0],t[1],t[2])
            branch = Branch(description, leaf, p) 
            branches.append(branch)
        node = Tree(branches, Tree.CHANCE_NODE)
        bough = Branch(s, node)
        boughs.append(bough)
    tree = Tree(boughs, Tree.DECISION_NODE)
    return tree


english = { "if"   : " if ",
            "then" : " then ",
            "else" : ",  else",
            "and"  : " and " }
german  = { "if"   : " wenn ",
            "then" : " dann ",
            "else" : ",  sonst",
            "and"  : " und " }
TL = german

def tableFromTree(tree):
    """Returns a decision table that corresponds to the decision tree. 
    WARNING: Algorithm is much too complicated and buggy!!!"""
    class XDict(dict):
        pass
    def strategies(tree):
        def genConditionalStrategies(branchList, branches):
            if len(branchList) == 1:
                for s in branches[branchList[0]]: yield {branchList[0]: s}
            elif len(branchList) > 1: 
                for s in branches[branchList[0]]:
                    for cs in genConditionalStrategies(branchList[1:], branches):
                        d = XDict()
                        d.update({branchList[0]: s})                        
                        d.update(cs)
                        d.keyOrder = branchList                        
                        yield d
        if not isinstance(tree, Tree): return []
        strategyList = []
        if tree.treeType == Tree.DECISION_NODE:
            for branch in tree.descendants:
                subTreeStrategies = strategies(branch.descendants[0])
                if subTreeStrategies:
                    for s in subTreeStrategies:
                        strategyList.append([branch]+s)
                else:
                    strategyList.append([branch])
        elif tree.treeType == Tree.CHANCE_NODE:
            branchList = []; branches = {}
            for branch in tree.descendants:
                subTreeStrategies = strategies(branch.descendants[0])
                if subTreeStrategies:
                    branchList.append(branch)
                    branches[branch] = subTreeStrategies
            for s in genConditionalStrategies(branchList, branches):
                strategyList.append([s])
        return strategyList
    def chances(tree):
        def genChanceCombinations(chancesPerBranch):
            if len(chancesPerBranch) == 1: 
                for c in chancesPerBranch[0]: yield c
            elif len(chancesPerBranch) > 1: 
                for c in chancesPerBranch[0]:
                    for sc in genChanceCombinations(chancesPerBranch[1:]):
                        yield c+sc
        if not isinstance(tree, Tree): return []
        chanceList = []
        if tree.treeType == Tree.CHANCE_NODE:
            for branch in tree.descendants: 
                subTreeChances = chances(branch.descendants[0])
                if subTreeChances:
                    for c in subTreeChances:
                        chanceList.append([branch]+c)
                else:
                    chanceList.append([branch])
        elif tree.treeType == Tree.DECISION_NODE:
            chancesPerBranch = []
            for branch in tree.descendants:
                subTreeChances = chances(branch.descendants[0])
                if subTreeChances: 
                    chancesPerBranch.append(subTreeChances)
            for c in genChanceCombinations(chancesPerBranch):
                chanceList.append(c)        
            #for branch in tree.descendants:
            #    if isinstance(branch.descendants[0], Tree):
            #        chanceList.extend(chances(branch.descendants[0]))
        return chanceList
    def strategyToStr(s):
        desc = []
        for item in s:
            if isinstance(item, Branch):
                desc.append(item.description)
            else:
                try:  keys = item.keyOrder
                except AttributeError:  keys = item.keys()
                for k in keys:
                    v = item[k]
                    desc.append(TL["if"]+k.description+TL["then"])
                    desc.append(strategyToStr(v))
                    desc.append(TL["else"])
                desc.pop()
            desc.append("; ")
        desc.pop()
        return "".join(desc)
    def chanceToStr(c):
        p = 1.0; desc = []
        for branch in c:
            if p > 0.0: p *= branch.probability
            desc.append(branch.description)
            desc.append(TL["and"])
        desc.pop()
        return ("".join(desc), p)
    def match(tree, strategy, chance):
        if isinstance(tree, Leaf):
            return (tree.description, tree.value, tree.unit)
        elif isinstance(tree, Branch):
            outcome = match(tree.descendants[0], strategy, chance)
            if tree.probability >= 0.0:
                d,v,u = outcome
                return (d, v*tree.probability, u)
            else: return outcome
        elif tree.treeType == Tree.DECISION_NODE:
            branch = strategy[0]
            #print strategyToStr(strategy)
            return match(branch, strategy[1:], chance)
        else: # tree.treeType == Tree.CHANCE_NODE
            for k in tree.descendants:
                if k in chance:
                    branch = k
                    break
            if len(strategy) > 0:
                return match(branch, strategy[0][branch], chance)
            else:
                return match(branch, [], chance)
    sl = strategies(tree)
    cl = chances(tree)
    table = zeros((len(sl)+1,len(cl)+1), dtype=object)
    for i, c in enumerate(cl):  table[0, i+1] = chanceToStr(c)
    for k, s in enumerate(sl):  table[k+1, 0] = strategyToStr(s)
    for k in xrange(len(sl)):
        for i in xrange(len(cl)):
            table[k+1, i+1] = match(tree, sl[k], cl[i])
    return table
        
            
def plotTree(tree, gfx, screenRegion = None):
    """Plots a decision tree onto region 'scrRegion'."""
    if screenRegion:
        x1, y1, x2, y2 = screenRegion
        w = x2-x1+1
        h = y2-y1+1
    else:
        w, h = gfx.getSize()
        x1, y1, x2, y2 = 0, 0, w-1, h-1
    if tree.gfx != gfx: tree.setGfx(gfx)
    tree.plot(x1, y1+h/2)

def stateStr(state):
    if isinstance(state, tuple):
        if state[1] >= 0:
            return state[0]+" p=(%1.2f)"%state[1]
        else: return state[0]
    else:
        if isinstance(state, str): return state
        else: return ""
    
def texTable(table, fName = "", fixedWidth = 0, replaceStrategies = "A", 
             replaceStates = ""):
    """Writes the table as tex file to file 'fName'. If 'fName' is an empty
    string then the tex-table is returned as string instead of writing a 
    file."""
    tex = ["\\begin{tabular}"]
    bottomLine = []           
    r, c = table.shape
    if replaceStates:
        bottomLine.append("\\begin{itemize}\n")
        for i in xrange(1, c):
            key = replaceStates+str(i)
            st = table[0, i]
            if isinstance(st, tuple):
                table[0, i] = (key, st[1])
                st = st[0]
            else: table[0, i] = key
            bottomLine.append("\item {\\em "+key+"}: "+st+"\n")
        bottomLine.append("\\end{itemize}\n")     
    if replaceStrategies:
        bottomLine.append("\\begin{itemize}\n")
        for i in xrange(1,r):
            key = replaceStrategies+str(i)
            st = table[i, 0]
            table[i, 0] = key
            bottomLine.append("\item {\\em "+key+"}: "+st+"\n")
        bottomLine.append("\\end{itemize}\n")       
    linefeed = "\\\\ \\cline{2-%i}\n" % c
    if fixedWidth:
        w = float(fixedWidth) / (c+1)
        tex.append("{p{%1.2fcm}|"%(2*w)+("p{%1.2fcm}|"%w)*(c-1)+"}\n")
        tex.append("\\multicolumn{1}{p{%1.2fcm}}{%s} & "%\
                   (2*w,stateStr(table[0,0])))
        for state in table[0,1:]:
            tex.append("\\multicolumn{1}{p{%1.2fcm}}{%s} "%(w,stateStr(state)))
            tex.append(" & ")
    else:
        tex.append("{"+"c|"*c+"}\n")
        for state in table[0]:
            tex.append("\\multicolumn{1}{c}{%s} "%stateStr(state))
            tex.append(" & ")
    tex.pop()
    tex.append(linefeed)
    for row in table[1:]:
        tex.append(" %s "%str(row[0]))
        for entry in row[1:]:
            if not isinstance(entry, tuple): entry = (entry, None, "")
            tex.append("& %s "%resultStr(*entry))
        tex.append(linefeed)        
    tex.append("\end{tabular}\n")
    tex.extend(bottomLine)  
    texStr = "".join(tex)
    if fName:
        f = file(fName, "w")
        f.write(texStr)
        f.close()
    return texStr
    
    
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
        
def bayes(br, pp, pn):
    return (br * pp) / (br * pp + (1-br)*pn)         

if __name__ == "__main__":
    raw  = [("go out",    [(0.3, "rain", -5),
                           (0.7, "sunshine", 5)]),
            ("stay home", [(0.6, "TV boring", 0),
                           (0.4, "TV good", 4)])]
    mytable = array([["",       "War",  "Peace"],
                     ["arm"  ,  "dead", "Cold War"],
                     ["disarm", "red",  "detente"]], dtype=object)
    
    raw2 = [("geh zur Küste", [("Regen", [("nach Hause", "gelangweilt"),
                                          ("Angeln gehen", [("Fische beißen", "erfreut"),
                                                            ("keine Fische", "frustriert")])]),
                               ("Sonnenschein",  [("sich sonnen", "erfreut")])] ),
            ("bleib daheim", "gelangweilt")]
    
    mytree = createTree(raw2)
    print texTable(tableFromTree(mytree))
    mytree = treeFromTable(mytable)
    mygfx = Compatibility.GetDriver().Window((800, 600), "decision_tree.py - self test")
    plotTree(mytree, mygfx)
    psDrv = psGfx.Driver()
    plotTree(mytree, psDrv)
    psDrv.save("/home/eckhart/tmp/test.ps")
    mygfx.waitUntilClosed()
    