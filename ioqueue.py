import time 
import random
import threading
import escalonator 
import process
import mmu

class IO(): 
    def __init__(self, mmu, disk, escalonator = None):
        self.queue = []
        self.mmu = mmu
        self.escalonator = escalonator
        self.disk = disk
            
    def enqueue(self, process):       
        self.queue.append(process)
        # self.wait_for_resource()

    def isOnQueue(self, process):
        if process in self.queue:
            return True
        return False
        
    def wait_for_resource(self, cpu):
        if len(self.queue) > 0:
            process = self.queue[0]
            if (process.numpages - len(process.pages) > 0):
                for i in range(min(2, process.numpages - len(process.pages))):
                    process.addPages(self.mmu.allocatePage(process, cpuProcess=cpu.process))
            else:
                for i in range(min(2, len(list(filter(lambda ref: not self.mmu.vm.isPageAllocated(process, ref), process.pages))))):
                    process.addPages(self.mmu.allocatePage(process, cpuProcess=cpu.process))

            if self.mmu.isAllocated(process):
                process.nextState(self.mmu)
                self.escalonator.ready_queue.append(process)
                del self.queue[0]
                