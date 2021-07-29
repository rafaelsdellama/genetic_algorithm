from genetic_algorithm.ga import GA
import string
import pandas as pd
import random
import numpy as np
import copy


class OptimizeRoute(GA):
    """"""
    def __init__(self, nr_max_gen, population_size, chromosome_length, elitism=2, output_dir='.',
                 tournament_size=3, crossover_rate=0.6, mutation_rate=None,
                 random_immigrants=True, immigration_rate=0.05,
                 seed=0, pool_processes=None, patience=5, selection_method="roulette",
                 objective_fitness=None, objective='maximization'):

        self.df_distances = pd.read_csv("distance_states.csv").set_index("nome")
        self.names = self.df_distances.columns.tolist()
        self.names.sort()
        self._encode = {l: i for i, l in enumerate(self.names)}
        self._decode = {v: k for k, v in self._encode.items()}

        super().__init__(nr_max_gen=nr_max_gen, population_size=population_size,
                         chromosome_length=len(self.names), elitism=elitism,
                         output_dir=output_dir, tournament_size=tournament_size,
                         crossover_rate=crossover_rate, mutation_rate=mutation_rate,
                         random_immigrants=random_immigrants, immigration_rate=immigration_rate,
                         seed=seed, pool_processes=pool_processes, patience=patience,
                         selection_method=selection_method, objective_fitness=objective_fitness,
                         objective=objective)

    def _generating_indiv(self):
        """Generate new indiv custom
        Parameters
            ----------
            Returns
            -------
                New indiv chromosome
        """
        chromosome = copy.deepcopy(self.names)
        random.shuffle(chromosome)
        chromosome = [self._encode[i] for i in chromosome]
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
                options.remove(self._decode[chromosome[i]])

                new_option = self._encode[random.choice(options)]
                old_option = chromosome[i]

                chromosome = np.where(chromosome == new_option, old_option, chromosome)
                chromosome[i] = new_option

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
                    np.array([g for g in parent_2 if g not in np.hstack((parent_1[0: crossover_points[0]], parent_1[crossover_points[1]:]))]),
                    parent_1[crossover_points[1]:],
                )
            )

            child_2 = np.hstack(
                (
                    parent_2[0: crossover_points[0]],
                    np.array([g for g in parent_1 if g not in np.hstack((parent_2[0: crossover_points[0]], parent_2[crossover_points[1]:]))]),
                    parent_2[crossover_points[1]:],
                )
            )

        # one point crossover
        else:
            child_1 = np.hstack(
                (
                    parent_1[0: crossover_points[0]],
                    np.array([g for g in parent_2 if g not in parent_1[0: crossover_points[0]]]),
                )
            )

            child_2 = np.hstack(
                (
                    parent_2[0: crossover_points[0]],
                    np.array([g for g in parent_1 if g not in parent_2[0: crossover_points[0]]]),
                )
            )

        return child_1, child_2

        raise NotImplementedError("_crossover Not Implemented Yet!")

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
        indiv_decoded = [self._decode[i] for i in indiv]
        fitness = 0
        for i in range(0, len(indiv_decoded) - 1):
            fitness = fitness + self.df_distances.loc[indiv_decoded[i], indiv_decoded[i+1]]

        fitness = fitness + self.df_distances.loc[indiv_decoded[-1], indiv_decoded[0]]
        return fitness

    def _get_options_to_position(self, position):
        return copy.deepcopy(self.names)




