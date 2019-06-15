import random

def transformList(mem, process, mem_vm):
    lista = mem
    if process == None:
        return lista
    for ref in process.pages:
        if mem_vm[ref][0] in lista:
            lista.remove(mem_vm[ref][0])
    return lista


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

    def __init__(self, disk, vm):
        self.algorithm = 'FIFO'
        self.queue = []
        for i in range(RAM.SIZE):
            page = Page()
            self.queue.append(page)
        self.ram_pointer = 0
        self.disk = disk
        self.vm = vm

    def setAlgorithm(self, algorithm):
        self.algorithm = algorithm


    def isAllocated(self, page):
        if page.isAllocated():
            return True
        return False

    def hasClear(self):
        for page in self.queue:
            if page.isAllocated() == False:
                return True
        return False

    def substitutePage(self, process, ind, cpuProcess=None, hadSubstitution=False):
        if self.algorithm == 'FIFO':
            ref_ram = self.ram_pointer

            while self.queue[ref_ram].num == process.id or (
                    cpuProcess != None and self.queue[ref_ram].index in cpuProcess.pages):
                self.ram_pointer += 1
                if self.ram_pointer >= RAM.SIZE:
                    self.ram_pointer = 0
                ref_ram = self.ram_pointer

            if not hadSubstitution:
                self.disk.putProcess(self.queue[ref_ram].num, 1)

            oldIndex = self.queue[ref_ram].index
            self.queue[ref_ram].num = process.id
            self.queue[ref_ram].freq = 0
            self.queue[ref_ram].index = ind

            self.ram_pointer += 1
            if self.ram_pointer >= RAM.SIZE:
                self.ram_pointer = 0

            return ref_ram, oldIndex
        elif self.algorithm == 'LRU':
            range_list = list(range(RAM.SIZE))
            if cpuProcess != None:
                for ref in cpuProcess.pages:
                    if self.vm[ref][0] in range_list:
                        range_list.remove(self.vm[ref][0])

            selec_list = []
            for ind in range_list:
                if self.queue[ind].num != process.id:
                    selec_list.append(ind)
            # selec_list = list(filter(lambda page: self.queue[page].num != process.id, selec_list))
            
            index = selec_list[0]
            for page in selec_list:
                if self.queue[index].freq > self.queue[page].freq:
                    index = page

            ref_ram = index
            oldIndex = self.queue[ref_ram].index

            if not hadSubstitution:
                self.disk.putProcess(self.queue[ref_ram].num, 1)

            self.queue[ref_ram].num = process.id
            self.queue[ref_ram].freq = 0
            self.queue[ref_ram].index = ind

            return ref_ram, oldIndex

    def allocatePage(self, process, ind, cpuProcess=None, hadSubstitution=False):
        selec_list = transformList(list(range(RAM.SIZE)), cpuProcess, self.vm)
        free_list = list(filter(lambda page: not self.isAllocated(self.queue[page]), selec_list))
        print(len(free_list))
        print(free_list)
        
        if len(free_list) > 0:
            rand = random.choice(free_list)
            self.queue[rand].num = process.id
            self.queue[rand].freq = 0
            self.queue[rand].index = ind

            return rand, -1
        else:
            return self.substitutePage(process, ind, cpuProcess, hadSubstitution)

    def clear(self):
        for ind in range(RAM.SIZE):
            newPage = Page()
            self.queue[ind] = newPage


