from escalonator import Escalonator
from process import Process
from ioqueue import IO
from cpu import CPU
from mmu import MMU, VirtualMemory
import random
import time
from Gantt import Window_Gantt

class main():
    def __init__(self, processes, quantum, override, type, typeMMU):
        super().__init__()
        self.quantum = quantum
        self.override = override
        self.type = type
        self.typeMMU = typeMMU
        escalonator = Escalonator(self.type.upper(), self.override)
        self.processes = processes
        vm = VirtualMemory(100)
        mmu = MMU(vm, self.typeMMU.upper())
        io = IO(mmu)
        io.escalonator = escalonator
        cpu = CPU(escalonator, mmu, io, self.quantum)
        escalonator.cpu = cpu
        n = len(self.processes)
        for i in self.processes:
            i.io = io
            i.numpages = 10
            escalonator.insertProcess(i)

        escalonator.not_arrived.sort(key=lambda x: x.start)
        escalonator.queue()
        gantt = Window_Gantt(escalonator.not_arrived, escalonator.ready_queue)

        while n != len(cpu.concluded_process_time):
            escalonator.nextProcess()
            cpu.runClock()
            io.wait_for_resource(cpu)

            print('Prontos: ', end='')
            for proc in escalonator.ready_queue:
                print(proc.id, end=' ')
            print()
            print('Bloqueados: ', end='')
            for proc in io.queue:
                print(proc.id, end=' ')
            print()

            #print(cpu.state)
            gantt.updateGantt(cpu.clock, escalonator, io, cpu)
            cpu.clock += 1
            time.sleep(1)

        #escalonator.queue()
        #cpu.run()
        # io.io.join(1)

        turnaround = sum(cpu.concluded_process_time)/n
        print("Turnaround == {0:.2f}" .format(turnaround))
        
if __name__ == "__main__":
    main()
    