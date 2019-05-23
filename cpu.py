import time
import threading
from process import Process
from execqueue import ExecQueue
from escalonator import Escalonator

class CPU():
    """ Classe responsável pela execução dos processos """
    def __init__(self, escalonator, mmu, ioqueue, quantum=0, process=None): 
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
        self.mmu = mmu
        self.ioqueue = ioqueue
        
    def run(self):
        """ Método para execução da CPU """
        
        # Verificação de preemptividade
        self.preemptiveness = False if self.escalonator.algorithm in self.escalonator.NON_PREEMPTIVE_ALGORITHMS else True       

        if process == None:
            print('ID: None')
        else:
            print('ID: %s' %self.process.id)
        print('Block: %s' %self.ioqueue.queue)
        print('Pronto: %s' %self.escalonator.ready_queue)
        
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

            print('ID: %s' %self.process.id)
            print('Block: %s' %self.ioqueue.queue)
            print('Pronto: %s' %self.escalonator.ready_queue)

            isAlloc = mmu.isAllocated(self)
            if self.process.state == Process.States[0] and isAlloc == False:
                self.io.enqueue(self.process)
                self.escalonator.forceRemove(self.process)
                continue

            self.execute()

            if self.preemptiveness:
                if self.escalonator.remove(self.process):
                    self.mmu.deallocate(self.process)
                if self.preemptiveness and not self.escalonator.ready_queue and self.escalonator.not_arrived:
                    self.escalonator.nextProcess()
            else:
                if self.escalonator.remove(self.process):
                    self.mmu.deallocate(self.process)
                if self.preemptiveness and not self.escalonator.ready_queue and self.escalonator.not_arrived:
                    self.escalonator.nextProcess()

        print("CPU executou todos os processos")                    

    def runClock(self):
        """ Método para execução de um clock da CPU """
        
        # Verificação de preemptividade
        self.preemptiveness = False if self.escalonator.algorithm in self.escalonator.NON_PREEMPTIVE_ALGORITHMS else True       
        
        self.process = self.escalonator.ready_queue[0]
            # # Caso o processo não começe exatamente onde a CPU está 
            # while self.cpu_execution < self.process.start:
            #     self.cpu_execution += 1 
                
        # O tempo de execução dos processos da fila de prontos depende da preemptividade da CPU
        if not self.preemptiveness:
            self.cpu_time = self.process.execution_time               
        else:
            self.cpu_time = self.quantum     

        isAlloc = mmu.isAllocated(self)
        if self.process.state == Process.States[0] and isAlloc == False:
            self.io.enqueue(self.process)
            self.escalonator.forceRemove(self.process)
            if len(escalonator.ready_queue) > 0:
                self.process = self.escalonator.ready_queue[0]
            else:
                return

        self.execute()

        if self.preemptiveness:    
            if process.finished():
                self.mmu.deallocate(self.process)
                # self.removeProcess()
            elif self.cpu_time - self.processing_time == 0:
                self.escalonator.ready_queue.append(self.process)
                self.escalonator.queue()
                # self.removeProcess()
        else:
            if process.finished():
                self.mmu.deallocate(self.process)
                # self.removeProcess()

    def execute(self):
        """ Método para executar um processo """
        self.process.nextState(self.mmu)
        self.processing_time += 1
        time.sleep(self.processing_time)
        # print ("CPU executou {} que precisa de {}s por {}s" .format(self.process.id, self.process.execution_time, self.processing_time))
        self.process.execution_time -= 1
