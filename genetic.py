import random

class Data:
    target = 0
    population = []

class Individual:
    def __init__(self, genes):
        self.genes = genes

def seed():
    for i in range(100):
        genes = []
        for i in range(6):
            genes.append(random.randint(0,100))
        Data.population.append(Individual(genes))

def rate():
    for individual in Data.population:
        individual.fitness = abs(sum(individual.genes) - Data.target)

def sort():
    sorted_list = []
    for i in range(100):
        best_value = 500
        best_index = 0
        for j in range(len(Data.population)):
            if Data.population[j].fitness < best_value:
                best_value = Data.population[j].fitness
                best_index = j
        best_individual = Data.population.pop(best_index)
        sorted_list.append(best_individual)
    Data.population = sorted_list

def reseed():
    survivors = []
    new_individuals = []
    new_population = []
    for i in range(20):
        survivors.append(Data.population.pop(i))
    for i in range(5):
        survivors.append(Data.population.pop(random.randint(0, len(Data.population) - 1)))
    for i in range(75):
        rnd1 = random.randint(0, 24)
        rnd2 = random.randint(0, 24)
        while rnd1 == rnd2:
            rnd1 = random.randint(0, 24)
            rnd2 = random.randint(0, 24)
        first_half = []
        second_half = []
        for i in range(3):
            first_half.append(survivors[rnd1].genes[random.randint(0, 5)])
            second_half.append(survivors[rnd2].genes[random.randint(0, 5)])
        combined = []
        for i in range(3):
            combined.append(first_half[i])
        for i in range(3):
            combined.append(second_half[i])
        new_individuals.append(Individual(combined))
    for i in range(25):
        new_population.append(survivors[i])
    for i in range(75):
        new_population.append(new_individuals[i])
    Data.population = new_population

def mutate():
    rnd = random.randint(25, 99)
    rnd2 = random.randint(0, 5)
    rnd3 = random.randint(0, 100)
    Data.population[rnd].genes[rnd2] = rnd3

def main():
    seed()
    Data.target = int(input("Target: "))
    for i in range(1000):
        rate()
        sort()
        print(Data.population[0].genes, "sum:", sum(Data.population[0].genes))
        reseed()
        mutate()

main()
