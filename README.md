# process-escalonator

![Supported Python Version](https://img.shields.io/pypi/pyversions/django.svg) ![Supported Platforms](https://img.shields.io/badge/platform-win--64%20%7C%20linux--64-red.svg) ![License](https://img.shields.io/cocoapods/l/afn.svg) ![](https://img.shields.io/badge/build-passing-brightgreen.svg) ![GitHub release](https://img.shields.io/github/release/gustavooquinteiro/process-escalonator.svg?color=yellow) 

Simulador de execução de processos de um sistema operacional em Python desenvolvido como parte da avaliação da matéria MATA58 - Sistemas Operacionais, do Departamento de Ciência da Computação da Universidade Federal da Bahia, ministrada por Maycon Leone Maciel Peixoto.

***
## Sumário

1. [Situação](#Situação)  
2. [Funcionamento](#Funcionamento)  
. [Back-end](#Back-end)  
. [Front-end](#Front-end)
3. [Requisitos do trabalho](#Requisitos)
4. [Entrada](#Entrada)
5. [Saída](#Saida)
6. [Convenções adotadas](#Convenções)
7. [Adicionais](#Adicionais)
8. [Uso do programa](#Uso)  
. [Requisitos para execução do programa](#Requisitos)  
. [Instalação dos requisitos](#Start)  
. [Execução do programa](#Execução)
9. [Desenvolvimento](#Autores)

***

<div id='Situação'/>  

## :clipboard: Situação  

Considere um sistema operacional que implementa o escalonamento de processos. O funcionamento esperado é que esse ambiente tenha ``` N ``` (número previamente informado pelo usuário) processos que podem chegar em tempos distintos para execução. Para cada processo, deve ser informado:  

- Tempo de chegada  
- Tempo de execução  
- Deadline  

Para o sistema como um todo deve se informar o tempo do **quantum do sistema** e o **tempo da sobrecarga**, na troca de processos, do sistema.

<div id='Funcionamento'/>

## :computer: Funcionamento

Esse sistema deve ter:

<div id='Back-end'/>

### Back-end

> A implementação de todos os algoritmos, tanto de escalonamento quanto de paginação, citados abaixo é obrigatória para avaliação do trabalho

#### [Algoritmos de escalonamento](https://pt.wikipedia.org/wiki/Escalonamento_de_processos)

-   [FCFS (First Come First Served)](https://pt.wikipedia.org/wiki/FIFO)
    -  Um algoritmo de escalonamento para estruturas de dados do tipo fila.
-   [SJF (Shortest Job First)](https://pt.wikipedia.org/wiki/Shortest_job_first)
    -  Um algoritmo de escalonamento que ordena os processos por tempo de execução de forma crescente.
-   [Round Robin](https://pt.wikipedia.org/wiki/Round-robin)
    -  O nome do algoritmo vem do princípio onde cada pessoa pega um compartilhamento de algo igual por vez.

-   [EDF (Earliest Deadline First)](https://pt.wikipedia.org/wiki/Sistema_operacional_de_tempo-real#Escalonamento)
    - Um algoritmo que escolhe na fila de prontos o processo que tenha o prazo de vencimento mais curto

#### [Algoritmos de substituição de páginas](http://escalonamentoprocessos.blogspot.com/2010/12/memoria-virtual-paginacao-por-demanda-e.html)

-   FIFO (First In First Out)
    - Algoritmo baseado na idade das páginas na memória, ou seja, páginas mais antigas serão removidas primeiro.
-   LRU (Least Recently Used)
    -  Algoritmo que escolhe preferencialmente páginas antigas e menos usadas para remoção.

Todos os algoritmos acima citados, basicamente funções de ordenação com variados critérios, foram implementados em Python utilizando suas funções _built-in_ por praticidade e facilidade.

<div id='Front-end'/>

### Front-end

Esse sistema deve implementar interface gráfica, onde deve-se criar:

-   [Gráfico de Gantt](https://pt.wikipedia.org/wiki/Diagrama_de_Gantt) para mostrar as execuções dos processos

-   **Visualização da CPU e da RAM**

-   Deve-se criar o gráfico de uso da RAM e do Disco, mostrando as página presentes em tempo real.  

-   Colocar _delay_ para verificar a execução  

Para tal utilizamos a biblioteca [PyQt5](https://pypi.org/project/PyQt5/) que nos fornece vários elementos para que compuséssemos a interface e os gráficos pedidos.

<div id='Requisitos'/>

## :ballot_box_with_check: Requisitos do trabalho

-   Cada página tem **4 K** de tamanho.

-   A RAM tem **200 K** de memória.

-   Crie a abstração de **Disco** para utilização da memória virtual.  

-   Caso ocorra falta de página (_page fault_), utilize _N_ unidades de tempo para o uso do Disco.  

-   O grupo está livre para a criação de qualquer abstração extra que se mostrar necessária.  

-   **Os processos só executam se todas as suas páginas estiverem na RAM.**

<div id='Entrada'/>

## :inbox_tray: Entrada

O usuário deve entrar com um inteiro `Q`, representando o quantum do sistema, e um inteiro ``` S ```, representando a sobrecarga do sistema. Além disso deve ser fornecido `N`, representando o número de processos, inteiros:  

-   `C`, representando o tempo de criação do processo, onde `C >= 0`;   

-   `E`, representando o tempo de execução do processo, onde `E > 0`;  

-   `D`, representando o deadline do processo, onde `D >= E`;  

-   `B`, representando o número de páginas que o processo precisa, onde `0 < B <= 10 `, e;  

-   `P`, representando a prioridade do processo, onde `P >= 0`

Deve ser escolhido um dos algoritmos de escalonamento de processo ofertados

- ``` FCFS (First Come First Served) ```;  
- ``` SJF (Shortest Job First) ```;
- ``` RR (Round-Robin)```;
- ``` EDF (Earliest Deadline First) ```;
- ``` SPN (Shortest Process Next) ```;
- ``` LOT (Loteria) ```;
- ``` PRIO (Prioridade) ```;

 > Os três últimos algoritmos foram adicionalmente implementados. Mais informações [aqui](#Adicionais)

Deve ser escolhido um dos algoritmos de paginação:

- ``` FIFO (First-In First-Out) ```;  
- ``` LRU (Least Recently Used) ```

<div id='Saída'/>

## :outbox_tray: Saída

A resposta deve ser dada em função do **turn-around médio** (tempo de espera + tempo de execução), o **gráfico de Gantt correspondente** às execuções dos processos, e o **estado da RAM**, durante a execução dos processos, de acordo o algoritmo de escalonamento e o algoritmo de paginação escolhidos

<div id='Convenções'/>

## :pushpin: Convenções adotadas

-   Utilizamos a notação ``` FCFS (First Come, First Served)```, no código, para nomear o algoritmo de escalonamento de processos e desambiguar da notação ``` FIFO  (First In, First Out) ```, utilizada para nomear o algoritmo de paginação, pois embora os dois algoritmos tenham teoricamente o mesmo funcionamento o escopo deles é diferente.  

-   Utilizamos uma **memória virtual** com o dobro de capacidade da memória RAM, ou seja,  **400 K**  

- A **capacidade do disco** é o somatório de `B`<sub>i</sub> para i variando de 1 a ``N``, ou seja, assumimos que o disco comporta todas as páginas de todos os processos criados.

-   Em caso de _page fault_ utilizamos ``` teto ((B - A) / W) ``` **_tiques_ de clock** para uso do disco, onde:

    -   `A` é o **número de páginas, desse processo, já alocadas na RAM** e;  

    -   `W ` é a **quantidade de páginas, escritas na RAM, por segundo**, em nossa implementação, escolhemos o valor de ```2 páginas por segundo```  

<div id='Adicionais'/>

## :heavy_plus_sign: Adicionais

Para acrescentar tanto em conhecimento sobre escalonamento de processos quanto em nota, decidimos implementar os seguintes algoritmos:

- Escalonamento por prioridades
   - Algoritmo que ordena a fila de prontos pela prioridade do processo, de forma decrescente
   > A implementação utilizada, foi a qual a CPU **diminui a prioridade do processo à sua metade**, após executá-lo: `P = P / 2`. A fila de prontos é então reordenada pelo critério do algoritmo

- SPN (Shortest Process Next)
   - Algoritmo similar ao [SJF](https://pt.wikipedia.org/wiki/Shortest_job_first) porém preemptivo

- Escalonamento por loteria
   - Algoritmo preemptivo onde a escolha de processos é aleatória

<div id='Uso'/>

## :gear: Uso do programa

É suposto que esse trabalho funcione em qualquer plataforma que tenha Python, porém a  [release](https://github.com/gustavooquinteiro/process-escalonator/releases/) mais recente só funciona em plataforma Windows, pois o requisito: `pyqt5-tools` somente pode ser instalado pelo `pip` da plataforma, mas que para o escopo do trabalho é mais que o suficiente.

Essa branch visa resolver esse problema.   
E ao remover o requisito `pyqt5-tools`, o programa funciona no Linux. 
> :exclamation: Testes ainda são requeridos na plataforma Windows

<div id='Requisitos'/>

### Requisitos

- Ter o [Python versão 3.x](https://www.python.org/downloads/) instalado na sua máquina
- Ter o `pip` instalado   
- Instalar as bibliotecas listadas em [requirements.txt](requirements.txt)  

<div id='Start'/>

### Instalação dos requisitos

- Abra um Terminal ou Prompt de Comando dentro da pasta ``` process-escalonator/ ```:  

> :warning: É recomendado que se instale as bibliotecas em um ambiente virtual, evitando conflitos de versões das bibliotecas instaladas localmente no seu computador. Para tal siga as instruções a seguir, de acordo sua plataforma.

- UNIX:  
```sh
  python3 -m venv env
  source env/bin/activate  
  pip3 install -r requirements.txt
```

- Windows:  
```sh
  python -m venv env
  env\Scripts\activate
  pip install -r requirements.txt
```

> Caso não queira criar um ambiente virtual, somente dê o comando ``` pip install -r requirements.txt ```, independentemente da sua plataforma

<div id='Execução'/>

### Execução do programa

Para executar basta dar o comando:

```sh
  python InterFace.py
```

Em plataformas UNIX é bom especificar a versão do Python, já que em algumas o Python 2.x ainda vem como padrão, com o comando:

```sh
  python3 InterFace.py
```

Em plataformas Windows, também é válido dar duplo-clique no arquivo ``` InterFace.py ```

<div id='Autores'/>

## :octocat: Desenvolvimento

Maiores detalhes e/ou dúvidas sobre o desenvolvimento desse trabalho, considere ver o [log](https://github.com/gustavooquinteiro/process-escalonator/commits/master) desse repositório, ou entrar em contato com os autores abaixo listados:

- [Giuseppe Mareschi](https://github.com/GiuseppeXD)
- [Gustavo Quinteiro](https://github.com/gustavooquinteiro)
- [Victor Pinheiro](https://github.com/vpinheiro38)
