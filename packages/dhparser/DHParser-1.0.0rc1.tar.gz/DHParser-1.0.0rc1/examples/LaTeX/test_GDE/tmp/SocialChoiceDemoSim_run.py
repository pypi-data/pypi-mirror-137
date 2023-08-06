"""
SocialChoiceDemoSim_run.py - A small simulation for demonstrating that
'critcal cases' appear only relatively rare when mapping individual
preferences unto collective preferences.

This is the front end for the simulation that conducts the simulations and
prints or plots the simulation results.
"""

from math import sqrt

try:
    import psyco
    psyco.full()
    print("psyco JIT speedup enabled")
except ImportError:
    pass

from matplotlib import pylab

from SocialChoiceDemoSim_main import *


def bestInCycle(utilities, cycles):
    """Returns True, if the element with the highest utility
    is caught in a cycle."""
    if len(cycles) == 0: return False
    mx = max(utilities)
    bestList = [i for i, u in enumerate(utilities) if u == mx]
    for best in bestList:
        for cyc in cycles:
            if best in cyc: 
                return True
    return False            

    
def simEffectAlternatives(plot, individuals, alternatives, 
                          repetitions = 100, cultureRatio = 0.0):
    repetitions = 1000
    individuals = 5
    alternatives = range(3, 25, 1)
    cyclesDict = {}.fromkeys(alternatives, 0)
    
    for i in range(repetitions):
        for alt in alternatives:
            profile = genPartialCultureProfile(individuals, alt, cultureRatio)
            utility, cyc = condorcet(profile)
            if len(cyc) > 0: cyclesDict[alt] += 1
    
    cycles = [cyclesDict[alt] / float(repetitions) for alt in alternatives]
    
    pyplot.plot(alternatives, cycles)
    pyplot.xlabel("number of alternatives")
    pyplot.ylabel("ratio of cyclic preferences")
    pyplot.show()


def simEffectIndividuals(plot, individuals, alternatives, 
                         repetitions = 100, cultureRatio = 0.0):
    labels = []
    for alt in alternatives:
        cyclesDict = {}.fromkeys(individuals, 0)        
        for i in range(repetitions):
            for ind in individuals:
                profile = genPartialCultureProfile(ind, alt, cultureRatio)
                utility, cyc = condorcet(profile)
                if len(cyc) > 0: cyclesDict[ind] += 1
    
        cycles = [cyclesDict[ind] / float(repetitions) for ind in individuals]
    
        labels.append(str(alt)+" alternatives")
        plot.plot(individuals, cycles, label = labels[-1])
        plot.set_xlabel("number of individuals")
        plot.set_ylabel("ratio of cyclic preferences")
    
    plot.legend(labels)


def simulateCondorcet(individuals, alternatives, partialCultures, repetitions):
    individualsDict = {}
    for ind in individuals:
        alternativesDict = {}
        individualsDict[ind] = alternativesDict
        for alt in alternatives:
            culturesDict = {}.fromkeys(partialCultures, 0)
            alternativesDict[alt] = culturesDict
            for culture in partialCultures:
                for i in range(repetitions):
                    profile = genPartialCultureProfile(ind, alt, culture)
                    utility, cyc = condorcet(profile)
                    if len(cyc) > 0: culturesDict[culture] += 1
                culturesDict[culture] /= float(repetitions)
    return individualsDict    
                

def plotIndividuals(data, individuals=[], alternatives=[], partialCultures=[]):
    if individuals == []:
        individuals = data.keys()
    if alternatives == []:
        alternatives = data[individuals[0]].keys()
    if partialCultures == []:
        partialCultures = data[individuals[0]][alternatives[0]].keys()
    
    figure = pylab.figure(figsize=(16.0, 9.0))
    cols = int(len(partialCultures) / sqrt(len(partialCultures)))
    rows = (len(partialCultures) + (cols-1)) / cols
    print rows, cols
    
    for i,culture in enumerate(partialCultures):
        plot = figure.add_subplot(rows, cols, i+1)
        if culture == 0.0:
            plot.set_title("impartial culture")
        else:
            plot.set_title("partial culture c = %1.2f"%culture)
        labels = []
        for alt in alternatives:
            values = [data[ind][alt][culture] for ind in individuals]
            labels.append(str(alt)+" alternatives")
            plot.plot(individuals, values, label = labels[-1])
            
        plot.set_xlabel("number of individuals")
        plot.set_ylabel("ratio of cyclic preferences")            
        plot.legend(labels)            
    
if __name__ == "__main__":
#    figure = pylab.figure(figsize=(16.0, 9.0))
#    plot = figure.add_subplot(111)
#    simEffectIndividuals(plot, [3,4,5]+range(10,105,5)+range(125,1025,25), [3,5,9], 
#                         repetitions=1000, cultureRatio = 0.0)
    data = simulateCondorcet([3,4,5]+range(10,105,5)+range(125,1025,25), 
                             [3,6,9], [0.0, 0.1], 5)
    plotIndividuals(data)
    pylab.show()

