import time
import threading
from process import Process
from execqueue import ExecQueue
from escalonator import Escalonator

class CPU():
    """ Classe responsável pela execução dos processos """
    State = ['Ocioso', 'Executando', 'Pronto', 'Sobrecarga', 'PosSobrecarga', 'PreSobrecarga']
    
    def __init__(self, escalonator, mmu, ioqueue, quantum=0, process=None, disk=None): 
        """ Inicialização com as caracteristicas de uma CPU
        Args:
            escalonator (Escalonator): tipo de escalonador utilizado na CPU
            quantum (int): quantidade de tempo destinado a execução do processo
            process (Process): processo a ser executado na CPU
        
        """
        
        self.clock = 0              # Tempo que a CPU permaneceu ligada
        self.quantum = quantum
        self.escalonator = escalonator
        self.process = process        
        self.processing_time = 0
        self.concluded_process_time = []
        self.mmu = mmu
        self.ioqueue = ioqueue
        self.override_time = 0
        self.state = CPU.State[0]
        self.disk = disk
        
    def run(self):
        """ Método para execução da CPU """
        
        # Verificação de preemptividade
        self.preemptiveness = False if self.escalonator.algorithm in self.escalonator.NON_PREEMPTIVE_ALGORITHMS else True       

        #if self.process == None:
            #print('ID: None')
        #else:
            #print('ID: %s' %self.process.id)
        #print('Block: %s' %self.ioqueue.queue)
        #print('Pronto: %s' %self.escalonator.ready_queue)
        
        while len(self.escalonator.ready_queue) > 0:  
            self.process = self.escalonator.ready_queue[0]
            
            # Caso o processo não começe exatamente onde a CPU está 
            while self.clock < self.process.start:
                self.clock += 1 
                
            # O tempo de execução dos processos da fila de prontos depende da preemptividade da CPU
            if not self.preemptiveness:
                self.cpu_time = self.process.execution_time               
            else:
                self.cpu_time = self.quantum     

            #print('ID: %s' %self.process.id)
            #print('Block: %s' %self.ioqueue.queue)
            #print('Pronto: %s' %self.escalonator.ready_queue)

            isAlloc = self.mmu.isAllocated(self)
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
        #print("CPU executou todos os processos")

    def runClock(self):
        """ Método para execução de um clock da CPU """
        
        # Verificação de preemptividade
        self.preemptiveness = False if self.escalonator.algorithm in self.escalonator.NON_PREEMPTIVE_ALGORITHMS else True       
        #self.escalonator.nextProcess()
        
        if self.state == CPU.State[5]:
            self.state = CPU.State[3]
        
        if self.state == CPU.State[2] or self.state == CPU.State[4]:
            self.override_time = 0
            self.state = CPU.State[0]
            
        while self.state == CPU.State[0]:
            if self.escalonator.ready_queue:
                self.state = CPU.State[1]
                self.process = self.escalonator.ready_queue.pop(0)
            else:
                return
            isAlloc = self.mmu.isAllocated(self.process)
            self.process.nextState(self.mmu)

            if isAlloc == False:
                self.ioqueue.enqueue(self.process)
                self.state = CPU.State[0]
            else:
                self.processing_time = 0
                self.mmu.referentiate(self.process)

        if self.preemptiveness:    
            
            if self.state != CPU.State[3]:
                self.execute()
                self.process.priority /= 2
                if self.quantum - self.processing_time == 0:
                    self.state = CPU.State[5]
                
            
            if self.process.finished(self.mmu):
                self.mmu.deallocate(self.process)
                self.concluded_process_time.append((self.clock+1) - self.process.start)
                self.state = CPU.State[2]
                
            elif self.quantum - self.processing_time == 0:
                if self.escalonator.override == 0:
                    self.state = CPU.State[2]
                    self.escalonator.updateDeadline()
                    self.escalonator.ready_queue.append(self.process)
                    self.override_time = 0
                
                elif self.escalonator.override - self.override_time == 0:
                    self.state = CPU.State[4]
                    self.escalonator.updateDeadline()
                    self.escalonator.ready_queue.append(self.process)
                    self.override_time = 0
                else:
                    self.override_time += 1
                    return
                # self.removeProcess()
        else:
            self.execute()
            if self.process.finished(self.mmu):
                self.mmu.deallocate(self.process)
                self.concluded_process_time.append((self.clock+1) - self.process.start)
                self.state = CPU.State[2]
                #self.removeProcess()
                
                
        
    def execute(self):
        """ Método para executar um processo """
        self.process.nextState(self.mmu)
        self.processing_time += 1
        #time.sleep(self.processing_time)
        #print ("CPU executou {} que precisa de {}s por {}s" .format(self.process.id, self.process.execution_time, self.processing_time))
        self.process.execution_time -= 1
