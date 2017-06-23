# Exact Cover

Este projeto contém dois arquivos python referentes aos modelos descritos no artigo. Os resultados
experimentais foram obtidos com estes programas. O tempo de execução foi calculado com base
no modo silencioso. Ou seja, somento o número de respostas e subproblemas foi impresso na tela.

## Modelo Dancing Links:

Para calcular o número de rainhas com o modelo Backtracking de Dijkstra, execute:

```
$ python backtracking_nqueens.py [-n] <num_queens>
```
A opção -n ativa o modo silencioso, onde as respostas não serão impressas, somente o número de resultados.

## Modelo Dancing Links:

Para calcular o número de rainahs com o modelo DLX, execute:

```
$ python dlx_nqueens.py <num_queens> [s_heuristic = True]
```

Por padrão o programa utiliza a heurística S e 8 rainhas. Este programa só imprime o número de resultados
e não tem opção para imprimir as respostas. Uma pequena alteração poderia ser feita para imprimir as respostas,
mas isso não era necessário para calcular a velocidade do modelo.
