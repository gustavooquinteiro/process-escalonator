import random

class Page():
    def __init__(self):
        self.num = None
        self.index = None
        self.freq = 0

    def isAllocated(self):
        if self.num == None and self.index == None and self.freq == 0:
            return False
        return True

class RAM():

    SIZE = 50

    def __init__(self):
        self.algorithm = 'FIFO'
        self.queue = []
        for i in range(RAM.SIZE):
            page = Page()
            self.queue.append(page)
        self.ram_pointer = 0

    def setAlgorithm(self, algorithm): self.algorithm = algorithm

    def hasClear(self):
        for page in self.queue:
            if page.isAllocated() == False:
                return True
        return False

    def substitutePage(self, process, ind):
        if self.algorithm == 'FIFO':
            ref_ram = self.ram_pointer
            while self.queue[ref_ram].num == process.id:
                self.ram_pointer += 1
                if self.ram_pointer >= RAM.SIZE:
                    self.ram_pointer = 0
                ref_ram = self.ram_pointer
            
            oldIndex = self.queue[ref_ram].index
            self.queue[ref_ram].num = process.id
            self.queue[ref_ram].freq = 0
            self.queue[ref_ram].index = ind

            self.ram_pointer += 1
            if self.ram_pointer >= RAM.SIZE:
                self.ram_pointer = 0

            return ref_ram, oldIndex
        elif self.algorithm == 'LRU':
            leastFreq = self.queue[0]
            index = 0
            for i in range(RAM.SIZE):
                if leastFreq.freq > self.queue[i].freq:
                    leastFreq = self.queue[i]
                    index = i

            ref_ram = index
            oldIndex = self.queue[ref_ram].index

            self.queue[ref_ram].num = process.id
            self.queue[ref_ram].freq = 0
            self.queue[ref_ram].index = ind

            return ref_ram, oldIndex
        
    def allocatePage(self, process, ind):
        if self.hasClear():
            rand = random.randint(0, RAM.SIZE-1)
            while self.queue[rand].isAllocated():
                rand = random.randint(0, RAM.SIZE-1)

            self.queue[rand].num = process.id
            self.queue[rand].freq = 0
            self.queue[rand].index = ind

            return rand, -1
        else:
            return self.substitutePage(process, ind)


class VirtualMemory():

    SIZE = 100

    def __init__(self, max):
        self.algorithm = 'FIFO'
        self.mem_vm = []
        for i in range(VirtualMemory.SIZE):
            self.mem_vm.append([None, 0])
        self.mem_ram = RAM()
        self.vm_pointer = 0

    def setAlgorithm(self, algorithm): self.algorithm = algorithm

    def hasClear(self):
        for ref in self.mem_vm:
            if ref[0] == None:
                return True
        return False

    def isPageAllocated(self, process, ref):
        if self.mem_vm[ref][0] == None:
            return False
        elif self.mem_ram.queue[self.mem_vm[ref][0]].num != process.id:
            return False
        
        return True

    def isAllocated(self, process):
        ret = True
        if process.getNumPages() != len(process.getPages()):
            ret = False

        for ref in process.getPages():
            if self.mem_vm[ref][0] == None:
                ret = False
            elif self.mem_ram.queue[self.mem_vm[ref][0]].num != process.id:
                ret = False

        return ret

    def substitutePage(self, process):
        if self.algorithm == 'FIFO':
            ind = self.vm_pointer

            while self.mem_ram.queue[self.mem_vm[ind][0]] == process.id:
                self.vm_pointer += 1
                if self.vm_pointer >= VirtualMemory.SIZE: self.vm_pointer = 0
                ind = self.vm_pointer

            self.vm_pointer += 1
            if self.vm_pointer >= VirtualMemory.SIZE:
                self.vm_pointer = 0

            return ind
        elif self.algorithm == 'LRU':
            leastFreq = self.mem_vm[0]
            # index = 0
            for i in range(VirtualMemory.SIZE):
                if leastFreq[1] > self.mem_vm[i][1]:
                    leastFreq = self.mem_vm[i]
                    # index = i

            rand = random.randint(0, VirtualMemory.SIZE-1)
            while self.mem_vm[rand][1] != leastFreq or rand in process.getPages():
                rand = random.randint(0, VirtualMemory.SIZE-1)

            ind = rand

            return ind


    def allocatePage(self, process, ref):
        page = None

        if ref == None:
            if self.hasClear():
                rand = random.randint(0, VirtualMemory.SIZE-1)
                while self.mem_vm[rand][0] != None:
                    rand = random.randint(0, VirtualMemory.SIZE-1)

                ram_ind, oldIndex = self.mem_ram.allocatePage(process, rand)
                if oldIndex != -1 and oldIndex != None:
                    self.mem_vm[oldIndex] = [None, 0]
                
                self.mem_vm[rand][0] = ram_ind
                self.mem_vm[rand][1] = 0
                
                return rand
            else:
                ref_vm = self.substitutePage(process)
                ram_ind, oldIndex = self.mem_ram.allocatePage(process, ref_vm)
                if oldIndex != -1 and oldIndex != None:
                    self.mem_vm[oldIndex] = [None, 0]

                self.mem_vm[ref_vm][0] = ram_ind
                self.mem_vm[ref_vm][1] = 0

                return ref_vm

        else:
            ram_ind, oldIndex = self.mem_ram.allocatePage(process, ref)
            if oldIndex != -1 and oldIndex != None:
                self.mem_vm[oldIndex] = [None, 0]
            
            self.mem_vm[ref][0] = ram_ind
            self.mem_vm[ref][1] = 0

            print(self.mem_vm[ref])

            return ref

        # for i in range(len(self.mem_vm)):
        #     if self.isPageAllocated(self.mem_vm[i]) == False:
        #         ram_ind, oldIndex = self.mem_ram.allocatePage(process, i)
        #         if oldIndex != -1:
        #             self.mem_vm[oldIndex] = [None, 0]
        #         self.mem_vm[i].index = ram_ind
        #         self.mem_vm[i].num = process.id
        #         page = self.mem_vm[i]
        #         break

