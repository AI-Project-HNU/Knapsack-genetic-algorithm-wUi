import random
import copy


class GeneticAlgorithm:
  

    def __init__(
        self,
        population_size=100,
        generations=200,
        mutation_rate=0.01,
        crossover_rate=0.8,
        elitism_ratio=0.05,
        chromosome_factory=None,
        fitness_fn=None,
        crossover_fn=None,
        mutation_fn=None,
        tournament_size=5,
    ):
    
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism_ratio = elitism_ratio
        self.chromosome_factory = chromosome_factory
        self.fitness_fn = fitness_fn
        self.crossover_fn = crossover_fn
        self.mutation_fn = mutation_fn
        self.tournament_size = tournament_size

        self.best_chromosome = None
        self.best_fitness = float("-inf")
        self.fitness_history = []   
        self.avg_fitness_history = []  

        self._stop_flag = False  


    def initialize_population(self):
       
        return [self.chromosome_factory() for _ in range(self.population_size)]

    def evaluate_population(self, population):
      
        return [self.fitness_fn(chrom) for chrom in population]
    

