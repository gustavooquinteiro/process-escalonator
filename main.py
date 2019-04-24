from ioqueue import IO
import cpu
import random
import process
import escalonator

l = [True, False]
io = IO()
escalonator = escalonator.Escalonator("RR")
c = cpu.CPU(escalonator)
escalonator.cpu = c
io.escalonator= escalonator
processes = []
for i in range(3):
    i = random.randint(1000, 3000)
    bolean = True
    p = process.Process(i, random.randint(0, 3), random.randint(1, 5), 1, 2, bolean, io)
    escalonator.queue(p)    
    processes.append(p)
