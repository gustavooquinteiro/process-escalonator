import time
import threading
from escalonator import Escalonator

class CPU():
    def __init__(self, escalonator): 
        self.cpu_time = 0
        self.escalonator = escalonator
        self.mutex = threading.Lock()
        self.cpuWorking = threading.Event()
        cpu = threading.Thread(target=self.execute)
        cpu.start()
        
    def execute(self):
        while True:
            self.mutex.acquire()
            if len(self.escalonator.ready_queue) > 0:
                if not self.escalonator.preemptiveness:
                    process = self.escalonator.ready_queue[0]
                    self.mutex.release()
                    self.cpuWorking.clear()
                    self.cpu_time = process.execution_time
                    process.execute(self.cpu_time)
                    self.escalonator.remove(process)
                else:
                    self.cpu_time = self.escalonator.quantum
                    process = self.escalonator.ready_queue[0]
                    self.mutex.release()
                    self.cpuWorking.clear()
                    process.execute(self.cpu_time)
                    self.escalonator.remove(process)
            else:         
                print("CPU esperando por processos")
                self.mutex.release()
                self.cpuWorking.wait()
