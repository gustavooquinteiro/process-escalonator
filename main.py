from escalonator import Escalonator
from process import Process
from ioqueue import IO
from cpu import CPU
from mmu import MMU, VirtualMemory
import random

def main():
    quantum = int(input("Quantum: "))
    override = int(input("Sobrecarga: "))
    type = str(input("Tipo de algoritmo de escalonamento (FCFS | SJF | RR | EDF): "))
    typeMMU = str(input("Algoritmo de substituição de página (FIFO | LRU ): "))
    escalonator = Escalonator(type.upper(), override)
    vm = VirtualMemory(100)
    mmu = MMU(vm, typeMMU.upper())
    io = IO(mmu)
    io.escalonator = escalonator
    cpu = CPU(escalonator, mmu, io, quantum)
    escalonator.cpu = cpu
    n = int(input("Quantidade de processos: "))
    for i in range(n):
        id = i 
        print("Criando o processo {}: " .format(id))
        start = int(input("Tempo de chegada: "))
        execution_time = int(input("Tempo de execução: "))
        deadline = int(input("Deadline: "))    
        numpages = int(input("Número de páginas: "))
        p = Process(id, start, execution_time, numpages, deadline=deadline, io=io)
        escalonator.insertProcess(p)
        
    escalonator.not_arrived.sort(key=lambda x: x.start)
    escalonator.queue()
      
    while n != len(cpu.concluded_process_time):
        escalonator.nextProcess()
        cpu.runClock()
        #print(cpu.state)
        cpu.clock += 1

    #escalonator.queue()
    #cpu.run()
    io.io.join(1)
    turnaround = sum(cpu.concluded_process_time)/n
    print("Turnaround == {}" .format(turnaround))

if __name__ == "__main__":
    main()
    
