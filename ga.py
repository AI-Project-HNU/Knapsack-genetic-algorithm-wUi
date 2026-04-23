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
       
        return [self.chromosome_factory() for _ in range(self.population_size)]# type: ignore

    def evaluate_population(self, population):
      
        return [self.fitness_fn(chrom) for chrom in population]# type: ignore
    

    def tournament_selection(self, population, fitnesses):
        competitors_idx= random.sample(range(len(population)), self.tournament_size)
        best_idx=max(competitors_idx, key=lambda i:fitnesses[i])
        return copy.deepcopy(population[best_idx])
    

    def apply_elitism(self, population, fitnesses):
        elite_count = max(1, int(self.elitism_ratio * self.population_size))
        sorted_pairs = sorted(
            zip(fitnesses, population), key=lambda x: x[0], reverse=True
        )
        return [copy.deepcopy(chrom) for _, chrom in sorted_pairs[:elite_count]]
    
    def evolve(self, progress_callback=None):

        self._stop_flag = False
        self.fitness_history = []
        self.avg_fitness_history = []
        self.best_chromosome = None
        self.best_fitness = float("-inf")

        population = self.initialize_population()

        for generation in range(self.generations):
            if self._stop_flag:
                break

            fitnesses = self.evaluate_population(population)
            gen_best_idx = max(range(len(fitnesses)), key=lambda i: fitnesses[i])
            gen_best_fitness = fitnesses[gen_best_idx]
            gen_avg_fitness = sum(fitnesses) / len(fitnesses)

            self.fitness_history.append(gen_best_fitness)
            self.avg_fitness_history.append(gen_avg_fitness)

            if gen_best_fitness > self.best_fitness:
                self.best_fitness = gen_best_fitness
                self.best_chromosome = copy.deepcopy(population[gen_best_idx])

            if progress_callback:       #USE THIS IN GUI
                progress_callback(generation, self.best_fitness, self.best_chromosome)

            elites = self.apply_elitism(population, fitnesses)

            next_population = elites[:]

            while len(next_population) < self.population_size:
                parent_a = self.tournament_selection(population, fitnesses)
                parent_b = self.tournament_selection(population, fitnesses)

                if random.random() < self.crossover_rate:
                    child_a, child_b = self.crossover_fn(parent_a, parent_b)# type: ignore
                else:
                    child_a, child_b = copy.deepcopy(parent_a), copy.deepcopy(parent_b)

                child_a = self.mutation_fn(child_a, self.mutation_rate)# type: ignore
                child_b = self.mutation_fn(child_b, self.mutation_rate)# type: ignore

                next_population.append(child_a)
                if len(next_population) < self.population_size:
                    next_population.append(child_b)

            population = next_population

        return (
            self.best_chromosome,
            self.best_fitness,
            self.fitness_history,
            self.avg_fitness_history,
        )

    def stop(self):     #USE THIS FUNCTION IN GUI
        self._stop_flag = True