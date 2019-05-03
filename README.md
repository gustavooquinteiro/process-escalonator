# process-escalonator
Escalonador de processos em Python desenvolvido como parte da avaliação da matéria MATA58 - Sistemas Operacionais, do Departamento de Ciência da Computação da Universidade Federal da Bahia, ministrada por Maycon Leone Maciel Peixoto 

## Autores
* [Giuseppe Mareschi](https://github.com/GiuseppeXD)
* [Gustavo Quinteiro](https://github.com/gustavooquinteiro)
* [Victor Pinheiro](https://github.com/vpinheiro38)

## Situação
Considere um sistema operacional que implementa o escalonamento de processos. O funcionamento esperado é que esse ambiente tenha ``` N ``` (número previamente informado pelo usuário) processos que podem chegar em
tempos distintos para execução. Para cada processo, deve ser informado
* Tempo de chegada
* Tempo de execução
* Deadline

Para o sistema como um todo deve se informar o tempo do **quantum do sistema** e o **tempo da sobrecarga**, na troca de processos, do sistema.

## Funcionamento  
Esse sistema deve implementar os algoritmos de escalonamento:
* [FIFO](https://pt.wikipedia.org/wiki/FIFO)
  + Um algoritmo de escalonamento para estruturas de dados do tipo fila.
* [SJF](https://pt.wikipedia.org/wiki/Shortest_job_first)
  + Um algoritmo de escalonamento que ordena os processos por tempo de execução de forma crescente.
* [Round Robin](https://pt.wikipedia.org/wiki/Round-robin)
  + O nome do algoritmo vem do princípio round-robin conhecido de outros campos, onde cada pessoa pega um compartilhamento de algo igual por vez.
* [EDF](https://pt.wikipedia.org/wiki/Sistema_operacional_de_tempo-real#Escalonamento)
  + Um algoritmo que escolhe na fila de prontos o processo que tenha o prazo de vencimento mais curto

Esse sistema deve implementar os algoritmos de substituição de páginas:
* FIFO
  + Algoritmo baseado na idade das páginas na memória, ou seja, páginas mais antigas podem ser removidas.
* Menos Recentemente Utilizado
  + Algoritmo que escolhe preferencialmente páginas antigas e menos usadas para remoção.

## Requisitos

* Cada processo deve ter até 10 páginas (entrada do usuário). Cada página tem 4K de
tamanho. A RAM tem 200 K de memória.
* Crie a abstração de DISCO para utilização da memória virtual. 
  + Caso ocorra falta de página, utilize N unidades de tempo para o uso do Disco.
* O grupo está livre para a criação de qualquer abstração extra que se mostrar
necessária.
* Os processos só executam se todas as suas páginas estiverem na RAM.
* Deve-se criar:
  + [Gráfico de Gantt](https://pt.wikipedia.org/wiki/Diagrama_de_Gantt) para mostrar as execuções dos processos,
  + Visualização da CPU e da RAM
* Deve-se criar o gráfico de uso da RAM e do Disco, mostrando as página presentes em
tempo real.
* A resposta deve ser dada em função do turn-around médio (tempo de espera + tempo
de execução)
* Colocar delay para verificar a execução

## Recomendações
Usar Python 3.7.2 ou superior 

## Como usar 
Em plataformas UNIX:
```py
  python3 main.py
```

Em plataformas Windows:
```py
  python main.py
```
