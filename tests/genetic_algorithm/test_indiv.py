from genetic_algorithm.indiv import Indiv


def test_indiv():
    indiv = Indiv()
    assert type(indiv) == Indiv


def test_fitness():
    indiv = Indiv()
    assert hasattr(indiv, 'fitness')


def test_chromosome():
    indiv = Indiv()
    assert hasattr(indiv, 'chromosome')
