from genetic_algorithm.ga import GA


class OptimizeRoute(GA):
    """"""
    def __init__(self, nr_max_gen, population_size, chromosome_length, elitism=2, output_dir='.',
                 tournament_size=3, crossover_rate=0.6, mutation_rate=None,
                 random_immigrants=True, immigration_rate=0.05,
                 seed=0, pool_processes=None, patience=5, selection_method="roulette",
                 objective_fitness=None, objective='maximization'):
        super().__init__(nr_max_gen=nr_max_gen, population_size=population_size,
                         chromosome_length=chromosome_length, elitism=elitism,
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
        raise NotImplementedError("_generating_indiv Not Implemented Yet!")

    def _randomly_mutate(self, chromosome):
        """Randomly mutate indiv custom
            Parameters
            ----------
                chromosome: list
                    Indiv chromosome
            Returns
            -------
        """
        raise NotImplementedError("_randomly_mutate Not Implemented Yet!")

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
        raise NotImplementedError("_calculate_fitness Not Implemented Yet!")

    def _get_options_to_position(self, position):
        raise NotImplementedError("_get_options_to_position Not Implemented Yet!")
