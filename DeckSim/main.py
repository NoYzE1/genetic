import random
import subprocess
import sys
import os

class Data:
    cardpool_file = "/home/<user>/.forge/decks/constructed/Cardpool SOI.dck"
    directory = "/home/<user>/.forge/decks/constructed/sim/"
    void = open(os.devnull, "w")
    cardpool = []
    population = []
    args = sys.argv
    verbose = False
    generation = 1
    mutation_rate = 1
    specific = False

class Deck:
    def __init__(self, genes):
        self.genes = genes
        self.fitness = 0

def load():
    if Data.verbose == True:
        print("Loading...")
    for entry in os.listdir(Data.directory):
        if entry != "best.dck":
            genes = []
            deckfile = open(Data.directory + entry, "r")
            start = False
            for line in deckfile:
                if "[Main]" in line:
                    start = True
                    continue
                if start:
                    genes.append(line.strip("\n"))
            Data.population.append(Deck(genes))

def get_cardpool():
    cardlist = open(Data.cardpool_file, "r")
    if Data.verbose == True:
        print("Getting cardpool...")
    start = False
    for line in cardlist.readlines():
        if "[Main]" in line:
            start = True
            continue
        if start:
            n = int(line.split(" ")[0])
            if n > 9:
                for i in range(n):
                    Data.cardpool.append(line[3:-1])
            elif n < 10:
                for i in range(n):
                    Data.cardpool.append(line[2:-1])
    cardlist.close()

def seed():
    if Data.verbose == True:
        print("Seeding...")
    for i in range(64):
        genes = []
        for j in range(60):
            while True:
                random_card = random.choice(Data.cardpool)
                if genes.count(random_card) < Data.cardpool.count(random_card):
                    break
            genes.append(random_card)
        Data.population.append(Deck(genes))

def reseed():
    if Data.verbose == True:
        print("Reseeding...")
    survivors = []
    new_individuals = []
    new_population = []
    for i in range(16):
        survivors.append(Data.population[i])
    for i in range(48):
        rnd1 = random.randint(0, 11)
        rnd2 = random.randint(0, 11)
        while rnd1 == rnd2:
            rnd1 = random.randint(0, 11)
            rnd2 = random.randint(0, 11)
        new_genes = []
        for j in range(30):
            while True:
                random_gene = survivors[rnd1].genes[random.randint(0, 59)]
                if new_genes.count(random_gene) < Data.cardpool.count(random_gene):
                    break
            new_genes.append(random_gene)
        for j in range(30):
            while True:
                random_gene = survivors[rnd2].genes[random.randint(0, 59)]
                if new_genes.count(random_gene) < Data.cardpool.count(random_gene):
                    break
            new_genes.append(random_gene)
        new_individuals.append(Deck(new_genes))
    for i in range(16):
        new_population.append(survivors[i])
    for i in range(48):
        new_population.append(new_individuals[i])
    Data.population = new_population

def write_files():
    if Data.verbose == True:
        print("Writing Files...")
    for i in range(64):
        deck_file = open("/home/<user>/.forge/decks/constructed/sim/deck{0}.dck".format(i), "w")
        string = "[metadata]\nName=deck{0}\n[Main]\n".format(i)
        for line in Data.population[i].genes:
            string += str(line) + "\n"
        deck_file.write(string)
        deck_file.close()

def reset_fitness():
    for i in range(64):
        Data.population[i].fitness = 0

def rate():
    current_round = 0
    current_field = 64
    rounds = []
    for i in range(6 + 1):
        rounds.append([])
    for i in range(64):
        rounds[0].append(i)
    if Data.verbose == True:
        print("Fighting...")
    for i in range(6):
        print("Round {0}".format(current_round + 1))
        for j in range(0, current_field, 2):
            if Data.verbose == True:
                print("Starting match: deck{0} vs deck{1}".format(rounds[current_round][j], rounds[current_round][j + 1]))
            match = subprocess.check_output(["java", "-jar", "forge-gui-desktop-1.5.55-jar-with-dependencies.jar", "sim", "-d", "./sim/deck{0}.dck".format(rounds[current_round][j]), "./sim/deck{0}.dck".format(rounds[current_round][j + 1])], cwd="/home/<user>/Programme/Forge", stderr=Data.void)
            match = str(match)
            if "deck{0} has won".format(rounds[current_round][j]) in match:
                Data.population[rounds[current_round][j]].fitness += 1
                if Data.population[rounds[current_round][j + 1]].fitness > 10:
                    Data.population[rounds[current_round][j + 1]].fitness = 0
                rounds[current_round + 1].append(rounds[current_round][j])
                if Data.verbose == True:
                    print("deck{0} has won".format(rounds[current_round][j]))
                    print("Fitness:", Data.population[rounds[current_round][j]].fitness)
            elif "deck{0} has won".format(rounds[current_round][j + 1]) in match:
                if Data.population[rounds[current_round][j]].fitness > 10:
                    Data.population[rounds[current_round][j]].fitness = 0
                Data.population[rounds[current_round][j + 1]].fitness += 1
                rounds[current_round + 1].append(rounds[current_round][j + 1])
                if Data.verbose == True:
                    print("deck{0} has won".format(rounds[current_round][j + 1]))
                    print("Fitness:", Data.population[rounds[current_round][j + 1]].fitness)
            if Data.verbose == True:
                print(rounds[current_round + 1])
        current_round += 1
        current_field = int(current_field / 2)

