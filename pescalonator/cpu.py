import time
import threading
from escalonator import Escalonator

class CPU():
    """ Classe responsável pela execução dos processos """
    def __init__(self, escalonator, quantum=0, process=None): 
        """ Inicialização com as caracteristicas de uma CPU
        Args:
            escalonator (Escalonator): tipo de escalonador utilizado na CPU
            quantum (int): quantidade de tempo destinado a execução do processo
            process (Process): processo a ser executado na CPU
        
        """
        self.cpu_time = 0           # Tempo que a CPU tem para cada processo
        self.cpu_execution = 0      # Tempo que a CPU permaneceu ligada
        self.quantum = quantum
        self.escalonator = escalonator
        self.process = process        
        self.concluded_process_time = []
        
    def run(self):
        """ Método para execução da CPU """
        
        # Verificação de preemptividade
        self.preemptiveness = False if self.escalonator.algorithm in self.escalonator.NON_PREEMPTIVE_ALGORITHMS else True
        
        while len(self.escalonator.ready_queue) > 0:  
            self.process = self.escalonator.ready_queue[0]
            
            # Caso o processo não começe exatamente onde a CPU está 
            while self.cpu_execution < self.process.start:
                self.cpu_execution += 1 
                
            # O tempo de execução dos processos da fila de prontos depende da preemptividade da CPU
            if not self.preemptiveness:                
                self.cpu_time = self.process.execution_time               
            else:
                self.cpu_time = self.quantum                
                
            self.execute()                    
            self.escalonator.manageQueue(self.process)
                

        print("CPU executou todos os processos")                    
                
    def execute(self):
        """ Método para executar um processo """
        self.process.nextState()
        if self.cpu_time > self.process.execution_time:
            self.processing_time = self.cpu_time - self.process.execution_time  
        else:
            self.processing_time = self.cpu_time
        time.sleep(self.processing_time)    
        print ("CPU executou {} que precisa de {}s por {}s" .format(self.process.id, self.process.execution_time, self.processing_time))
        self.process.execution_time -= self.processing_time
        self.cpu_execution += self.processing_time
        if self.process.isFinished():
            self.concluded_process_time.append(self.cpu_execution - self.process.start)

