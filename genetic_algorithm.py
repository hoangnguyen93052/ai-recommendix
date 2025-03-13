import numpy as np
import random
import matplotlib.pyplot as plt

class GeneticAlgorithm:
    def __init__(self, function, num_genes, population_size, mutation_rate, generations):
        self.function = function
        self.num_genes = num_genes
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.population = self.initialize_population()
    
    def initialize_population(self):
        return [np.random.uniform(-5, 5, self.num_genes) for _ in range(self.population_size)]

    def fitness(self, individual):
        return -self.function(individual)

    def select_parent(self):
        tournament_size = 3
        tournament = random.sample(self.population, tournament_size)
        tournament.sort(key=self.fitness)
        return tournament[-1]

    def crossover(self, parent1, parent2):
        crossover_point = random.randint(1, self.num_genes - 1)
        offspring = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
        return offspring

    def mutate(self, individual):
        for gene in range(self.num_genes):
            if random.random() < self.mutation_rate:
                individual[gene] += np.random.normal()
        return individual

    def evolve(self):
        for generation in range(self.generations):
            new_population = []
            for _ in range(self.population_size):
                parent1 = self.select_parent()
                parent2 = self.select_parent()
                offspring = self.crossover(parent1, parent2)
                offspring = self.mutate(offspring)
                new_population.append(offspring)
            self.population = new_population
            self.log_best(generation)
    
    def log_best(self, generation):
        best_individual = max(self.population, key=self.fitness)
        best_fitness = self.fitness(best_individual)
        print(f'Generation {generation}: Best Fitness = {best_fitness}, Best Individual = {best_individual}')

    def plot_results(self):
        x = np.linspace(-5, 5, 100)
        y = self.function(x)
        plt.plot(x, y)
        plt.title('Function Optimization using Genetic Algorithm')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.grid()
        plt.show()

def example_function(x):
    return np.sum(x**2)

if __name__ == '__main__':
    num_genes = 10
    population_size = 100
    mutation_rate = 0.01
    generations = 50
    ga = GeneticAlgorithm(example_function, num_genes, population_size, mutation_rate, generations)
    ga.evolve()
    ga.plot_results()