from scipy.stats import entropy
import numpy as np
from operator import itemgetter
from matplotlib import pyplot as plt
import json

def entropyPopulation(fitnessValues):
    genoSize=len(fitnessValues)
    values=np.array(fitnessValues)
    value,counts = np.unique(values, return_counts=True)
    return entropy(counts/genoSize)

def updateStatistics(stats,population):
    #stats['bestIndiv']=([1,6,3,2,9],0.9)
    #stats['best']=[0.1,0.5,0.5,0.9]
    #stats['average']=[0.1,0.5,0.4,0.7]
    #stats['diversity']=[1.4,1.2,0.5,0]
    population=population.copy()
    population.sort(key=itemgetter(1),reverse=True)
    fitValues=[fit for indiv,fit in population]

    if stats.get('bestIndiv',None)==None or fitValues[0]>stats['bestIndiv'][1]:
        stats['bestIndiv']=population[0]
        stats['best']=stats.get('best',[])+[fitValues[0]]
    else:
        stats['best']=stats['best']+[stats['best'][-1]]
    
    stats['average']=stats.get('average',[])+[sum(fitValues)/len(fitValues)]
    stats['diversity']=stats.get('diversity',[])+[entropyPopulation(fitValues)]

    return stats

def writeStatisticsToFile(stats,targetFile):
    json_object = json.dumps(stats, indent = 4)
    with open(targetFile, "w") as outfile:
        outfile.write(json_object)

def readStatisticsToFile(targetFile):
    stats={}
    with open(targetFile, 'r') as openfile:
        stats = json.load(openfile)
    return stats

def plotStatistics(stats):
    gens=list(range(len(stats['average'])))
    plt.plot(gens,stats['average'],label='Average')
    plt.plot(gens,stats['best'],label='Best')
    plt.plot(gens,np.array(stats['diversity'])/6,label='Diversity/6')
    plt.legend()
    plt.show()