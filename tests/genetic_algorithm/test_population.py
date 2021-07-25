import pytest
from genetic_algorithm.population import Population


@pytest.mark.parametrize(
    "population_size", [0, 5, 10],
)
def test_population_len(population_size):
    pop = Population(population_size)
    assert len(pop) == population_size


def test_indivs():
    pop = Population(5)
    assert hasattr(pop, 'indivs')
    assert isinstance(pop.indivs, list)


def test_meanFitness():
    pop = Population(5)
    assert hasattr(pop, 'meanFitness')


def test_maxFitness():
    pop = Population(5)
    assert hasattr(pop, 'maxFitness')


def test_bestIndivs():
    pop = Population(5)
    assert hasattr(pop, 'bestIndivs')
