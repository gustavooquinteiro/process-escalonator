from escalonator import Escalonator
from process import Process
from ioqueue import IO
from cpu import CPU
from mmu import MMU
import random

def main():
    quantum = int(input("Quantum: "))
    override = int(input("Sobrecarga: "))
    type = str(input("Tipo de algoritmo de escalonamento (FCFS | SJF | RR | EDF): "))
    escalonator = Escalonator(type.upper(), override)
    mmu = MMU()
    cpu = CPU(escalonator, mmu, quantum)
    escalonator.cpu = cpu
    #io = IO()
    #io.escalonator = escalonator
    n = int(input("Quantidade de processos: "))
    for i in range(n):
        id = i 
        print("Criando o processo {}: " .format(id))
        start = int(input("Tempo de chegada: "))
        execution_time = int(input("Tempo de execução: "))
        deadline = int(input("Deadline: "))    
        numPages = int(input("Numero de Paginas: "))    
        p = Process(id, start, execution_time, numPages, deadline)
        escalonator.ready_queue.append(p)
        
    escalonator.queue()
    cpu.run()
    
    turnaround = sum(cpu.concluded_process_time)/n
    print("Turnaround == {}" .format(turnaround))

if __name__ == "__main__":
    main()
