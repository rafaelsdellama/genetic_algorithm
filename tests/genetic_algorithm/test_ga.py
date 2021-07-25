"""Tests for GA."""
import pytest
from genetic_algorithm.ga import GA
from utils.logger import setup_logger

pytest_output_directory = "./Pytest_output"
logger = setup_logger("Allocation", pytest_output_directory)


@pytest.mark.parametrize(
    "max_gen, pop_size",
    [
        (2, 3),
        (2, 4)
    ]
)
def test_success_ga(max_gen, pop_size):
    ga = GA(nr_max_gen=max_gen, population_size=pop_size, output_dir=pytest_output_directory)
    ga.run()


@pytest.mark.parametrize(
    "max_gen", ["wrong", 1.1],
)
def test_wrong_max_gen_type(max_gen):
    with pytest.raises(TypeError):
        GA(nr_max_gen=max_gen, population_size=10)


@pytest.mark.parametrize(
    "max_gen", [0, -1],
)
def test_wrong_max_gen_value(max_gen):
    with pytest.raises(ValueError):
        GA(nr_max_gen=max_gen, population_size=10)


@pytest.mark.parametrize(
    "pop_size", ["wrong", 1.1],
)
def test_wrong_pop_size_type(pop_size):
    with pytest.raises(TypeError):
        GA(nr_max_gen=2, population_size=pop_size)


@pytest.mark.parametrize(
    "pop_size", [0, -1],
)
def test_wrong_pop_size_value(pop_size):
    with pytest.raises(ValueError):
        GA(nr_max_gen=2, population_size=pop_size)


@pytest.mark.parametrize(
    "chromosome_length", ["wrong", 1.1],
)
def test_wrong_chromosome_length_type(chromosome_length):
    with pytest.raises(TypeError):
        GA(nr_max_gen=2, population_size=4, chromosome_length=chromosome_length)


@pytest.mark.parametrize(
    "chromosome_length", [0, -1],
)
def test_wrong_chromosome_length_value(chromosome_length):
    with pytest.raises(ValueError):
        GA(nr_max_gen=2, population_size=4, chromosome_length=chromosome_length)


@pytest.mark.parametrize(
    "pop_size, elitism", [
        (5, "wrong"),
        (5, 0.1),
    ],
)
def test_wrong_elitism_type(pop_size, elitism):
    with pytest.raises(TypeError):
        GA(nr_max_gen=2, population_size=pop_size,
           elitism=elitism)


@pytest.mark.parametrize(
    "pop_size, elitism", [
        (5, -1),
        (5, 10)
    ],
)
def test_wrong_elitism_value(pop_size, elitism):
    with pytest.raises(ValueError):
        GA(nr_max_gen=2, population_size=pop_size,
           elitism=elitism)


@pytest.mark.parametrize(
    "crossover_rate", ["wrong", 2],
)
def test_wrong_crossover_rate_type(crossover_rate):
    with pytest.raises(TypeError):
        GA(nr_max_gen=2, population_size=4,
           crossover_rate=crossover_rate)


@pytest.mark.parametrize(
    "crossover_rate", [-1.1, 1.1],
)
def test_wrong_crossover_rate_value(crossover_rate):
    with pytest.raises(ValueError):
        GA(nr_max_gen=2, population_size=4,
           crossover_rate=crossover_rate)


@pytest.mark.parametrize(
    "mutation_rate", ["wrong", 2],
)
def test_wrong_mutation_rate_type(mutation_rate):
    with pytest.raises(TypeError):
        GA(nr_max_gen=2, population_size=4,
           mutation_rate=mutation_rate)


@pytest.mark.parametrize(
    "mutation_rate", [-1.1, 1.1],
)
def test_wrong_mutation_rate_value(mutation_rate):
    with pytest.raises(ValueError):
        GA(nr_max_gen=2, population_size=4,
           mutation_rate=mutation_rate)


@pytest.mark.parametrize(
    "pop_size, tournament_size", [
        (5, "wrong"),
        (5, 1.1)
    ],
)
def test_wrong_tournament_size_type(pop_size, tournament_size):
    with pytest.raises(TypeError):
        GA(nr_max_gen=2, population_size=pop_size,
           tournament_size=tournament_size)


@pytest.mark.parametrize(
    "pop_size, tournament_size", [
        (5, -1),
        (5, 10)
    ],
)
def test_wrong_tournament_size_value(pop_size, tournament_size):
    with pytest.raises(ValueError):
        GA(nr_max_gen=2, population_size=pop_size,
           tournament_size=tournament_size)


@pytest.mark.parametrize(
    "rd_imigrantes", ["wrong", 0.1, 1],
)
def test_wrong_rd_imigrantes_type(rd_imigrantes):
    with pytest.raises(TypeError):
        GA(nr_max_gen=2, population_size=4,
           random_immigrants=rd_imigrantes)


@pytest.mark.parametrize(
    "imigration_rate", ["wrong", 0],
)
def test_wrong_imigration_rate_type(imigration_rate):
    with pytest.raises(TypeError):
        GA(nr_max_gen=2, population_size=4,
           immigration_rate=imigration_rate)


@pytest.mark.parametrize(
    "imigration_rate", [-1.1, 1.1],
)
def test_wrong_imigration_rate_value(imigration_rate):
    with pytest.raises(ValueError):
        GA(nr_max_gen=2, population_size=4,
           immigration_rate=imigration_rate)


@pytest.mark.parametrize(
    "seed", ["wrong", 1.1],
)
def test_wrong_seed(seed):
    with pytest.raises(TypeError):
        GA(nr_max_gen=2, population_size=4,
           seed=seed)


@pytest.mark.parametrize(
    "patience", ["wrong", 1.1],
)
def test_wrong_patience_type(patience):
    with pytest.raises(TypeError):
        GA(nr_max_gen=2, population_size=4,
           patience=patience)


@pytest.mark.parametrize(
    "patience", [-1],
)
def test_wrong_patience_value(patience):
    with pytest.raises(ValueError):
        GA(nr_max_gen=2, population_size=4,
           patience=patience)


@pytest.mark.parametrize(
    "pool_processes", ["wrong", 1.1],
)
def test_wrong_pool_processes(pool_processes):
    with pytest.raises(TypeError):
        GA(nr_max_gen=2, population_size=4,
           pool_processes=pool_processes)


@pytest.mark.parametrize(
    "selection_method", ["wrong"],
)
def test_wrong_selection_method_value(selection_method):
    with pytest.raises(ValueError):
        GA(nr_max_gen=2, population_size=4,
           selection_method=selection_method)


@pytest.mark.parametrize(
    "selection_method", [1, 1.1],
)
def test_wrong_selection_method_type(selection_method):
    with pytest.raises(TypeError):
        GA(nr_max_gen=2, population_size=4,
           selection_method=selection_method)


@pytest.mark.parametrize(
    "objective_fitness", ["wrong"],
)
def test_wrong_objective_fitness_type(objective_fitness):
    with pytest.raises(TypeError):
        GA(nr_max_gen=2, population_size=4,
           objective_fitness=objective_fitness)
