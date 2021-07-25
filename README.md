# Genetic Algorithm
**Current stable version**: 0.0.0

Algoritmo Genético utilizado para busca/otimização.

## Clonando o repositório
Para fazer o download do **Genetic Algorithm**, crie uma pasta no diretório de sua preferência e execute os comandos abaixo para clonar o projeto.

```
git clone 
```

## Instalação
Crie uma venv e em seguida, execute o comando abaixo para instalação

```
virtualenv --python python3 venv
source venv/bin/activate

pip install .
```

### Executar os testes
```console
pytest --cov=genetic_algorithm tests/
```

## Utilizando Allocation **C**ommand **Li**ne **I**nterface:
Assim que o **Genetic Algorithm** foi instalado, podemos usar o aplicativo ** ga-cli ** para execução do algoritmo, algo assim:

### Parâmetros
```
$ ga-cli -h

usage: allocation-cli [-h] [--output-dir OUTPUT_DIR] [--nr-max-gen NR_MAX_GEN]
                      [--population-size POPULATION_SIZE] [--elitism ELITISM]
                      [--tournament-size TOURNAMENT_SIZE]
                      [--crossover-rate CROSSOVER_RATE]
                      [--mutation-rate MUTATION_RATE]
                      [--random-immigrants RANDOM_IMMIGRANTS]
                      [--immigration-rate IMMIGRATION_RATE] [--seed SEED]
                      [--pool-processes POOL_PROCESSES] [--patience PATIENCE]

Genetic Algorithm CLI

optional arguments:
  -h, --help            show this help message and exit
 --task TASK           Task to be run. Can be DiscoverPhraseGA, SumVectorGA
                        or OptimizeRoute
  --output-dir OUTPUT_DIR
                        path to output dir. Default: .
  --nr-max-gen NR_MAX_GEN
                        Maximum number of generations
  --population-size POPULATION_SIZE
                        Population size.
  --chromosome-length CHROMOSSOME_LENGHT
                        Chromosome length.
  --elitism ELITISM     Number of individuals to be selected by elitism.
  --tournament-size TOURNAMENT_SIZE
                        Number of individuals selected by selection per
                        tournament.
  --crossover-rate CROSSOVER_RATE
                        Crossover rate.
  --mutation-rate MUTATION_RATE
                        AVG of one mutation per individual.
  --random-immigrants RANDOM_IMMIGRANTS
                        If true, each generation immigration_rate percent of
                        the population is replaced by new random individuals.
                        Elitist individuals can't be replaced.
  --immigration-rate IMMIGRATION_RATE
                        Percentage of population to be randomly replaced by
                        new solutions.
  --seed SEED           Seed to be used by numpy and random.
  --pool-processes POOL_PROCESSES
                        Number of pool processes. If None, use max number of
                        cores available on your system.
  --patience PATIENCE   Number of generation with no improvement after which
                        search will be stopped.
```

### Iniciar a otimização
```console
ga-cli
```

#### Tasks
ga-cli --task SumVectorGA --objective minimization --chromosome-length 1000 --population-size 100 --nr-max-gen 250

ga-cli --task DiscoverPhraseGA --population-size 200 --nr-max-gen 1500 --patience 0
95 letras ^ 74 caracteres = 2.246709e+146 soluções

ga-cli --task OptimizeRoute --population-size 200 --nr-max-gen 1500 --patience 0

### Saída do Algoritmo


###  Funcionamento do AG
Para entender melhor o funcionamento do algoritmo genético [genetic_algorithm.md](/docs/genetic_algorithm.md).
