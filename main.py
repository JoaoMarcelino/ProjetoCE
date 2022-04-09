import random
from operator import itemgetter

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

#Generate Population
def gen_pop(size_pop, size_cromo):
    return [(gen_indiv, 0) for i in range(size_pop)]

#Generate Individual
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
                j = (j + 1) % length
            
            child1[pos] = cromo2[j]
            pos = (pos + 1) % length

        #second offspring
        pos = (cp2 + 1) % length
        while pos != cp1:
            j = fixed % length
            
            while cromo1[j] in child2:
                j = (j + 1) % length
            
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

# Parents Selection: tournament
def tour_sel(t_size):
    def tournament(pop):
        size_pop= len(pop)
        mate_pool = []
        for i in range(size_pop):
            winner = one_tour(pop,t_size)
            mate_pool.append(winner)
        return mate_pool
    return tournament

def one_tour(population,size):
    """Minimization Problem. Deterministic"""
    pool = random.sample(population, size)
    pool.sort(key=itemgetter(1), reverse=False)
    return pool[0]

def best_pop(populacao):
    populacao.sort(key=itemgetter(1),reverse=False)
    return populacao[0]

#Survivors Selection

def survivor_selection():
    pass


# Evolutionary Algorithm Random Immigrants
def sea_ri(numb_generations,size_pop, size_cromo, prob_cross,sel_parents,crossover,mutation,sel_survivors, fitness_func):
    
    # inicialize population: indiv = (cromo,fit)
    population = gen_pop(size_pop,size_cromo)

    # evaluate population
    population = [(indiv, fitness_func(indiv)) for indiv, fitness in populacao]

    for gen in range(numb_generations):

        # sparents selection
        mate_pool = sel_parents(populacao)

        # Variation
        # ------ Crossover
        progenitores = []
        for i in  range(0,size_pop-1,2):
            indiv_1= mate_pool[i]
            indiv_2 = mate_pool[i+1]
            filhos = crossover(indiv_1,indiv_2, prob_cross)
            progenitores.extend(filhos) 

        # ------ Mutation
        descendentes = []
        for cromo,fit in progenitores:
            novo_cromo = mutation(cromo, size_cromo)
            descendentes.append((novo_cromo,fitness_func(novo_cromo)))

        # New population
        populacao = sel_survivors(populacao,descendentes)

        # Evaluate the new population
        populacao = [(indiv[0], fitness_func(indiv[0])) for indiv in populacao]     

    return best_pop(populacao)

# Evolutionary Algorithm Multiple Populations



if __name__ == "__main__":
    numb_generations = 100
    size_pop = 50
    size_cromo = 20
    prob_mut = 0.01
    prob_cross = 0.9


    seed =  1
