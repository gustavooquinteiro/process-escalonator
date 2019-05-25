import time 
import random
import threading
import escalonator 
import process

class IO(): 
    def __init__(self, mmu, escalonator = None):
        self.queue = []
        self.mmu = mmu
        self.mutex = threading.Condition()
        self.ioWorking = threading.Event()
        self.io = threading.Thread(target=self.run)
        self.escalonator = escalonator
        self.io.start()
        
    def run(self):
        while True:
            if self.queue:
                self.mutex.acquire()
                print('wait_for_resource')
                self.wait_for_resource()
                self.mutex.release()
                self.ioWorking.clear()
            else:            
                self.ioWorking.wait()
                
            
    def enqueue(self, process):
        self.mutex.acquire()
        self.queue.append(process)
        self.mutex.release()
        self.ioWorking.set()

    def isOnQueue(self, process):
        if process in self.queue:
            return True
        return False
        
    def wait_for_resource(self):
        process = self.queue[0]
        print ("Processo {} na fila de Bloqueados " .format(process.id))
        
        time_now = time.time()
        while time.time() - time_now < 0.001:
            continue

        if process.getPages() == []:
            process.setPages(self.mmu.giveMemAddr(process))
        elif process.execution_time != 0:
            self.mmu.reallocate(process)
            process.nextState(self.mmu)
            print(process)
            if process.state == Process.States[1]:
                self.escalonator.ready_queue.append(process)
                # self.escalonator.queue()
                print ("Processo {} na fila de Pronto " .format(process.id))
        del self.queue[0]
