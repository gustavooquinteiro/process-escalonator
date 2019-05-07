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
        self.mutex = threading.Lock()
        self.cpuWorking = threading.Event()
        self.process = process        
        self.cpu = threading.Thread(target=self.run)
        self.cpu.start()
        
    def run(self):
        """ Método para execução da CPU """
        
        # Verificação de preemptividade
        self.preemptiveness = False if self.escalonator.algorithm == "FCFS" or self.escalonator.algorithm == "SJF" else True
        
        while True:
            self.mutex.acquire()
            if len(self.escalonator.ready_queue) > 0: 
                # O modo de executar os processos da fila de prontos depende da preemptividade da CPU
                if not self.preemptiveness:
                    self.process = self.escalonator.ready_queue[0]
                    self.mutex.release()
                    self.cpuWorking.clear()
                    # Caso o processo não começe exatamente quando a CPU iniciou 
                    while self.cpu_execution < self.process.start:
                        self.cpu_execution += 1
                    self.cpu_time = self.process.execution_time
                    self.execute()                    
                    self.escalonator.remove(self.process)
                else:
                    self.cpu_time = self.quantum
                    self.process = self.escalonator.ready_queue[0]
                    self.mutex.release()
                    self.cpuWorking.clear()
                    if self.cpu_execution >= self.process.start:
                        self.execute()
                    else:
                        if all(self.cpu_execution < process.start for process in self.escalonator.ready_queue):
                            self.cpu_execution += 1
                        else:
                            self.escalonator.next_process()
                    
                    self.escalonator.remove(self.process)
            else:         
                print("CPU esperando por processos")
                self.mutex.release()
                self.cpuWorking.wait()
                
    def execute(self):
        """ Método para executar um processo """
        self.process.nextState()
        print("Processo {} em estado de {}" .format(self.process.id ,self.process.state))
        if self.cpu_time > self.process.execution_time:
            self.processing_time = self.cpu_time - self.process.execution_time  
        else:
            self.processing_time = self.cpu_time
        time.sleep(self.processing_time)    
        print ("CPU executou {} que precisa de {}s por {}s" .format(self.process.id, self.process.execution_time, self.processing_time))
        self.process.execution_time -= self.processing_time
        self.cpu_execution += self.processing_time
        
        
    def stop(self):
        """ Método para desligar a CPU"""
        print("CPU encerrando")
        self.cpu.join()
