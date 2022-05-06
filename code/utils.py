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
    plt.plot(gens,stats['average'],label='Average Fit.')
    plt.plot(gens,stats['best'],label='Best Fit.')
    plt.plot(gens,np.array(stats['diversity'])/6,label='Diversity/6')
    plt.xlabel("Generations")
    plt.legend()
    plt.show()
    
def plotMultipleStatistics(statsArray):
    best=[]
    average=[]
    diversity=[]

    for stat in statsArray:
        best.append(stat['best'])
        average.append(stat['average'])
        diversity.append(stat['diversity'])

    best=np.average(np.array(best),axis=0)
    average=np.average(np.array(average),axis=0)
    diversity=np.average(np.array(diversity),axis=0)
    
    gens=list(range(len(average)))
    plt.plot(gens,average,label='Average Fit.')
    plt.plot(gens,best,label='Best Fit.')
    plt.plot(gens,diversity/6,label='Diversity/6')
    plt.xlabel("Generations")
    plt.legend()
    plt.show()

def plotStatisticsDiferentParameters(statsArray,metricName,parametersValues, name):
    metric=[]

    for stats in statsArray:
        metricSpecificParam=[]
        for run in stats:
            metricSpecificParam.append(run[metricName])
        metricSpecificParam=np.average(np.array(metricSpecificParam),axis=0)
        metric.append(metricSpecificParam)
        
    
    for i,metricSpecificParam in enumerate(metric):
        gens=list(range(len(metricSpecificParam)))
        plt.plot(gens,metricSpecificParam,label='{}'.format(parametersValues[i]))
    plt.xlabel("Generations")
    plt.legend()
    #plt.show()
    plt.savefig(f"./plots/{name}/statistics.png")

def plotMatrix(stats,rowNames,colNames,xlabel,ylabel,title,name):
    stats=np.array(stats)
    fig=plt.figure()
    plt.clf()
    ax=fig.add_subplot(111)
    ax.set_aspect(1)
    res=ax.imshow(stats,cmap=plt.cm.jet,interpolation='nearest')
    height,width=stats.shape
    for x in range(width):
        for y in range(height):
            ax.annotate(str(round(stats[y][x],3)), xy=(x, y), 
                        horizontalalignment='center',
                        verticalalignment='center')
    
    cb = fig.colorbar(res)
    plt.xticks(range(width), colNames)
    plt.yticks(range(height), rowNames)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()
    plt.savefig(f"./plots/{name}/matrix.png")


def plotMultipleRuns(runs,metric,labels):
    gens=list(range(len(runs[0]['average'])))

    for i,stat in enumerate(runs):
        plt.plot(gens,stat[metric],label=labels[i])
    plt.xlabel("Generations")
    plt.legend()
    plt.show()



