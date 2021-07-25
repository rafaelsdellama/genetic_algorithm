""" Command line inferface for package Genetic Algorithm"""
import argparse
import traceback
from utils.logger import setup_logger
from genetic_algorithm.sum_vector_ga import SumVectorGA
from genetic_algorithm.discover_phrase_ga import DiscoverPhraseGA
from genetic_algorithm.optimize_route import OptimizeRoute


TASKS = {
    'SumVectorGA': SumVectorGA,
    'DiscoverPhraseGA': DiscoverPhraseGA,
    'OptimizeRoute': OptimizeRoute
}


def get_ga(task_name):
    """Return a ga for a specific task"""
    ga = TASKS.get(task_name)
    if ga is None:
        raise RuntimeError(
            f"There isn't a valid TASK!\n "
            f"Tasks: {TASKS.keys()}"
        )
    return ga


def main():
    """Parse argments and execute train/predict"""

    parser = argparse.ArgumentParser(
        description="Genetic Algorithm CLI"
    )

    parser.add_argument(
        "--task",
        help="Task to be run. Can be DiscoverPhraseGA, SumVectorGA or OptimizeRoute",
        type=str,
    )

    parser.add_argument(
        "--output-dir",
        default=".",
        help="path to output dir. Default: .",
        type=str,
    )

    parser.add_argument(
        "--nr-max-gen",
        default=100,
        help="Maximum number of generations",
        type=int,
    )

    parser.add_argument(
        "--population-size",
        default=80,
        help="Population size.",
        type=int,
    )

    parser.add_argument(
        "--chromosome-length",
        default=100,
        help="Chromosome length.",
        type=int,
    )

    parser.add_argument(
        "--elitism",
        default=2,
        help="Number of individuals to be selected by elitism.",
        type=int,
    )

    parser.add_argument(
        "--tournament-size",
        default=3,
        help="Number of individuals selected by selection per tournament.",
        type=int,
    )

    parser.add_argument(
        "--crossover-rate",
        default=0.6,
        help="Crossover rate.",
        type=float,
    )

    parser.add_argument(
        "--mutation-rate",
        default=None,
        help="AVG of one mutation per individual.",
    )

    parser.add_argument(
        "--random-immigrants",
        default=True,
        help="If true, each generation immigration_rate percent of the population "
             "is replaced by new random individuals. Elitist individuals can't be replaced.",
        type=bool,
    )

    parser.add_argument(
        "--immigration-rate",
        default=0.05,
        help="Percentage of population to be randomly replaced by new solutions.",
        type=float,
    )

    parser.add_argument(
        "--seed",
        default=0,
        help="Seed to be used by numpy and random.",
        type=int,
    )

    parser.add_argument(
        "--pool-processes",
        default=None,
        help="Number of pool processes.	If None, use max number of cores available on your system.",
    )

    parser.add_argument(
        "--patience",
        default=5,
        help="Number of generation with no improvement after which search will be stopped.",
        type=int,
    )

    parser.add_argument(
        "--selection-method",
        default='roulette',
        help="Selection method. Can be 'tournament' or 'roulette'",
        type=str,
    )

    parser.add_argument(
        "--objective-fitness",
        default=None,
        help="Objective fitness. If fitness is reached, the search ends.",
        type=int,
    )

    parser.add_argument(
        "--objective",
        default='maximization',
        help="Objective of GA. maximization or minimization.",
        type=str,
    )

    args = parser.parse_args()

    # Config the log
    logger = setup_logger("Genetic Algorithm", args.output_dir)
    logger.info(args)

    GA = get_ga(args.task)
    try:
        ga = GA(nr_max_gen=args.nr_max_gen,
                population_size=args.population_size,
                chromosome_length=args.chromosome_length,
                elitism=args.elitism,
                output_dir=args.output_dir,
                tournament_size=args.tournament_size,
                crossover_rate=args.crossover_rate,
                mutation_rate=args.mutation_rate,
                random_immigrants=args.random_immigrants,
                immigration_rate=args.immigration_rate,
                seed=args.seed,
                pool_processes=args.pool_processes,
                patience=args.patience,
                selection_method=args.selection_method,
                objective_fitness=args.objective_fitness,
                objective=args.objective)
        ga.run()

    except Exception:
        msg = f"Failed:\n{traceback.format_exc()}"
        logger.error(msg)


if __name__ == "__main__":
    main()
