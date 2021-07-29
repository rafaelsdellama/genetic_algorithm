import random
import numpy as np
import multiprocessing
import time
import copy
import operator
from abc import abstractmethod
from genetic_algorithm.population import Population
from utils.logger import get_logger
from utils.data_io import save_statistic
from operator import gt, lt, ge, le
from functools import partial


class GA:
    """ This class implements the Genetic Algorithm
        Parameters
        ----------
            nr_max_gen: int
                Maximum number of generations
            population_size: int
                Population size
            chromosome_length: int
                Chomosome lenght
            elitism: int (optional) - Default 2
                Number of individuals to be selected by elitism
            output_dir: str (optional) - Default .
                output dir path
            tournament_size: int (optional) - Default 3
                Number of individuals selected by selection per tournament
            crossover_rate: float (optional) - Default 0.6
                Crossover rate
            mutation_rate: float (optional) - Default 1/chromosome_length
                AVG of one mutation per individual
            random_immigrants: bool (optional) - Default True
                If true, each generation immigration_rate percent
                of the population is replaced by new random individuals.
                elitist individuals can't be replaced
            immigration_rate: float (optional) - Default 0.05
                Percentage of population to be randomly replaced by new solutions.
            seed: int (optional) - Default 0
                Seed to be used by numpy and random
            pool_processes: int (optional) - Default None
                Number of pool processes
                If None, use max number of cores available on your system
            patience: int (optional) - Default 5
                Number of generation with no improvement after which search will be stopped.

        Returns
        -------
    """
    def __init__(self, nr_max_gen, population_size, chromosome_length, elitism=2, output_dir='.',
                 tournament_size=3, crossover_rate=0.6, mutation_rate=None,
                 random_immigrants=True, immigration_rate=0.05,
                 seed=0, pool_processes=None, patience=5, selection_method="roulette",
                 objective_fitness=None, objective='maximization'):
        self.nr_max_gen = nr_max_gen
        self.population_size = population_size
        self.chromosome_length = chromosome_length
        self.elitism = elitism
        self.output_dir = output_dir
        self.tournament_size = tournament_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.random_immigrants = random_immigrants
        self.immigration_rate = immigration_rate
        self._seed = seed
        self.pool_processes = pool_processes
        self.patience = patience
        self.selection_method = selection_method
        self.objective_fitness = objective_fitness
        self.objective = objective

        self.logger = get_logger("Genetic Algorithm")
        self._statistic = []

        # Check variables
        self._check_parameters()

        self.mutation_rate = 1 / self.chromosome_length if self.mutation_rate is None else self.mutation_rate
        self.old_pop = Population(self.population_size)
        self.new_pop = Population(self.population_size)

        self.logger.info(f"GA created!")
        self.logger.info(f"Chromosome_lenght: {self.chromosome_length}")

    def _check_parameters(self):
        """"checks the consistency of all variables before starting GA execution"""
        if not isinstance(self.nr_max_gen, int):
            raise TypeError("nr_max_gen must be a int number")

        if self.nr_max_gen <= 0:
            raise ValueError("(0 < nr_max_gen)")

        if not isinstance(self.population_size, int):
            raise TypeError("population_size must be a int number")

        if self.population_size <= 0:
            raise ValueError("(0 < population_size)")

        if not isinstance(self.chromosome_length, int):
            raise TypeError("chromosome_length must be a int number")

        if self.chromosome_length <= 0:
            raise ValueError("(0 < chromosome_length)")

        if not isinstance(self.elitism, int):
            raise TypeError("elitism must be a int number ")

        if self.elitism <= 0 or self.elitism > self.population_size:
            raise ValueError("(0 < elitism < population_size)")

        if not isinstance(self.crossover_rate, float):
            raise TypeError("crossover_rate must be a float number ")

        if self.crossover_rate <= 0 or self.crossover_rate >= 1:
            raise ValueError("(0 < crossover_rate < 1)")

        if self.mutation_rate is not None and not isinstance(self.mutation_rate, float):
            raise TypeError("mutation_rate must be a float number ")

        if self.mutation_rate is not None and (self.mutation_rate <= 0 or self.mutation_rate >= 1):
            raise ValueError("(0 < mutation_rate < 1)")

        if not isinstance(self.tournament_size, int):
            raise TypeError("tournament_size must be a int number ")

        if self.tournament_size <= 0 or self.tournament_size > self.population_size:
            raise ValueError("(0 < tournament_size < population_size)")

        if not isinstance(self.random_immigrants, bool):
            raise TypeError("random_immigrants must be a bool")

        if not isinstance(self.immigration_rate, float):
            raise TypeError("immigration_rate must be a float number ")

        if self.immigration_rate <= 0 or self.immigration_rate >= 1:
            raise ValueError("(0 < immigration_rate < 1)")

        if not isinstance(self._seed, int):
            raise TypeError("seed must be a int number")

        if not isinstance(self.patience, int):
            raise TypeError("patience must be a int number")

        if self.patience < 0:
            raise ValueError("(0 <= patience)")

        if self.pool_processes is not None and not isinstance(self.pool_processes, int):
            raise TypeError("pool_processes must be a int number or None"
                            "(0 < pool_processes)")

        if not isinstance(self.selection_method, str):
            raise TypeError("selection_method must be a string")

        if self.selection_method not in ["tournament", "roulette"]:
            raise ValueError("selection_method can be ['tournament', 'roulette']")

        if self.pool_processes is not None and not isinstance(self.objective_fitness, float) \
                and not isinstance(self.objective_fitness, int):
            raise TypeError("objective_fitness must be int or float")

        if not isinstance(self.objective, str):
            raise TypeError("objective must be a string")

        if self.objective not in ["minimization", "maximization"]:
            raise ValueError("objective can be ['minimization', 'maximization']")

    def _generate_initial_population(self):
        """Generate a initical population"""
        indivs = []
        for i in range(self.population_size):
            indivs.append(self._generating_indiv())

        pool = multiprocessing.Pool(processes=self.pool_processes)
        outputs = pool.map(self._calculate_fitness, indivs)
        pool.close()

        for i in range(self.population_size):
            self.new_pop.indivs[i].chromosome = indivs[i]
            self.new_pop.indivs[i].fitness = outputs[i]

    def _population_statistic(self):
        """ Calculate the population statistic"""
        self.new_pop.bestIndiv = []
        self.new_pop.sumFitness = 0
        reverse = True if self.objective == 'maximization' else False

        for i in range(0, self.population_size):
            self.new_pop.sumFitness = self.new_pop.sumFitness + self.new_pop.indivs[i].fitness
            self.new_pop.bestIndiv.append((i, self.new_pop.indivs[i].fitness))

        self.new_pop.bestIndiv.sort(key=operator.itemgetter(1), reverse=reverse)
        self.new_pop.bestIndiv = self.new_pop.bestIndiv[0: self.elitism]
        self.new_pop.bestIndiv = [t[0] for t in self.new_pop.bestIndiv]

        self.new_pop.bestFitness = self.new_pop.indivs[
            self.new_pop.bestIndiv[0]
        ].fitness
        self.new_pop.meanFitness = self.new_pop.sumFitness / self.population_size

        self._statistic.append(
            {
                "mean_fitness": self.new_pop.meanFitness,
                "best_fitness": self.new_pop.bestFitness,
                "best_indiv": self.new_pop.indivs[self.new_pop.bestIndiv[0]].chromosome,
                "second_best_indiv": self.new_pop.indivs[self.new_pop.bestIndiv[1]].chromosome
            }
        )

    def _select_individual(self, pop):
        """ Select individual by tournament
            Parameters
            ----------
                pop: Population
                    Pop to be used to select the individual by tournament
            Returns
            -------
                Index of the Indiv selected
        """
        if self.selection_method == 'tournament':
            return self._select_individual_by_tournament(pop)
        elif self.selection_method == 'roulette':
            return self._select_individual_by_roulette(pop)

    def _select_individual_by_tournament(self, pop):
        """ Select individual by tournament
            Parameters
            ----------
                pop: Population
                    Pop to be used to select the individual by tournament
            Returns
            -------
                Index of the Indiv selected (winner)
        """

        compare_op = partial(gt) if self.objective == 'maximization' else partial(lt)

        # Pick individuals for tournament
        fighters = random.sample(
            range(0, self.population_size), self.tournament_size
        )

        # Identify individual with highest fitness
        winner = fighters[0]
        winner_fitness = pop.indivs[fighters[0]].fitness
        for fighter in fighters:
            if compare_op(pop.indivs[fighter].fitness, winner_fitness):
                winner = fighter
                winner_fitness = pop.indivs[fighter].fitness

        return winner

    def _select_individual_by_roulette(self, pop):
        """ Select individual by roulette
            Parameters
            ----------
                pop: Population
                    Pop to be used to select the individual by roulette
            Returns
            -------
                Index of the Indiv selected
        """
        fitness = [f.fitness / pop.sumFitness for f in pop.indivs]

        if self.objective == 'minimization':
            fitness = 1 - np.cumsum(fitness)
            fitness = fitness / sum(fitness)
        fitness = np.cumsum(fitness)
        roulette_value = random.random()
        for idx, f in enumerate(fitness):
            if f > roulette_value:
                return idx

    def _generating_new_population(self):
        """ Generate the new pop from next generation"""
        self.old_pop = copy.deepcopy(self.new_pop)

        for i in range(self.elitism):
            self.new_pop.indivs[i] = copy.deepcopy(
                self.old_pop.indivs[self.old_pop.bestIndiv[i]]
            )

        for i in range(self.elitism, self.population_size, 2):
            parent_1 = self._select_individual(
                self.old_pop
            )
            parent_2 = self._select_individual(
                self.old_pop
            )

            # Crossover
            child_1, child_2 = self._crossover(
                self.old_pop.indivs[parent_1].chromosome,
                self.old_pop.indivs[parent_2].chromosome,
            )

            # Mutation
            self._randomly_mutate(child_1)
            self._randomly_mutate(child_2)

            # child_1
            self.new_pop.indivs[i].chromosome = child_1

            # child_2
            if i + 1 < self.population_size:
                self.new_pop.indivs[i + 1].chromosome = child_2

        if self.random_immigrants:
            for i in range(self.elitism, self.population_size):
                if random.random() < self.immigration_rate:
                    self.new_pop.indivs[
                        i
                    ].chromosome = self._generating_indiv()

        indivs = []
        for i in range(self.elitism, self.population_size):
            indivs.append(self.new_pop.indivs[i].chromosome)

        pool = multiprocessing.Pool(processes=self.pool_processes)
        outputs = pool.map(self._calculate_fitness, indivs)
        pool.close()

        for i in range(len(indivs)):
            self.new_pop.indivs[i + self.elitism].fitness = outputs[i]

    def _crossover(self, parent_1, parent_2):
        """ Generate the new pop from next generation
            Parameters
            ----------
                parent_1: Indiv
                    Indiv to be used to create a new Indiv by crossover
                parent_2: Indiv
                Indiv to be used to create a new Indiv by crossover
            Returns
            -------
                Return two new Indivs
        """
        if random.random() > self.crossover_rate:
            return parent_1, parent_2

        # Pick crossover points
        crossover_points = random.sample(range(0, self.chromosome_length), 2)

        # two points crossover
        if crossover_points[0] != crossover_points[1]:

            # Order by the points. Smaller first
            if crossover_points[0] > crossover_points[1]:
                aux = crossover_points[0]
                crossover_points[0] = crossover_points[1]
                crossover_points[1] = aux

            child_1 = np.hstack(
                (
                    parent_1[0: crossover_points[0]],
                    parent_2[crossover_points[0]: crossover_points[1]],
                    parent_1[crossover_points[1]:],
                )
            )

            child_2 = np.hstack(
                (
                    parent_2[0: crossover_points[0]],
                    parent_1[crossover_points[0]: crossover_points[1]],
                    parent_2[crossover_points[1]:],
                )
            )

        # one point crossover
        else:
            child_1 = np.hstack(
                (
                    parent_1[0: crossover_points[0]],
                    parent_2[crossover_points[0]:],
                )
            )

            child_2 = np.hstack(
                (
                    parent_2[0: crossover_points[0]],
                    parent_1[crossover_points[0]:],
                )
            )

        return child_1, child_2

    def run(self):
        """Run the Genetic Algorithm"""
        self.logger.info("\n\n*************************  Genetic Algorithm   *************************")
        self.logger.info(f"Objective: {self.objective}")
        self.logger.info(f"============================ Execution with seed: {self._seed}  ============================")
        self.logger.info(f"{time.strftime('%d/%m/%Y %H:%M:%S')}\n\n")

        random.seed(self._seed)
        np.random.seed(self._seed)

        self._generate_initial_population()
        self._population_statistic()
        self._print_population_info(self.new_pop, 0)

        best_fitness = self.new_pop.bestFitness
        count_patience = 0

        compare_op_obj = partial(ge) if self.objective == 'maximization' else partial(le)
        compare_op_best = partial(gt) if self.objective == 'maximization' else partial(lt)

        for gen in range(1, self.nr_max_gen + 1):
            self._generating_new_population()
            self._population_statistic()
            self._print_population_info(self.new_pop, gen)

            if compare_op_best(self.new_pop.bestFitness, best_fitness):
                best_fitness = self.new_pop.bestFitness
                count_patience = 0
            else:
                count_patience += 1

            if self.objective_fitness is not None:
                if compare_op_obj(self.new_pop.bestFitness, self.objective_fitness):
                    self.logger.info(f"Stop because found the objective fitness {self.objective_fitness}")
                    break

            if self.patience > 0:
                if count_patience >= self.patience:
                    self.logger.info(f"Stop because patience limit")
                    break

        self.logger.info(f"Best solution found: {self._statistic[-1]['best_indiv']}")
        save_statistic(self.output_dir, self._statistic)

    def _print_population_info(self, pop, gen):
        """Print population info
        Parameters
            ----------
                pop: Population
                    Pop to be print info
                gen: int
                    Gen number
            Returns
            -------
        """

        self.logger.info(
            f"Generation: {gen} - {time.strftime('%d/%m/%Y %H:%M:%S')}\n"
            f"Fitness best indiv: {pop.bestFitness}\n"
            f"Best indivs index: {pop.bestIndiv}\n"
            f"Best solution found so far: {pop.indivs[pop.bestIndiv[0]].chromosome}\n"
            f"Fitness mean: {pop.meanFitness}\n"
            f"Mutation rate: {self.mutation_rate}\n\n"
        )

    def _generating_indiv(self):
        """Generate new indiv custom
        Parameters
            ----------
            Returns
            -------
                New indiv chromosome
        """
        chromosome = [random.choice(self._get_options_to_position(i)) for i in range(self.chromosome_length)]
        return np.array(chromosome, dtype=object)

    def _randomly_mutate(self, chromosome):
        """Randomly mutate indiv custom
            Parameters
            ----------
                chromosome: list
                    Indiv chromosome
            Returns
            -------
        """
        for i in range(self.chromosome_length):
            if random.random() < self.mutation_rate:
                options = self._get_options_to_position(i)
                if len(options) > 1:
                    options.remove(chromosome[i])
                chromosome[i] = random.choice(options)

    @abstractmethod
    def _calculate_fitness(self, indiv):
        """Calculate fitness from indiv
        Parameters
            ----------
                indiv: Indiv
                    Indiv to calculate the fitness
            Returns
            -------
                fitness: float
                    return indiv fitness
        """
        raise NotImplementedError("_calculate_fitness Not Implemented Yet!")

    @abstractmethod
    def _get_options_to_position(self, position):
        raise NotImplementedError("_get_options_to_position Not Implemented Yet!")
