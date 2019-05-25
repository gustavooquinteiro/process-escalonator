import time
import process
import threading

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
        elif self.algorithm == "SJF":
            self.ready_queue.sort(key=lambda x: (x.start, x.execution_time))
            self.not_arrived.sort(key=lambda x: (x.start, x.execution_time))
                
    def updateDeadline(self):
        for process in self.ready_queue:
            process.deadline = process.deadline - self.cpu.clock + process.start
            
    def remove(self, process):
        """ Remove o processo da fila de prontos, se ele já estiver finalizado, e coloca o próximo da fila na frente.
            Args:
                process (Process): processo a ser removido da fila
        """
        if process.finished(self.cpu.mmu):            
            self.ready_queue.remove(process)
            self.cpu.concluded_process_time.append(self.cpu.clock - process.start)
            self.nextProcess()

            return True
            
        elif self.cpu.preemptiveness:
            self.nextProcess()
            time.sleep(self.override)
            self.cpu.clock += self.override
            self.updateDeadline()
            
            if self.algorithm == "EDF" and process.isOutDeadline():
                print("\nProcesso {} está fora do prazo" .format(process))

        return False

    def forceRemove(self, process):
        self.ready_queue.remove(process)
        self.nextProcess()

    def nextProcess(self):
        """ Atualiza a fila de prontos colocando o primeiro da fila no final da fila ou reoordenando-a de acordo seus algoritmos  """
        
        ready_queue_empty = True if not self.ready_queue else False
        not_keep = []
        for process in self.not_arrived:
            if process.isArrived(self.cpu.clock):
                self.ready_queue.append(process)
                not_keep.append(process)
                    
        for process in not_keep:
            self.not_arrived.remove(process)
            
        if len(self.ready_queue) > 1:
        
            if self.algorithm == "FCFS":
                self.ready_queue.sort(key=lambda x: x.start)
                return
            
            if self.algorithm == "SJF":
                self.ready_queue.sort(key=lambda x: x.execution_time)
                return 
            if self.algorithm == "EDF":
                self.ready_queue.sort(key=lambda x: x.deadline)
                return
        
            # [2 3]
            # [2 3 1]
