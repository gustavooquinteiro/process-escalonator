import random

class Page():
    def __init__(self):
        self.num = None
        self.freq = 0

    def getNum(self): return self.num
    def setNum(self, n): self.num = n

    def getFreq(self): return self.freq
    def setFreq(self, freq): self.freq = freq

    def isAllocated(self):
        if self.num and self.freq == 0:
            return False
        return True

class RAM():
    def __init__(self):
        self.algorithm = 'FIFO'
        self.queue = []
        for i in range(50):
            page = Page()
            self.queue.append(page)
        self.ram_pointer = 0

    def setAlgorithm(self, algorithm): self.algorithm = algorithm

    def hasClear(self):
        for page in self.queue:
            if page.isAllocated() == False:
                return True
        return False

    def substitutePage(self, process):
        if self.algorithm == 'FIFO':
            ref_ram = self.ram_pointer
            self.queue[ref_ram].setNum(process.id)
            self.queue[ref_ram].setFreq(1)

            self.ram_pointer += 1
            if self.ram_pointer >= 50:
                self.ram_pointer = 0

            return ref_ram
        elif self.algorithm == 'LRU':
            leastFreq = self.queue[0]
            index = 0
            for i in range(50):
                if leastFreq.getFreq() > self.queue[i].getFreq():
                    leastFreq = self.queue[i]
                    index = i

            ref_ram = index
            self.queue[ref_ram].setNum(process.id)
            self.queue[ref_ram].setFreq(1)

            return ref_ram
        
    def allocatePage(self, process):
        if self.hasClear():
            rand = random.randint(0, 49)
            while self.queue[rand].isAllocated():
                rand = random.randint(0, 49)

            self.queue[rand].setNum(process.id)
            self.queue[rand].setFreq(1)

            return rand
        else:
            return self.substitutePage(process)


class VirtualMemory():
    def __init__(self, max):
        self.algorithm = 'FIFO'
        self.mem_vm = []
        for i in range(max):
            self.mem_vm.append([None, 0])
        self.mem_ram = RAM()
        self.vm_pointer = 0

    def setAlgorithm(self, algorithm): self.algorithm = algorithm

    def hasClear(self):
        for ref in self.mem_vm:
            if ref[0] == None:
                return True
        return False

    def isAllocated(self, process):
        ret = True
        if process.getNumPages() != len(process.getPages()):
            ret = False

        for ref in process.getPages():
            if self.mem_vm[ref][0] == None:
                self.mem_vm[ref] = [None, 0]
                ret = False
            elif self.mem_ram.queue[self.mem_vm[ref][0]].getNum() != process.id:
                self.mem_vm[ref] = [None, 0]
                ret = False

        return ret

    def substitutePage(self, process):
        if self.algorithm == 'FIFO':
            ref_ram = self.mem_vm[self.vm_pointer][0]
            self.mem_ram.queue[ref_ram].setNum(process.id)
            self.mem_ram.queue[ref_ram].setFreq(1)
            ind = self.vm_pointer
            self.vm_pointer += 1
            if self.vm_pointer >= len(self.mem_vm):
                self.vm_pointer = 0

            return ind
        elif self.algorithm == 'LRU':
            leastFreq = self.mem_vm[0]
            index = 0
            for i in range(len(self.mem_vm)):
                if leastFreq[1] > self.mem_vm[i][1]:
                    leastFreq = self.mem_vm[i]
                    index = i

            ref_ram = leastFreq[0]
            self.mem_ram.queue[ref_ram].setNum(process.id)
            self.mem_ram.queue[ref_ram].setFreq(1)
            ind = index

            return ind
            

    def allocatePage(self, process):
        page = None
        for i in range(len(self.mem_vm)):
            if self.isPageAllocated(self.mem_vm[i]) == False:
                ram_ind = self.mem_ram.allocatePage(process)
                self.mem_vm[i].setIndex(ram_ind)
                self.mem_vm[i].setNum(process.id)
                self.mem_vm[i].setAllocated(True)
                page = self.mem_vm[i]
                break

class MMU():
    def __init__(self, vm, algorithm):
        self.vm = vm
        self.vm.setAlgorithm(algorithm)
        self.vm.mem_ram.setAlgorithm(algorithm)

    def isAllocated(self, process):
        return self.vm.isAllocated(process)

    def giveMemAddr(self, process):
        pages = []
        for i in range(process.getNumPages()):
            if self.vm.hasClear():
                rand = random.randint(0, len(self.vm.mem_vm)-1)
                while self.vm.mem_vm[rand][0] != None:
                    rand = random.randint(0, len(self.vm.mem_vm)-1)

                self.vm.mem_vm[rand][1] = 1
                self.vm.mem_vm[rand][0] = self.vm.mem_ram.allocatePage(process)

                pages.append(rand)
            else:
                page = self.vm.substitutePage(process)
                pages.append(page)

        return pages


    def reallocate(self, process):
        pages = process.getPages()

        for ref in process.getPages():
            if self.vm.mem_ram.queue[self.vm.mem_vm[ref][0]].getNum() != process.id:
                ind = self.vm.mem_ram.allocatePage(process)
                self.vm.mem_vm[ref][0] = ind
                self.vm.mem_vm[ref][1] = 1
            else:
                self.vm.mem_vm[ref][1] += 1

    def deallocate(self, process):
        for ref in process.getPages():
            newPage = Page()
            self.vm.mem_ram.queue[self.vm.mem_vm[ref][0]] = newPage
            self.vm.mem_vm[ref] = [None, 0]