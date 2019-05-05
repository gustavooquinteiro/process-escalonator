import time
import threading
from escalonator import Escalonator

class CPU():
    def __init__(self, escalonator, process=None): 
        self.cpu_time = 0
        self.cpu_execution = 0
        self.processing_time = 0
        self.escalonator = escalonator
        self.mutex = threading.Lock()
        self.cpuWorking = threading.Event()
        self.process = process        
        self.cpu = threading.Thread(target=self.execute)
        self.cpu.start()
        
    def execute(self):
        while True:
            self.mutex.acquire()
            if len(self.escalonator.ready_queue) > 0:                
                if not self.escalonator.preemptiveness:
                    self.process = self.escalonator.ready_queue[0]
                    self.mutex.release()
                    self.cpuWorking.clear()
                    while self.cpu_execution < self.process.start:
                        self.cpu_execution += 1
                    self.cpu_time = self.process.execution_time
                    self.process.execute(self)                    
                    self.escalonator.remove(self.process)
                else:
                    self.cpu_time = self.escalonator.quantum
                    self.process = self.escalonator.ready_queue[0]
                    self.mutex.release()
                    self.cpuWorking.clear()
                    if self.cpu_execution >= self.process.start:
                        self.process.execute(self)
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
  
    def stop(self):
        print("CPU encerrando")
        self.cpu.join()
