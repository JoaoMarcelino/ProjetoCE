from random import random, randint, seed, sample, choice, shuffle, randrange
from math import sqrt
from tqdm import tqdm
from operator import itemgetter
from utils import *

# create Table


def create_table(size_cromo, min, max,  bidirectional=True):
    table = [[0] * size_cromo for i in range(size_cromo)]

    if bidirectional:
        for i, row in enumerate(table):
            for j in range(i + 1, len(row)):
                if i != j:
                    value = random.randint(min, max + 1)
                    table[i][j] = value
                    table[j][i] = value

    else:
        for i, row in enumerate(table):
            for j, elem in enumerate(row):
                if i != j:
                    row[j] = random.randint(min, max + 1)

    return table


def readDataset(targetFile):
    with open(targetFile, 'r') as file:
        lines = file.readlines()
        coordLines = lines[6:-1]
        coordLines = [line.strip('\n').split() for line in coordLines]

        cities = {}
        for i, line in enumerate(coordLines):
            line = line[1:]
            line = tuple((float(coord) for coord in line))
            cities[i] = line
        return cities


def generatePopulation(popSize, genoSize):
    return [(generateIndividual(genoSize), 0) for i in range(popSize)]


def generateIndividual(genoSise):
    individual = [num for num in range(genoSise)]
    shuffle(individual)
    return individual


def orderCrossover(parent1, parent2, probCrossover):

    if random() < probCrossover:
        genoSise = len(parent1[0])

        cromo1 = parent1[0]
        cromo2 = parent2[0]

        # define two cutting points
        cutting_points = sample(range(genoSise), 2)
        cutting_points.sort()

        cp1, cp2 = cutting_points

        child1 = [None] * genoSise
        child2 = [None] * genoSise

        # copy middle part
        child1[cp1: cp2 + 1] = cromo1[cp1: cp2 + 1]
        child2[cp1: cp2 + 1] = cromo2[cp1: cp2 + 1]

        # include rest
        # first offspring
        pos = (cp2 + 1) % genoSise
        fixed = pos
        while pos != cp1:
            j = fixed % genoSise
            while cromo2[j] in child1:
                j = (j + 1) % genoSise
            child1[pos] = cromo2[j]
            pos = (pos + 1) % genoSise

        # second offspring
        pos = (cp2 + 1) % genoSise
        while pos != cp1:
            j = fixed % genoSise
            while cromo1[j] in child2:
                j = (j + 1) % genoSise
            child2[pos] = cromo1[j]
            pos = (pos + 1) % genoSise

        return [(child1, 0), (child2, 0)]
    else:
        return [parent1, parent2]


def swapMutation(cromo, probMutation):
    if random() < probMutation:
        genoSize = len(cromo) - 1
        copy = cromo[:]

        i = randint(0, genoSize)
        j = randint(0, genoSize)
        while i == j:
            i = randint(0, genoSize)
            j = randint(0, genoSize)

        copy[i], copy[j] = copy[j], copy[i]
        return copy
    return cromo


def fitness(genotype, cities, knownAnswer):
    nCities = len(genotype)
    totalDistance = 0
    for i in range(nCities):
        j = (i+1) % nCities
        totalDistance += distance(genotype[i], genotype[j], cities)
    return knownAnswer/totalDistance

def distance(city1, city2, cities):
    x1, y1 = cities[city1]
    x2, y2 = cities[city2]

    dx = x1-x2
    dy = y1-y2
    dist = sqrt(dx**2+dy**2)
    return dist


def tournamentSelection(pop, tournSize):
    size_pop = len(pop)
    mate_pool = []
    for i in range(size_pop):
        winner = one_tour(pop, tournSize)
        mate_pool.append(winner)
    return mate_pool


def one_tour(population, size):
    pool = sample(population, size)
    pool.sort(key=itemgetter(1), reverse=True)
    return pool[0]


def survivalSelection(population, offsprings, elitRate):
    population = population.copy()
    offsprings = offsprings.copy()

    popSize = len(population)
    elitSize = round(elitRate*popSize)

    population.sort(key=itemgetter(1), reverse=True)
    offsprings.sort(key=itemgetter(1), reverse=True)
    return population[0:elitSize]+offsprings[0:popSize-elitSize]


def bestMigrantSelection(population, migrationRate):
    popSize = len(population)
    population = population.copy()

    population.sort(key=itemgetter(1), reverse=True)
    migrants = population[0:round(migrationRate*popSize)]
    return migrants


def worstMigrantReplacement(population, migrants):
    population = population.copy()

    popSize = len(population)
    migSize = len(migrants)

    population.sort(key=itemgetter(1), reverse=True)
    population = population[0:popSize-migSize]+migrants
    return population