def rate_specific():
    enemy_deck = "Angelic Fury"
    if Data.verbose == True:
        print("Fighting...")
    for i in range(64):
        if Data.verbose == True:
            print("Starting match: deck{0} vs {1}".format(i, enemy_deck))
        match = subprocess.check_output(["java", "-jar", "forge-gui-desktop-1.5.55-jar-with-dependencies.jar", "sim", "-d", "./sim/deck{0}.dck".format(i), "./{1}.dck".format(i, enemy_deck)], cwd="/home/<user>/Programme/Forge", stderr=Data.void)
        match = str(match)
        if "deck{0} has won".format(i) in match:
            Data.population[i].fitness += 1
            if Data.verbose == True:
                print("deck{0} has won".format(i))
                print("Fitness:", Data.population[i].fitness)
        elif "{0} has won".format(enemy_deck) in match:
            if Data.verbose == True:
                print("{0} has won".format(enemy_deck))

class DuplicateExeption(Exception):
    def __init__(self, message):
        print(message)

def rate_duplicates():
    if Data.verbose == True:
        print("Rating Duplicates")
    for i in range(64):
        for j in range(60):
            if Data.population[i].genes.count(Data.population[i].genes[j]) > Data.cardpool.count(Data.population[i].genes[j]):
                Data.population[i].fitness = 0
                raise DuplicateExeption([Data.population[i].genes[j], Data.population[i].genes.count(Data.population[i].genes[j]), Data.cardpool.count(Data.population[i].genes[j])])

def sort():
    if Data.verbose == True:
        print("Sorting...")
    sorted_list = []
    for i in range(64):
        best_value = 0
        best_index = 0
        for j in range(len(Data.population)):
            if Data.population[j].fitness > best_value:
                best_value = Data.population[j].fitness
                best_index = j
        best_deck = Data.population.pop(best_index)
        sorted_list.append(best_deck)
    Data.population = sorted_list

def shuffle():
    if Data.verbose == True:
        print("Shuffling...")
    random.shuffle(Data.population)

def mutate():
    if Data.verbose == True:
        print("Mutating...")
    for i in range(Data.mutation_rate):
        i = random.randint(16, 47)
        j = random.randint(0, 59)
        while True:
            k = random.choice(Data.cardpool)
            if Data.population[i].genes.count(k) < Data.cardpool.count(k):
                break
        Data.population[i].genes[j] = k

def write_best():
    best = open(Data.directory + "best.dck", "w")
    string = "[metadata]\nName=best\n[Main]\n"
    for line in Data.population[0].genes:
        string += str(line) + "\n"
    best.write(string)
    best.close()

def read_stats():
    stat_file = open("stats", "r")
    Data.generation = int(stat_file.readline())
    for i in range(64):
        fitness = int(stat_file.readline())
        Data.population[i].fitness = fitness
    stat_file.close()

def write_stats():
    stat_file = open("stats", "w")
    stat_file.write(str(Data.generation) + "\n")
    for i in range(64):
        stat_file.write(str(Data.population[i].fitness) + "\n")
    stat_file.close()

def increase_generation():
    Data.generation += 1

def usage():
    print("""Usage: main.py [-v] [-n | -c] [-s]
    -v Verbose
    -n New
    -c Continue
    -s Specific""")

def population_fitness():
    fitness = 0
    for i in range(64):
        counter = Data.population[i].fitness
        print(counter, end=", ")
        fitness += counter
    print("")
    print("Population Fitness:", fitness)

def main():
    get_cardpool()
    if len(Data.args) == 1:
        usage()
        exit(2)
    elif len(Data.args) == 2:
        if Data.args[1] == "-c":
            load()
            read_stats()
        elif Data.args[1] == "-n":
            seed()
            write_files()
        else:
            usage()
            sys.exit(2)
    elif len(Data.args) == 3:
        if Data.args[1] == "-v":
            Data.verbose = True
        else:
            usage()
            sys.exit(2)
        if Data.args[2] == "-c":
            load()
            read_stats()
        elif Data.args[2] == "-n":
            seed()
            write_files()
        else:
            usage()
            sys.exit(2)
    elif len(Data.args) == 4:
        if Data.args[1] == "-v":
            Data.verbose = True
        else:
            usage()
            sys.exit(2)
        if Data.args[2] == "-c":
            load()
            read_stats()
        elif Data.args[2] == "-n":
            seed()
            write_files()
        else:
            usage()
            sys.exit(2)
        if Data.args[3] == "-s":
            Data.specific = True
        else:
            usage()
            sys.exit(2)

    while True:
        print("Generation:", Data.generation)
        #reset_fitness()
        if Data.specific == True:
            rate_specific()
        else:
            rate()
        rate_duplicates()
        sort()
        write_best()
        population_fitness()
        reseed()
        mutate()
        shuffle()
        write_files()
        increase_generation()
        write_stats()

main()
