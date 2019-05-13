class Page():
    def __init__(self, num=0, freq=0):
        self.num = num
        self.freq = freq
        self.isClear = True

    def setClear(self, boolean):
        self.isClear = boolean

    def isClear(self):
        return self.isClear

    def getFreq(self):
        return self.freq

    def resetFreq(self):
        self.freq = 0

    def addFreq(self):
        self.freq += 1

    def getNum(self):
        return self.num

    def setNum(self, n):
        self.num = n

class MMU():
    def __init__(self, algorithm):
        self.algorithm = algorithm

        self.mem_ram = []
        for i in range(50):
            p = Page()
            self.mem_ram.append(p)

        self.pointer = 0

    def incPointer(self):
        self.pointer += 1
        if (self.pointer >= 50):
            self.pointer = 0

    def checkFaultPages(self, process):
        allocatedPages = process.getPages()
        numFault = process.getNumPages()
        length = len(allocatedPages)
        
        for i in range(length):
            if (self.mem_ram[allocatedPages[i].getNum()].isClear() == False and 
                self.mem_ram[allocatedPages[i].getNum()].getNum() == process.getId()):
                numFault -= 1
            else:
                allocatedPages[i].setNum(-1)

        process.setPages(allocatedPages)
        return numFault

    def allocatePages(self, process):
        count = self.checkFaultPages(process)
        pages = process.getPages()
        
        for i in range(len(self.mem_ram)):
            if (count == 0): break
            if (self.mem_ram[i].isClear):
                self.mem_ram[i].setNum(process.getId())
                self.mem_ram[i].addFreq()
                count -= 1
                ind = 0
                while (len(pages) > 0 and pages[ind].getNum() != -1):
                    ind += 1

                pages.insert(ind, self.mem_ram[i])

        if (count > 0): 
            # Quer dizer q toda a memória está ocupada e deve haver substituição
            if (self.algorithm == 'LRU'):
                leastIndex = 0
                leastFreq = self.mem_ram[0].getFreq()
                for j in range(len(self.mem_ram)):
                    if self.mem_ram[j].getFreq() < leastFreq:
                        leastFreq = self.mem_ram[j].getFreq()
                        leastIndex = j
                for i in range(count):
                    self.mem_ram[leastIndex].setNum(process.getId())
                    self.mem_ram[leastIndex].resetFreq()
                    self.mem_ram[leastIndex].addFreq(1)
                    
                    ind = 0
                    while (len(pages) > 0 and pages[ind].getNum() != -1):
                        ind += 1

                    pages.insert(ind, self.mem_ram[leastIndex])
            elif (self.algorithm == 'FIFO'):
                for i in range(count):
                    while (self.mem_ram[self.pointer].getNum() == process.getId()):
                        incPointer()
                    
                    self.mem_ram[self.pointer].setNum(process.getId())
                    self.mem_ram[self.pointer].resetFreq()
                    self.mem_ram[self.pointer].addFreq(1)

                    ind = 0
                    while (len(pages) > 0 and pages[ind].getNum() != -1):
                        ind += 1
                    pages.insert(ind, self.mem_ram[self.pointer])

                    incPointer()

        process.setPages(pages)

    def deallocatePages(self, process):
        for i in range(len(self.mem_ram)):
            page = self.mem_ram[i]
            if (page.isClear() == False and page.getNum() == process.getId()):
                page.setClear(True)
                page.setNum(0)
                page.resetFreq()
        process.setPages([])
