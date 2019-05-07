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
        self.algorithm = typeof
        self.override = override         
        self.cpu = cpu

        
    def queue(self):
        """ Ordena a fila de prontos de acordo com o algoritmo escolhido e inicia a execução na CPU """
        if self.algorithm in self.PREEMPTIVE_ALGORITHMS:
            self.aux_queue = []
            #for index, process in enumerate(self.ready_queue):
                #if not process.isArrived(self.cpu.cpu_execution):
                    #self.aux_queue.append(self.ready_queue.pop(index))
            #print("lista auxiliar")
            #print("tmepo da cpu {}".format(self.cpu.cpu_execution))
            #print(*self.aux_queue, sep='\n')
            if self.algorithm == "RR":
                self.ready_queue.sort(key=lambda x: x.start)
                self.aux_queue.sort(key=lambda x: x.start)
            elif self.algorithm == "EDF":
                self.ready_queue.sort(key=lambda x: (x.start, x.deadline))
                self.aux_queue.sort(key=lambda x: (x.start, x.deadline))
        else:
            if self.algorithm == "FCFS":
                self.ready_queue.sort(key=lambda x: x.start)
            elif self.algorithm == "SJF":
                self.ready_queue.sort(key=lambda x: (x.start, x.execution_time))
        
            

    def updateDeadline(self):
        for process in self.ready_queue:     
            if process.isArrived(self.cpu.cpu_execution):
                process.deadline -= self.cpu.cpu_execution + process.start
            print ("Processo {} agr com deadline de {}" .format(process.id, process.deadline))        
        
    def remove(self, process):
        """ Remove o processo da fila de prontos, se ele já estiver finalizado, e coloca o próximo da fila na frente.
            Args:
                process (Process): processo a ser removido da fila
        """
        if process.finished():
            self.ready_queue.remove(process)
            if any(process.start == self.cpu.cpu_execution for process in self.ready_queue): 
                if self.algorithm == "SJF":
                    self.ready_queue.sort(key=lambda x: x.execution_time)
            self.cpu.concluded_process_time.append(self.cpu.cpu_execution - process.start)
            print(*self.cpu.concluded_process_time)
        elif self.cpu.preemptiveness:
            self.updateDeadline()
            self.nextProcess()
            time.sleep(self.override)
            self.cpu.cpu_execution += self.override               
            if process.outOfTime(self.cpu.cpu_execution) and self.algorithm == "EDF":
                print("Processo {} está fora do prazo" .format(process.id))

    def nextProcess(self):
        """ Atualiza a fila de prontos colocando o primeiro da fila no final da fila ou reoordenando-a caso seja o algoritmo de escalonamento EDF  """
        if self.algorithm == "EDF":
            actual_process = self.ready_queue[0]
            self.ready_queue = self.ready_queue[1:]+[self.ready_queue[0]]
            new_process = self.ready_queue[0]
            index = self.ready_queue.index(actual_process)
            while not new_process.isArrived(self.cpu.cpu_execution):
                self.ready_queue = self.ready_queue[1:]+[self.ready_queue[0]]    
                new_process = self.ready_queue[0]
            for i in range(1, len(self.ready_queue)):
                process = self.ready_queue[i]
                if not process.isArrived(self.cpu.cpu_execution):
                    self.ready_queue[index], self.ready_queue[i] = self.ready_queue[i], self.ready_queue[index]
        elif self.algorithm == "RR":
            #if self.aux_queue and self.aux_queue[0].isArrived(self.cpu.cpu_execution):
                #self.ready_queue.append(self.aux_queue.pop(0))
            #self.ready_queue = self.ready_queue[1:]+[self.ready_queue[0]]
            actual_process = self.ready_queue[0]
            self.ready_queue = self.ready_queue[1:]+[self.ready_queue[0]]
            new_process = self.ready_queue[0]
            index = self.ready_queue.index(actual_process)
            while not new_process.isArrived(self.cpu.cpu_execution):
                self.ready_queue = self.ready_queue[1:]+[self.ready_queue[0]]    
                new_process = self.ready_queue[0]
            for i in range(1, len(self.ready_queue)):
                process = self.ready_queue[i]
                if not process.isArrived(self.cpu.cpu_execution):
                    self.ready_queue[index], self.ready_queue[i] = self.ready_queue[i], self.ready_queue[index]
        elif len(self.ready_queue) > 1:
            self.ready_queue = self.ready_queue[1:]+[self.ready_queue[0]]        
            
    
        
        
