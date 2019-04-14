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
for ll in range(3):
    i = random.randint(1000, 3000)
    bolean = True
    p = process.Process(i, random.randint(1, 5), io, 1, 2, bolean)
    escalonator.queue(p)    
