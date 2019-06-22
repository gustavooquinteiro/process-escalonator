import random


class Escalonator():
    """ Classe responsável pela  gerência da fila de prontos """

    NON_PREEMPTIVE_ALGORITHMS = ["FCFS", "SJF"]
    PREEMPTIVE_ALGORITHMS = ["RR", "EDF", "SPN", "PRIO", "LOT", "MLF"]

    def __init__(self, typeof="FCFS", override=.015, cpu=None):
        """ Método de inicialização de um escalonador.
        Args:
            typeof (str): tipo de algoritmo de escalonamento que será utilizado
            override (int): tempo necessário para a troca de contexto de processos
            cpu (CPU): objeto da cpu responsável pela execução dos processos

        """

        self.ready_queue = []
        self.not_arrived = []
        self.algorithm = typeof
        self.override = override
        self.cpu = cpu

    def insert_process(self, process):
        """ Insere processos em sua respectiva fila
        Args:
            process (Process): processo que será inserido em uma fila

        """
        if process.is_arrived(self.cpu.clock):
            self.ready_queue.append(process)
        else:
            self.not_arrived.append(process)

    def queue(self):
        """ Ordena a fila de prontos de acordo com o algoritmo escolhido """
        if self.algorithm == "RR" or self.algorithm == "FCFS":
            self.ready_queue.sort(key=lambda process: process.start)
        elif self.algorithm == "EDF":
            self.ready_queue.sort(key=lambda process:
                                      (process.start, process.deadline))
        elif self.algorithm == "SJF" or self.algorithm == "SPN":
            self.ready_queue.sort(key=lambda process:
                                      (process.start, process.execution_time))
        elif self.algorithm == "PRIO":
            self.ready_queue.sort(key=lambda process:
                                      (process.start, process.priority),
                                      reverse=True)
        elif self.algorithm == "LOT":
            random.shuffle(self.ready_queue)
        elif self.algorithm == "MLF":
            self.ready_queue.sort(key=lambda process:
                                      (process.start, process.laxity))
        # Os processos que não chegaram são ordenados por seu tempo de chegada
        self.not_arrived.sort(key=lambda process: process.start)

    def update_attributes(self):
        """ Atualiza o deadline e o laxity de todos os processos na fila de prontos """
        for process in self.ready_queue:
            process.deadline = process.deadline - self.cpu.clock + process.start
            process.laxity = process.deadline - self.cpu.clock - process.execution_time

    def real_time_over(self, process):
        """ Verifica se um processo ultrapassou seu limite de execução.
        Somente válido para algoritmos de escalonamento de tempo real
        Args:
            process (Process): processo que será averiguado
        """
        if self.algorithm == "EDF" and process.is_out_deadline():
            return True
        if self.algorithm == "MLF" and process.is_out_laxity():
            return True
        return False

    def next_process(self):
        """ Adiciona processos, que chegaram, à fila de prontos e reordena-a, se necessário  """

        arrived = list(filter(
            lambda process: process.is_arrived(self.cpu.clock),
            self.not_arrived))

        for process in arrived:
            self.ready_queue.append(process)
            self.not_arrived.remove(process)

        if len(self.ready_queue) > 1:
            if self.algorithm == "SJF" or self.algorithm == "SPN":
                self.ready_queue.sort(key=lambda process: process.execution_time)
            elif self.algorithm == "EDF":
                self.ready_queue.sort(key=lambda process: process.deadline)
            elif self.algorithm == "PRIO":
                self.ready_queue.sort(key=lambda process:
                                          process.priority,
                                          reverse=True)
            elif self.algorithm == "LOT":
                random.shuffle(self.ready_queue)
            elif self.algorithm == "MLF":
                self.ready_queue.sort(key=lambda process: process.laxity)
