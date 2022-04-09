import random

from numpy import size

#create Table
def create_table(size_cromo, min, max,  bidirectional = True):
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


#Generate Individuals
def gen_indiv(size_cromo):
    individual = [num for num in range(size_cromo)]
    random.shuffle(individual)
    return individual

#Order Crossover

def order_crossover(parent1, parent2, prob_crossover):
    
    if random.random() < prob_crossover:
        length = len(parent1[0])

        cromo1 = parent1[0]
        cromo2 = parent2[0]

        #define two cutting points
        cutting_points = random.sample(range(length), 2)
        cutting_points.sort()

        cp1, cp2 = cutting_points

        child1 = [None] * length
        child2 = [None] * length

        #copy middle part
        child1[cp1: cp2 + 1] = cromo1[cp1: cp2 + 1]
        child2[cp1: cp2 + 1] = cromo2[cp1: cp2 + 1]

        #include rest
        fixed = pos

        #first offspring
        pos = (cp2 + 1) % length
        while pos != cp1:
            j = fixed % length
            
            while cromo2[j] in child1:
                j = (j + 1) % size
            
            child1[pos] = cromo2[j]
            pos = (pos + 1) % length

        #second offspring
        pos = (cp2 + 1) % length
        while pos != cp1:
            j = fixed % length
            
            while cromo1[j] in child2:
                j = (j + 1) % size
            
            child2[pos] = cromo1[j]
            pos = (pos + 1) % length

        return ((child1, 0), (child2, 0))

    else:
        return parent1, parent2

#Swap Mutation

def swap_mutation(cromo, prob_mutation):
    if random() < prob_mutation:
        length = len(cromo) - 1
        copy = cromo[:]
        
        i = random.randint(0, length)
        j = random.randint(0, length)
        while i == j:
            i = random.randint(0, length)
            j = random.randint(0, length)
        
        copy[i], copy[j] = copy[j], copy[i]

        return copy

    return cromo

#fenotipo (maybe not needed?)

#fitness

def fitness(individual):
    pass

#tournament

# Evolutionary Algorithm Random Immigrants

# Evolutionary Algorithm Multiple Populations



if __name__ == "__main__":
    numb_generations = 100
    size_pop = 50
    size_cromo = 20
    prob_mut = 0.01
    prob_cross = 0.9


    seed =  1
