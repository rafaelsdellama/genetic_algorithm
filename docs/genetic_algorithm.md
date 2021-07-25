## Algoritmo Genético 

Os Algoritmos Genéticos (AGs) são métodos adaptativos inspirados nos processos genéticos de organismos biológicos e na teoria da evolução por selelção natural.

No AG, um conjunto de invivíduos (ou cromossomos) representando soluções do problema é sujeito a operadores de seleção e transformação inspirados em mecanismos encontrados na evolução por seleção natural. A solução *x<sub>i</sub>* (também chamada de indivíduo ou cromossomo), para *i*=1,...,*N*, sendo *N* o tamanho da população, é avaliado através de uma função de custo, ou *fitness*, *f(x<sub>i</sub>)*

Os operadores de transformação mais utilizados são o *crossover* e a mutação. No primeiro, dois indivíduos da população corrente escolhidos por meio do operador de seleção têm algumas das variáveis trocadas entre si. Um exemplo de operador de seleção é o método do torneio, no qual *M* indivíduos são escolhidos aleatóriamente e vence o indivíduo com maior *fitness*.

A probabilidade de se aplicar *crossover* é definida por uma taxa *p<sub>c</sub>*, chamada de taxa de *crossover*. Na mutação, indivíduos têm alguns de seus elementos alterados. O número de variváveis de decisão alteradas por muetação é definido por uma taxa *p<sub>m</sub>*, chamada de taxa de mutação.

o AG deste repositório inicia a sua execução através do ```run()```.
O tamanho dos cromossomos é definido pelo número de par (grupo econômico/fornecedor) com titulos disponíveis para anteciar. Cada posição dessa solução (cromossomo) irá receber um número de 0 até o nro de fundos disponíveis.
O valor 0 corresponde a "nenhum investidor" e os demais correspondem a um fundo especifico.


O funcionamento do AG é apresentado na Figura abaixo:

![ga](/docs/ga.png)

**1 - Gerar população inicial:** o método responsável por gerar a população inicial é o ```_generate_initial_population()```,
q irá gerar uma população do tamanho *N*, onde *N* é definido pelo parâmetro ```population_size```. Para gerar a população inicial, é utilizado o método ```_generating_indiv()```, responsável por gerar um indivíduo com variáveis aleatórias.

**2- Avaliar a população:** o método próprio método responsável por gerar a população inicial ```_generate_initial_population()``` já calcula o *fitness* de cada indivíduo através do método ```_calculate_fitness()```. Nesta etapa é utilizado **multiprocessing** para acelerar a execução do algoritmo. O número de processos é definido pelo parâmetro ```pool_processes```.

Na sequencia os métodos ```population_statistic()``` ```_print_population_info() ``` são responsáveis por calcular e mostrar as estatisticas da população, respectivamente.

Nesta etapa a população inicial já foi gerada e avaliada. A Figura abaixo ilustra uma população:

![pop](/docs/pop.png)


**3- Gerar nova população:** O método ```_generating_new_population()``` é responsável pela geração de uma nova população. Ele utiliza a população atual e por meio dos operadores de transformação gera uma nova população.

**3.1- Seleção:** O método de seleção utilizado é o método do torneio. O método consiste em selecionar *N* individuos, onde *N* é definido pelo parâmetro ```tournament_size```, e o indivíduo com maior *fitness* vence a batalha e é selecionado.
Sempre são selecionados 2 individuos da população atual (chamados de individuos pais) para gerar 2 novos individuos da nova geração (individuos filhos) através dos operadores de transformação.
Os *N* melhores individuos de uma geração são passados para à proxima geração, onde o valor de *N* é definido pelo parâmetro ```elitism```.

**3.2- *Crossover*:** O *crossover* é representado pelo método ```_crossover()```, e a taxa de crossover é definida pelo parâmetro ```crossover_rate```. Neste método são gerados 2 pontos de cortes, e se os pontos gerados sejam diferentes é executado o *crossover* de 2 ponto e caso contrário é executado o *crossover* de 1 ponto. O *crossover* de dois pontos é apresentado na Figura à seguir: 

![crossover](/docs/crossover.png)

**3.3- Mutação:** A mutação é representada pelo método ```__randomly_mutate()```, e a taxa de mutação é definida pelo parâmetro ```mutation_rate```. Um exemplo de mutação é apresentado na Figura à seguir:

![mutation](/docs/mutation.png)

**3.4- Imigrantes aleatórios:** A técnica de Imigrantes aleatórios consiste em substituir uma parcela da população por novos indivíduos aleatórios para auxiliar na manutenção da diversidade de soluções e evitar ótimos locais. O método responsável é executado quando o parâmetro ```random_immigrants``` está definido como **True**, substituindo o percentual da população definido pelo parâmetro ```immigration_rate```. 


Na sequencia os métodos ```population_statistic()``` ```_print_population_info() ``` são responsáveis por calcular e mostrar as estatisticas da população, respectivamente.

**4- Critério de parada:** Responvável por verificar se os critérios de parada foram satisfeitos e finalizar a otimização. Os critérios de parada são 3:

**4.1 - Número de gerações**: Quando o número de gerações atingir o número máximo de gerações definido pelo parâmetro ```nr_max_gen```, a otimização é finalizada.

**4.2 - Paciência**: Se a paciência for definida pelo parâmetro ```patience```, no final de cada geração é verificado se houve uma melhora no *fitness* do melhor indivíduo. Se houver uma melhora um contador de paciencia é resetado, caso contrário é incrementado em 1. Quando o contador atingir o valor de paciencia, a otimização é finalizada.

**4.3 - *Fitness* máximo**: Obter um *Fitness* = 1