class VirtualMemory():
    SIZE = 100

    def __init__(self, max, disk):
        self.algorithm = 'FIFO'
        self.mem_vm = []
        for i in range(VirtualMemory.SIZE):
            self.mem_vm.append([None, 0])
        self.mem_ram = RAM(disk, self.mem_vm)
        self.vm_pointer = 0
        self.disk = disk

    def setAlgorithm(self, algorithm):
        self.algorithm = algorithm

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
        elif not self.mem_ram.isAllocated(self.mem_ram.queue[self.mem_vm[ref][0]]):
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

    def substitutePage(self, process, cpuProcess=None):
        if self.algorithm == 'FIFO':
            ind = self.vm_pointer

            while self.mem_ram.queue[self.mem_vm[ind][0]].num == process.id or (cpuProcess != None and ind in cpuProcess.pages):
                self.vm_pointer += 1
                if self.vm_pointer >= VirtualMemory.SIZE: self.vm_pointer = 0
                ind = self.vm_pointer

            self.vm_pointer += 1
            if self.vm_pointer >= VirtualMemory.SIZE:
                self.vm_pointer = 0
            self.disk.putProcess(self.mem_ram.queue[self.mem_vm[ind][0]].num, 1)

            return ind
        elif self.algorithm == 'LRU':
            selec_list = list(filter(lambda page: self.mem_ram.queue[self.mem_vm[page]].num != process.id and page not in cpuProcess.pages,
                                     list(range(VirtualMemory.SIZE))))

            select_pages = list(self.mem_vm[i] for i in selec_list)
            leastFreq = min(select_pages, default=select_pages[0], key=lambda x: x[1])
            ind = random.choice(list(filter(lambda page: self.mem_vm[page][1] == leastFreq[1], selec_list)))

            self.disk.putProcess(self.mem_ram.queue[self.mem_vm[ind][0]].num, 1)

            return ind

    def allocatePage(self, process, ref, cpuProcess=None):
        page = None

        if ref == None:
            if self.hasClear():
                rand = random.choice(list(
                    filter(lambda page: self.mem_vm[page][0] == None and page not in cpuProcess.pages,
                           list(range(VirtualMemory.SIZE)))))

                ram_ind, oldIndex = self.mem_ram.allocatePage(process, rand, cpuProcess=cpuProcess, hadSubstitution=False)
                if oldIndex != -1 and oldIndex != None:
                    self.mem_vm[oldIndex] = [None, 0]

                self.mem_vm[rand][0] = ram_ind
                self.mem_vm[rand][1] = 0

                return rand
            else:
                ref_vm = self.substitutePage(process, cpuProcess)
                ram_ind, oldIndex = self.mem_ram.allocatePage(process, ref_vm, cpuProcess=cpuProcess,
                                                              hadSubstitution=True)
                if oldIndex != -1 and oldIndex != None:
                    self.mem_vm[oldIndex] = [None, 0]

                self.mem_vm[ref_vm][0] = ram_ind
                self.mem_vm[ref_vm][1] = 0

                return ref_vm

        else:
            ram_ind, oldIndex = self.mem_ram.allocatePage(process, ref, cpuProcess=cpuProcess, hadSubstitution=False)

            if oldIndex != -1 and oldIndex != None:
                self.mem_vm[oldIndex] = [None, 0]

            self.mem_vm[ref][0] = ram_ind
            self.mem_vm[ref][1] = 0

            return ref

    def clear(self):
        for ind in range(VirtualMemory.SIZE):
            self.mem_vm[ind] = [None, 0]

class MMU():
    def __init__(self, vm, algorithm, disk):
        self.vm = vm
        self.vm.setAlgorithm(algorithm)
        self.vm.mem_ram.setAlgorithm(algorithm)
        self.disk = disk

    def isAllocated(self, process):
        return self.vm.isAllocated(process)

    def allocatePage(self, process, cpuProcess=None):
        pages = []

        if len(process.pages) != process.numpages:
            ref = self.vm.allocatePage(process, None, cpuProcess)
            pages.append(ref)
        else:
            for ref in process.pages:
                if self.vm.isPageAllocated(process, ref) == False:
                    self.vm.allocatePage(process, ref, cpuProcess)
                    break
        self.disk.remProcess(process, 1)
        return pages

    def referentiate(self, process):
        for ref in process.pages:
            self.vm.mem_vm[ref][1] += 1
            self.vm.mem_ram.queue[self.vm.mem_vm[ref][0]].freq += 1

    def deallocate(self, process):
        self.disk.putProcess(process.id, len(process.pages))
        for ind in range(RAM.SIZE):
            newPage = Page()
            if self.vm.mem_ram.queue[ind].num == process.id:
                self.vm.mem_ram.queue[ind] = newPage

        for ref in process.pages:
            newPage = Page()
            if self.vm.isPageAllocated(process, ref):
                self.vm.mem_ram.queue[self.vm.mem_vm[ref][0]] = newPage
                self.vm.mem_vm[ref] = [None, 0]
