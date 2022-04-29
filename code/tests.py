from main import *
from utils import *

def test_gen(x):
    print(gen_indiv(x))

def test_table(size, min, max):

    print("Unidirectional")

    table = create_table(size, min, max, bidirectional=False)
    for i, row in enumerate(table):
        print(row)

    print("Bidirectional")

    table = create_table(size, min, max)
    for i, row in enumerate(table):
        print(row)

def test1():
    """
    datasetFileName = './berlin52.tsp'
    cities = readDataset(datasetFileName)
    knownAnswer = 7544.3
    nGenerations = 200
    popSize = 100
    genoSize = len(cities.keys())
    probMut = 0.05
    probCross = 0.9
    tournSize = 3
    elitRate = 0.05
    #migrationRate = 0.05
    #migrationInterval = 20
    #seedNumber = 1

    fitnessFunc = fitness
    crossoverFunc = orderCrossover
    mutationFunc = swapMutation

    parentSelectionFunc = tournamentSelection
    survivalSelectionFuc = survivalSelection
    migrantReplacementFunc = worstMigrantReplacement
    migrantSelectionFunc= bestMigrantSelection
    
    i=0
    for migrationRate in [0.05, 0.2, 0.5, 0.8]:
        for migrationInterval in [5, 10, 20, 40, 100]:
            for seedNumber in range(30):
                results = seaDP(nGenerations, popSize, genoSize, probCross, probMut, tournSize, elitRate, crossoverFunc, mutationFunc, parentSelectionFunc, survivalSelectionFuc, fitnessFunc, migrationInterval, migrationRate, migrantReplacementFunc, migrantSelectionFunc, seedNumber, cities, knownAnswer)
                results["migrationRate"]=migrationRate
                results["migrationInterval"]=migrationInterval
                results["seedNumber"]=seedNumber
                writeStatisticsToFile(results,"./results/test1/run{}.json".format(i))
                i+=1
    """
    i=0
    results=[]
    parameterValues=[]
    for migrationRate in [0.05, 0.2, 0.5, 0.8]:
        for migrationInterval in [5, 10, 20, 40, 100]:
            runs=[]
            for k in range(30):
                runs.append(readStatisticsToFile("./results/test1/run{}.json".format(i)))
                i+=1
            results.append(runs)
            parameterValues.append("mi={} mr={}".format(migrationInterval,migrationRate))

    plotStatisticsDiferentParameters(results, 'best',parameterValues)

    i=0
    results=[]
    colNames=["5", "10", "20", "40", "100"]
    rowNames=["0.05", "0.2", "0.5","0.8"]
    metric='best'
    title="Average of best fitness value"
    xlabel="Migration Interval"
    ylabel="Migration Rate"
    for migrationRate in [0.05, 0.2, 0.5, 0.8]:
        row=[]
        for migrationInterval in [5, 10, 20, 40, 100]:
            runs=[]
            for k in range(30):
                runs.append(readStatisticsToFile("./results/test1/run{}.json".format(i))[metric][-1])
                i+=1
            row.append(np.average(np.array(runs)))
        results.append(row)

    plotMatrix(results, rowNames, colNames,xlabel,ylabel,title)


def test2():
    
    testName="test2"
    """
    datasetFileName = './berlin52.tsp'
    cities = readDataset(datasetFileName)
    knownAnswer = 7544.3
    nGenerations = 200
    popSize = 100
    genoSize = len(cities.keys())
    probMut = 0.05
    probCross = 0.9
    tournSize = 3
    elitRate = 0.05
    #migrationRate = 0.05
    #migrationInterval = 20
    #seedNumber = 1

    fitnessFunc = fitness
    crossoverFunc = orderCrossover
    mutationFunc = swapMutation

    parentSelectionFunc = tournamentSelection
    survivalSelectionFuc = survivalSelection
    migrantReplacementFunc = worstMigrantReplacement
    migrantSelectionFunc= bestMigrantSelection
    
    i=0
    for migrationRate in [0.05, 0.2, 0.5, 0.8]:
        for migrationInterval in [5, 10, 20, 40, 100]:
            for seedNumber in range(30):
                results = seaRI(nGenerations, popSize, genoSize, probCross, probMut, tournSize, elitRate, crossoverFunc, mutationFunc, parentSelectionFunc, survivalSelectionFuc, fitnessFunc, migrationInterval, migrationRate, migrantReplacementFunc, seedNumber, cities, knownAnswer)
                results["migrationRate"]=migrationRate
                results["migrationInterval"]=migrationInterval
                results["seedNumber"]=seedNumber
                writeStatisticsToFile(results,"./results/{}/run{}.json".format(testName,i))
                i+=1
    """
    i=0
    results=[]
    parameterValues=[]
    for migrationRate in [0.05, 0.2, 0.5, 0.8]:
        for migrationInterval in [5, 10, 20, 40, 100]:
            runs=[]
            for k in range(30):
                runs.append(readStatisticsToFile("./results/{}/run{}.json".format(testName,i)))
                i+=1
            results.append(runs)
            parameterValues.append("mi={} mr={}".format(migrationInterval,migrationRate))

    plotStatisticsDiferentParameters(results, 'best',parameterValues)

    i=0
    results=[]
    colNames=["5", "10", "20", "40", "100"]
    rowNames=["0.05", "0.2", "0.5","0.8"]
    metric='best'
    title="Average of best fitness value" 
    #title="Average diversity of last generation"
    xlabel="Migration Interval"
    ylabel="Migration Rate"
    for migrationRate in [0.05, 0.2, 0.5, 0.8]:
        row=[]
        for migrationInterval in [5, 10, 20, 40, 100]:
            runs=[]
            for k in range(30):
                runs.append(readStatisticsToFile("./results/{}/run{}.json".format(testName,i))[metric][-1])
                i+=1
            row.append(np.average(np.array(runs)))
        results.append(row)

    plotMatrix(results, rowNames, colNames,xlabel,ylabel,title)
if __name__=="__main__":
    test2()