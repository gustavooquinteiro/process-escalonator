import time
import random
import process


class Escalonator():
    """ Classe responsável pela  gerência da fila de prontos """

    NON_PREEMPTIVE_ALGORITHMS = ["FCFS", "SJF"]
    PREEMPTIVE_ALGORITHMS = ["RR", "EDF", "SPN", "PRIO", "LOT"]

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
        
    def insertProcess(self, process):
        if process.isArrived(self.cpu.clock):
            self.ready_queue.append(process)
        else:
            self.not_arrived.append(process)
            
    def queue(self):
        """ Ordena a fila de prontos de acordo com o algoritmo escolhido """
        if self.algorithm == "RR" or self.algorithm == "FCFS":
            self.ready_queue.sort(key=lambda x: x.start)
            self.not_arrived.sort(key=lambda x: x.start)
        elif self.algorithm == "EDF":
            self.ready_queue.sort(key=lambda x: (x.start, x.deadline))
            self.not_arrived.sort(key=lambda x: (x.start, x.deadline))
        elif self.algorithm == "SJF" or self.algorithm == "SPN":
            self.ready_queue.sort(key=lambda x: (x.start, x.execution_time))
            self.not_arrived.sort(key=lambda x: (x.start, x.execution_time))
        elif self.algorithm == "PRIO":
            self.ready_queue.sort(key=lambda x: (x.start, x.priority), reverse=True)
            self.not_arrived.sort(key=lambda x: (x.start, x.priority), reverse=True)
        elif self.algorithm == "LOT":
            random.shuffle(self.ready_queue)
            self.not_arrived.sort(key=lambda x: x.start)

    def updateDeadline(self):
        """ Atualiza o deadline de todos os processos na fila de prontos """
        for process in self.ready_queue:
            process.deadline = process.deadline - self.cpu.clock + process.start

    def manageQueue(self, process):
        """ Gerencia a fila de prontos de acordo o estado do processo no inicio da fila
            Args:
                process (Process): processo a ser removido da fila
        """

        if process.finished(self.cpu.mmu):
            self.ready_queue.remove(process)
            self.cpu.concluded_process_time.append(self.cpu.clock - process.start)
            self.nextProcess()
            return True

        if self.algorithm in self.PREEMPTIVE_ALGORITHMS:
            self.nextProcess()
            #time.sleep(self.override)
            self.cpu.clock += self.override
            self.updateDeadline()
        return False

    def forceRemove(self, process):
        self.ready_queue.remove(process)
        self.nextProcess()

    def nextProcess(self):
        """ Adiciona processos, que chegaram, à fila de prontos e reordena-a, se necessário  """

        arrived = list(filter(
            lambda x: x.isArrived(self.cpu.clock),
            self.not_arrived))

        for process in arrived:
            self.ready_queue.append(process)
            self.not_arrived.remove(process)

        if len(self.ready_queue) > 1:
            if self.algorithm == "FCFS":
                self.ready_queue.sort(key=lambda x: x.start)
            elif self.algorithm == "SJF" or self.algorithm == "SPN":
                self.ready_queue.sort(key=lambda x: x.execution_time)
            elif self.algorithm == "EDF":
                self.ready_queue.sort(key=lambda x: x.deadline)
            elif self.algorithm == "PRIO":
                self.ready_queue.sort(key=lambda x: x.priority, reverse=True)
            elif self.algorithm == "LOT":
                random.shuffle(self.ready_queue)
