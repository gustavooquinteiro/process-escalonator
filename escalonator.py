import time
import process
import threading

class Escalonator():
    def __init__(self, typeof="FCFS", quantum =2, override = .015, cpu=None):
        self.ready_queue = []
        self.algorithm = typeof
        self.quantum = quantum
        self.override = override
        self.preemptiveness = False if self.algorithm == "FCFS" or self.algorithm == "SJF" else True
        self.cpu = cpu
        self.mutex = threading.Lock()

        
    def queue(self):
        if self.algorithm == "FCFS" or self.algorithm == "RR":
            self.ready_queue.sort(key=lambda x: x.start)
        if self.algorithm == "SJF":
            self.ready_queue.sort(key=lambda x: (x.start, x.execution_time))
        if self.algorithm == "EDF":
            self.ready_queue.sort(key=lambda x: (x.start, x.deadline))
        self.cpu.cpuWorking.set()

    def updateDeadline(self):
        waiting_time = 0
        for process in self.ready_queue:     
            if process.start < self.cpu.cpu_execution:
                process.deadline -= self.cpu.processing_time + process.start
            waiting_time = self.cpu.processing_time + self.override
            print ("Processo {} agr com deadline de {}" .format(process.id, process.deadline))        
        
    def remove(self, process):
        if self.preemptiveness:
            if process.finished():
                self.ready_queue.remove(process)
            else:
                if process.needIO:
                    self.ready_queue.remove(process)
                else:
                    self.next_process()
                    time.sleep(self.override)
            self.updateDeadline()
            self.cpu.cpu_execution += self.override
            if process.outOfTime() and self.algorithm == "EDF":
                print("Processo {} está fora do prazo" .format(process.id))
        else:
            self.ready_queue.remove(process)

    def next_process(self):
        if len(self.ready_queue) > 1:
            self.ready_queue = self.ready_queue[1:]+[self.ready_queue[0]]
