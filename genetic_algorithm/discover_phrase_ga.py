from genetic_algorithm.ga import GA
import string


class DiscoverPhraseGA(GA):
    """This genetic algorithm is responsible for discovering a certain phrase"""
    def __init__(self, nr_max_gen, population_size, chromosome_length, elitism=2, output_dir='.',
                 tournament_size=3, crossover_rate=0.6, mutation_rate=None,
                 random_immigrants=True, immigration_rate=0.05,
                 seed=0, pool_processes=None, patience=5, selection_method="roulette",
                 objective_fitness=None, objective='maximization'):
        self.phrase = "O nosso Algoritmo Genetico tem por objetivo descobrir essa frase simples."
        super().__init__(nr_max_gen=nr_max_gen, population_size=population_size,
                         chromosome_length=len(self.phrase), elitism=elitism,
                         output_dir=output_dir, tournament_size=tournament_size,
                         crossover_rate=crossover_rate, mutation_rate=mutation_rate,
                         random_immigrants=random_immigrants, immigration_rate=immigration_rate,
                         seed=seed, pool_processes=pool_processes, patience=patience,
                         selection_method=selection_method, objective_fitness=objective_fitness,
                         objective=objective
                         )

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

        def _compare_strings(str1, str2):
            str1 = list(str1)
            str2 = list(str2)
            count = 0

            for i in range(len(str1)):
                if str1[i] == str2[i]:
                    count = count + 1

            return count

        return _compare_strings(self.phrase, indiv) / len(indiv)

    def _get_options_to_position(self, position):
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        punctuation = string.punctuation + ' '
        digits = string.digits

        return list(lowercase + uppercase + punctuation + digits)