class MMU():
    def __init__(self, vm, algorithm):
        self.vm = vm
        self.vm.setAlgorithm(algorithm)
        self.vm.mem_ram.setAlgorithm(algorithm)

    def isAllocated(self, process):
        print('Processo %d esta alocado? %s' %(process.id, self.vm.isAllocated(process)))
        return self.vm.isAllocated(process)

    # def giveMemAddr(self, process):
    #     pages = []
        
    #     print('giveMemAddr: ', end='')
    #     for i in range(process.getNumPages()):
    #         if self.vm.hasClear():
    #             rand = random.randint(0, len(self.vm.mem_vm)-1)
    #             while self.vm.mem_vm[rand][0] != None:
    #                 rand = random.randint(0, len(self.vm.mem_vm)-1)

    #             self.vm.mem_vm[rand][1] = 1
    #             self.vm.mem_vm[rand][0], oldIndex = self.vm.mem_ram.allocatePage(process, rand)
    #             print(oldIndex)
    #             if oldIndex != -1:
    #                 self.vm.mem_vm[oldIndex] = [None, 0]

    #             print(self.vm.mem_vm[rand], end='1-')

    #             pages.append(rand)
    #         else:
    #             page = self.vm.substitutePage(process)
    #             print(self.vm.mem_vm[rand], end='2-')
    #             pages.append(page)

    #     print(pages, end='-')
    #     return pages


    def allocate(self, process):
        pages = []

        if process.pages == []:
            for i in range(process.numpages):
                ref = self.vm.allocatePage(process, None)
                print(self.vm.mem_ram.queue[self.vm.mem_vm[ref][0]].num, end=':')
                print(self.vm.mem_vm[ref][0], end='-')
                pages.append(ref)
        else:
            for ref in process.pages:
                if self.vm.isPageAllocated(process, ref) == False:
                    self.vm.allocatePage(process, ref)
                    print('not alloc')
                else:
                    self.vm.mem_vm[ref][1] += 1

        print('allocate: ', end='')
        # for ref in process.getPages():
        #     if self.vm.mem_ram.queue[self.vm.mem_vm[ref][0]].num != process.id:
        #         ind, oldIndex = self.vm.mem_ram.allocatePage(process, ref)
        #         print("old: %d" %oldIndex)
        #         if oldIndex != -1:
        #             self.vm.mem_vm[oldIndex] = [None, 0]
        #         self.vm.mem_vm[ref][0] = ind
        #         self.vm.mem_vm[ref][1] = 1
        #         print(self.vm.mem_vm[ref], end='1-')
        #     else:
        #         self.vm.mem_vm[ref][1] += 1
        #         print(self.vm.mem_vm[ref], end='2-')

        # print(pages, end='-')

        print(pages)
        return pages

    def deallocate(self, process):
        for ref in process.getPages():
            newPage = Page()
            print('Desalocou %d, pagina %d' %(process.id, ref))
            print(self.vm.mem_vm[ref])
            if self.vm.isPageAllocated(process, ref):
                self.vm.mem_ram.queue[self.vm.mem_vm[ref][0]] = newPage
                self.vm.mem_vm[ref] = [None, 0]
            else:
                print('not')
            # if self.vm.mem_vm[ref][0] != None:
            #     if self.vm.mem_ram.queue[self.vm.mem_vm[ref][0]].num == process.id:
                    
            #     else:
            #         print('not')