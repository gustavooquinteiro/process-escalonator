import time
import process
import threading

class Escalonator():
    def __init__(self, typeof="FCFS", quantum =2, override = .015, cpu=None):
        self.ready_queue = []
        self.algorithm = typeof
        self.quantum = quantum
        self.override = override
        self.preemptiveness = self.check()
        self.cpu = cpu
        self.mutex = threading.Lock()

        
    def queue(self):
        if self.algorithm == "FCFS":
            self.ready_queue.sort(key=lambda x: x.start)
        if self.algorithm == "SJF":
            self.ready_queue.sort(key=lambda x: x.execution_time and x.start)
        if self.algorithm == "PQ":
            self.ready_queue.sort(key=lambda x: x.priority and x.start, reverse=True)
        if self.algorithm == "EDF":
            self.ready_queue.sort(key=lambda x: x.deadline and x.start)
        self.cpu.cpuWorking.set()
                
    def check(self):
        if self.algorithm == "FCFS" or self.algorithm == "SJF":
            return False
        return True
    
    def remove(self, process):
        if self.preemptiveness:
            if process.finished():
                self.ready_queue.remove(process)
            else:
                if process.needIO:
                    self.ready_queue.remove(process)
                else:
                    self.ready_queue = self.ready_queue[1:]+[self.ready_queue[0]]
                    time.sleep(self.override)
        else:
            self.ready_queue.remove(process)