# Evolutionary Algorithm Random Immigrants
def seaRI(nGenerations, popSize, genoSize, probCross, probMut, tournSize, elitRate, crossoverFunc, mutationFunc, parentSelectionFunc, survivalSelectionFuc, fitnessFunc, migrationInterval, migrationRate, migrantReplacementFunc, seedNumber, cities, knownAnswer):
    stats = {}
    seed(seedNumber)
    gensOfMigration = list(range(0, nGenerations, migrationInterval))
    nImigrants = round(migrationRate*popSize)

    # inicialize population: indiv = (cromo,fit)
    population = generatePopulation(popSize, genoSize)

    # evaluate population
    population = [(indiv, fitnessFunc(indiv, cities, knownAnswer))
                  for indiv, fitness in population]
    stats=updateStatistics(stats,population)

    for gen in tqdm(range(nGenerations)):
        # sparents selection
        parents = parentSelectionFunc(population, tournSize)
        offsprings = []
        # Crossover
        for i in range(0, popSize-1, 2):
            indiv_1 = parents[i]
            indiv_2 = parents[i+1]
            sons = crossoverFunc(indiv_1, indiv_2, probCross)
            offsprings += sons
        # Mutation
        for i, indiv in enumerate(offsprings):
            newGeno = mutationFunc(indiv[0], probMut)
            offsprings[i] = (newGeno, fitnessFunc(
                newGeno, cities, knownAnswer))

        # New population
        population = survivalSelectionFuc(population, offsprings, elitRate)

        if gen in gensOfMigration:
            population = migrantReplacementFunc(
                population, generatePopulation(nImigrants, genoSize))

        population = [(indiv, fitnessFunc(indiv, cities, knownAnswer))
                      for indiv, fitness in population]
        stats=updateStatistics(stats,population)
    return stats

# Evolutionary Algorithm Two Populations


def seaDP(nGenerations, popSize, genoSize, probCross, probMut, tournSize, elitRate, crossoverFunc, mutationFunc, parentSelectionFunc, survivalSelectionFuc, fitnessFunc, migrationInterval, migrationRate, migrantReplacementFunc, migrantSelectionFunc, seedNumber, cities, knownAnswer):
    stats = {}
    seed(seedNumber)
    gensOfMigration = list(range(0, nGenerations, migrationInterval))
    popSize = round(popSize/2)
    nImigrants = round(migrationRate*popSize)

    # inicialize population: indiv = (cromo,fit)
    populations = [generatePopulation(popSize, genoSize) for i in range(2)]

    # evaluate population
    populations = [[(indiv, fitnessFunc(indiv, cities, knownAnswer))
                    for indiv, fitness in population] for population in populations]
    stats=updateStatistics(stats,populations[0]+populations[1])

    for gen in tqdm(range(nGenerations)):
        for k, population in enumerate(populations):
            # sparents selection
            parents = parentSelectionFunc(population, tournSize)
            offsprings = []
            # Crossover
            for i in range(0, popSize-1, 2):
                indiv_1 = parents[i]
                indiv_2 = parents[i+1]
                sons = crossoverFunc(indiv_1, indiv_2, probCross)
                offsprings += sons
            # Mutation
            for i, indiv in enumerate(offsprings):
                newGeno = mutationFunc(indiv[0], probMut)
                offsprings[i] = (newGeno, fitnessFunc(
                    newGeno, cities, knownAnswer))

            # New population

            population = survivalSelectionFuc(population, offsprings, elitRate)
            population = [(indiv, fitnessFunc(indiv, cities, knownAnswer))
                          for indiv, fitness in population]
            populations[k] = population

        if gen in gensOfMigration:
            migrants = [migrantSelectionFunc(
                population, migrationRate) for population in populations]
            populations[0] = migrantReplacementFunc(
                populations[0], migrants[1])
            populations[1] = migrantReplacementFunc(
                populations[1], migrants[0])

        populations = [[(indiv, fitnessFunc(indiv, cities, knownAnswer))
                        for indiv, fitness in population] for population in populations]
        stats=updateStatistics(stats,populations[0]+populations[1])
    return stats


if __name__ == "__main__":

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
    migrationRate = 0.05
    migrationInterval = 20
    seedNumber = 1

    fitnessFunc = fitness
    crossoverFunc = orderCrossover
    mutationFunc = swapMutation

    parentSelectionFunc = tournamentSelection
    survivalSelectionFuc = survivalSelection
    migrantReplacementFunc = worstMigrantReplacement

    results = seaRI(nGenerations, popSize, genoSize, probCross, probMut, tournSize, elitRate, crossoverFunc, mutationFunc, parentSelectionFunc,
                    survivalSelectionFuc, fitnessFunc, migrationInterval, migrationRate, migrantReplacementFunc, seedNumber, cities, knownAnswer)
    plotStatistics(results)
    writeStatisticsToFile(results,"./results/run1.json")
