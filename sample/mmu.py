import random

def transform_list(mem, process, mem_vm):
    lista = mem
    if process is None:
        return mem
    for ref in process.pages:
        if mem_vm[ref][0] in lista:
            lista.remove(mem_vm[ref][0])
    return lista


class Page():
    def __init__(self):
        self.num = None
        self.index = None
        self.freq = 0

    def is_allocated(self):
        if self.num is None and self.index is None and self.freq == 0:
            return False
        return True

class RAM():
    SIZE = 50

    def __init__(self, disk, vm):
        self.algorithm = 'FIFO'
        self.queue = []
        for __ in range(RAM.SIZE):
            page = Page()
            self.queue.append(page)
        self.ram_pointer = 0
        self.disk = disk
        self.vm = vm

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm

    def is_allocated(self, page):
        if page.is_allocated():
            return True
        return False

    def has_clear(self):
        for page in self.queue:
            if not page.is_allocated():
                return True
        return False

    def substitute_page(self, process,
                       ind, cpu_process=None, had_substitution=False):
        if self.algorithm == 'FIFO':
            ref_ram = self.ram_pointer
            is_in_ram = (self.queue[ref_ram].num == process.pid)
            is_in_index = (cpu_process and
                           self.queue[ref_ram].index in cpu_process.pages)

            while (is_in_ram or is_in_index):
                self.ram_pointer = (self.ram_pointer + 1) % RAM.SIZE
                ref_ram = self.ram_pointer
                is_in_ram = (self.queue[ref_ram].num == process.pid)
                is_in_index = (cpu_process and
                               self.queue[ref_ram].index in cpu_process.pages)

            if not had_substitution:
                self.disk.put_process(self.queue[ref_ram].num, 1)

            old_index = self.queue[ref_ram].index
            self.queue[ref_ram].num = process.pid
            self.queue[ref_ram].freq = 0
            self.queue[ref_ram].index = ind

            self.ram_pointer = (self.ram_pointer + 1) % RAM.SIZE

            return ref_ram, old_index
        elif self.algorithm == 'LRU':
            range_list = list(range(RAM.SIZE))
            if cpu_process:
                for ref in cpu_process.pages:
                    if self.vm[ref][0] in range_list:
                        range_list.remove(self.vm[ref][0])

            selec_list = []
            for ind in range_list:
                if self.queue[ind].num != process.pid:
                    selec_list.append(ind)
            index = selec_list[0]
            for page in selec_list:
                if self.queue[index].freq > self.queue[page].freq:
                    index = page

            ref_ram = index
            old_index = self.queue[ref_ram].index

            if not had_substitution:
                self.disk.put_process(self.queue[ref_ram].num, 1)

            self.queue[ref_ram].num = process.pid
            self.queue[ref_ram].freq = 0
            self.queue[ref_ram].index = ind
            return ref_ram, old_index

    def allocate_page(self, process,
                     ind, cpu_process=None, had_substitution=False):

        selec_list = transform_list(list(range(RAM.SIZE)), 
                                    cpu_process, self.vm)
        free_list = list(filter(
            lambda page: not self.is_allocated(self.queue[page]), selec_list))
        print(len(free_list))
        print(free_list)
        if free_list:
            rand = random.choice(free_list)
            self.queue[rand].num = process.pid
            self.queue[rand].freq = 0
            self.queue[rand].index = ind
            return rand, -1
        else:
            return self.substitute_page(process, ind,
                                       cpu_process, had_substitution)

    def clear(self):
        for ind in range(RAM.SIZE):
            new_page = Page()
            self.queue[ind] = new_page


