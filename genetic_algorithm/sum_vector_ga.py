from genetic_algorithm.ga import GA


class SumVectorGA(GA):
    """This genetic algorithm is responsible for optimizing the sum of a given numpy array"""
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
        return sum(indiv) / len(indiv)

    def _get_options_to_position(self, position):
        return [0, 1]
