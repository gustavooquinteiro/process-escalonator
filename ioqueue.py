import time 
import random
import threading
import escalonator 
import process
import mmu

class IO(): 
    def __init__(self, mmu, escalonator = None):
        self.queue = []
        self.mmu = mmu
        self.escalonator = escalonator
            
    def enqueue(self, process):       
        self.queue.append(process)
        self.wait_for_resource()

    def isOnQueue(self, process):
        if process in self.queue:
            return True
        return False
        
    def wait_for_resource(self):
        process = self.queue[0]
        print ("Processo {} na fila de Bloqueados " .format(process.id))
        
        time_now = time.time()
        while time.time() - time_now < 1:
            continue
        print("passou do while")
        if process.getPages() == []:
            print("entro aqu")
            process.setPages(self.mmu.giveMemAddr(process))
        elif process.execution_time != 0:
            self.mmu.reallocate(process)
        process.nextState(self.mmu)
        if process.state == process.__class__.States[1]:
            self.escalonator.ready_queue.append(process)
            # self.escalonator.queue()
            print ("Processo {} na fila de Pronto " .format(process.id))
        del self.queue[0]