class VirtualMemory():
    SIZE = 100

    def __init__(self, disk):
        self.algorithm = 'FIFO'
        self.mem_vm = []
        for __ in range(VirtualMemory.SIZE):
            self.mem_vm.append([None, 0])
        self.mem_ram = RAM(disk, self.mem_vm)
        self.vm_pointer = 0
        self.disk = disk

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm

    def has_clear(self):
        for ref in self.mem_vm:
            if ref[0] is None:
                return True
        return False

    def is_page_allocated(self, process, ref):
        allocated_in_ram = self.mem_ram.is_allocated(
            self.mem_ram.queue[self.mem_vm[ref][0]])
        if self.mem_vm[ref][0] is None:
            return False
        elif self.mem_ram.queue[self.mem_vm[ref][0]].num != process.pid:
            return False
        elif not allocated_in_ram:
            return False
        return True

    def is_allocated(self, process):
        if process.numpages != len(process.pages):
            return False
        for ref in process.pages:
            if self.mem_vm[ref][0] is None:
                return False
            elif self.mem_ram.queue[self.mem_vm[ref][0]].num != process.pid:
                return False
        return True

    def substitute_page(self, process, cpu_process=None):
        ram = self.mem_ram.queue
        if self.algorithm == 'FIFO':
            ind = self.vm_pointer
            in_vm = (ram[self.mem_vm[ind][0]].num == process.pid)
            in_index = (cpu_process and ind in cpu_process.pages)
            while in_vm or in_index:
                self.vm_pointer = (self.vm_pointer + 1) % VirtualMemory.SIZE
                ind = self.vm_pointer
                in_vm = (ram[self.mem_vm[ind][0]].num == process.pid)
                in_index = (cpu_process and ind in cpu_process.pages)

            self.vm_pointer = (self.vm_pointer + 1) % VirtualMemory.SIZE
            self.disk.put_process(
                self.mem_ram.queue[self.mem_vm[ind][0]].num, 1)
            return ind

        elif self.algorithm == 'LRU':

            selec_list = list(filter(
                lambda page:
                    (ram[self.mem_vm[page]].num != process.pid and
                     page not in cpu_process.pages),
                    list(range(VirtualMemory.SIZE))))
            select_pages = list(self.mem_vm[i] for i in selec_list)
            least_freq = min(select_pages,
                            default=select_pages[0],
                            key=lambda x: x[1])
            ind = random.choice(list(filter(
                lambda page: self.mem_vm[page][1] == least_freq[1],
                selec_list)))

            self.disk.put_process(
                self.mem_ram.queue[self.mem_vm[ind][0]].num, 1)
            return ind

    def allocate_page(self, process, ref, cpu_process=None):
        if ref is None:
            if self.has_clear():
                rand = random.choice(list(filter(
                    lambda page:
                        (self.mem_vm[page][0] is None and
                         page not in cpu_process.pages),
                        list(range(VirtualMemory.SIZE)))))

                ram_ind, old_index = self.mem_ram.allocate_page(
                    process, rand, cpu_process=cpu_process,
                    had_substitution=False)
                if old_index != -1 and old_index:
                    self.mem_vm[old_index] = [None, 0]

                self.mem_vm[rand][0] = ram_ind
                self.mem_vm[rand][1] = 0

                return rand
            else:
                ref_vm = self.substitute_page(process, cpu_process)
                ram_ind, old_index = self.mem_ram.allocate_page(
                    process, ref_vm, cpu_process=cpu_process,
                    had_substitution=True)
                if old_index != -1 and old_index:
                    self.mem_vm[old_index] = [None, 0]

                self.mem_vm[ref_vm][0] = ram_ind
                self.mem_vm[ref_vm][1] = 0

                return ref_vm

        else:
            ram_ind, old_index = self.mem_ram.allocate_page(
                process, ref, cpu_process=cpu_process, had_substitution=False)

            if old_index != -1 and old_index:
                self.mem_vm[old_index] = [None, 0]

            self.mem_vm[ref][0] = ram_ind
            self.mem_vm[ref][1] = 0

            return ref

    def clear(self):
        for ind in range(VirtualMemory.SIZE):
            self.mem_vm[ind] = [None, 0]


class MMU():
    def __init__(self, vm, algorithm, disk):
        self.vm = vm
        self.vm.set_algorithm(algorithm)
        self.vm.mem_ram.set_algorithm(algorithm)
        self.disk = disk

    def is_allocated(self, process):
        return self.vm.is_allocated(process)

    def allocate_page(self, process, cpu_process=None):
        pages = []

        if len(process.pages) != process.numpages:
            ref = self.vm.allocate_page(process, None, cpu_process)
            pages.append(ref)
        else:
            for ref in process.pages:
                if self.vm.is_page_allocated(process, ref) == False:
                    self.vm.allocate_page(process, ref, cpu_process)
                    break
        self.disk.remove_process(process, 1)
        return pages

    def referentiate(self, process):
        for ref in process.pages:
            self.vm.mem_vm[ref][1] += 1
            self.vm.mem_ram.queue[self.vm.mem_vm[ref][0]].freq += 1

    def deallocate(self, process):
        self.disk.put_process(process.pid, len(process.pages))
        for ind in range(RAM.SIZE):
            newPage = Page()
            if self.vm.mem_ram.queue[ind].num == process.pid:
                self.vm.mem_ram.queue[ind] = newPage

        for ref in process.pages:
            newPage = Page()
            if self.vm.is_page_allocated(process, ref):
                self.vm.mem_ram.queue[self.vm.mem_vm[ref][0]] = newPage
                self.vm.mem_vm[ref] = [None, 0]
