import time
import process

class Escalonator():
    """ Classe responsável pela  gerência da fila de prontos """
    
    NON_PREEMPTIVE_ALGORITHMS = ["FCFS", "SJF"]
    PREEMPTIVE_ALGORITHMS = ["RR", "EDF"]
    
    def __init__(self, typeof="FCFS", override = .015, cpu=None):
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
        
    def appendProcess(self, process):
        if process.isArrived(self.cpu.cpu_execution):
            self.ready_queue.append(process)
        else:
            self.not_arrived.append(process)

    def sortQueue(self):
        """ Ordena a fila de prontos de acordo com o algoritmo escolhido """
        
        if self.algorithm == "RR" or self.algorithm == "FCFS":
            self.ready_queue.sort(key=lambda x: x.start)
            self.not_arrived.sort(key=lambda x: x.start)
        elif self.algorithm == "EDF":
            self.ready_queue.sort(key=lambda x: (x.start, x.deadline))
            self.not_arrived.sort(key=lambda x: (x.start, x.deadline))
        elif self.algorithm == "SJF":
            self.ready_queue.sort(key=lambda x: (x.start, x.execution_time))
            self.not_arrived.sort(key=lambda x: (x.start, x.execution_time))
                
    def updateDeadline(self):
        for process in self.ready_queue:
            process.deadline = process.deadline - self.cpu.cpu_execution + process.start
            if self.algorithm == "EDF" and process.isOutDeadline():
                print("\nProcesso {} está fora do prazo" .format(process.id))
            
    def manageQueue(self, process):
        """ Gerencia a fila de prontos de acordo o estado do processo no inicio da fila
            Args:
                process (Process): processo a ser removido da fila
        """
        if process.isFinished():            
            self.ready_queue.remove(process)            
            self.nextProcess()
            
        elif self.algorithm in self.PREEMPTIVE_ALGORITHMS:
            self.nextProcess()
            time.sleep(self.override)
            self.cpu.cpu_execution += self.override            
            self.updateDeadline()   
            

    def nextProcess(self):
        """ Adiciona processos, que chegaram, à fila de prontos e reordena-a, se necessário  """

        ready_queue_empty = True if not self.ready_queue else False
        
        arrived = list(filter(
            lambda x: x.isArrived(self.cpu.cpu_execution),
            self.not_arrived))

        for process in arrived:
            self.ready_queue.append(process)
            self.not_arrived.remove(process)
        
        if self.algorithm == "SJF":
            self.ready_queue.sort(key=lambda x: x.execution_time)
            return 
        elif self.algorithm == "EDF":
            self.ready_queue.sort(key=lambda x: x.deadline)
            return
        
        if not ready_queue_empty:
            self.ready_queue = self.ready_queue[1:]+[self.ready_queue[0]]        
        elif self.not_arrived and ready_queue_empty:
            self.ready_queue.append(self.not_arrived.pop(0))
            
