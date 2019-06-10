
import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QIcon
from process import Process
from WProcess import Window_Process
from escalonator import Escalonator
from process import Process
from ioqueue import IO
from cpu import CPU
from disk import Disk
from mmu import MMU, VirtualMemory
import random
import time
from Gantt import Window_Gantt


class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.idProcess = 1
        self.process = None
        self.listProcess = []

        self.setWindowIcon(QIcon('computer.png'))

        self.setGeometry(300, 300, 900, 400)
        self.setWindowTitle('OS SIMULATOR')
        self.show()

        self.statusBar()

        openFile = QAction(QIcon('openThing.png'), '&Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open File')
        openFile.triggered.connect(self.file_open)

        saveFile = QAction(QIcon('saveThing.png'), '&Save', self)
        saveFile.setShortcut("Ctrl+S")
        saveFile.setStatusTip('Save File')
        saveFile.triggered.connect(self.file_save)

        addProcess = QAction(QIcon('newThing.png'), '&NewProcess', self)
        addProcess.setShortcut('Ctrl+N')
        addProcess.setStatusTip('New Process')
        addProcess.triggered.connect(self.new_Process)

        self.comboCPU = QComboBox()
        self.comboCPU.addItem("FCFS")
        self.comboCPU.addItem("SJF")
        self.comboCPU.addItem("RR")
        self.comboCPU.addItem("EDF")
        self.comboCPU.addItem("SPN")
        self.comboCPU.addItem("PRIO")
        self.comboCPU.addItem("LOT")

        self.comboMem = QComboBox()
        self.comboMem.addItem("FIFO")
        self.comboMem.addItem("LRU")

        linhaCPU = QLabel()
        linhaCPU.setText("Scheduling Algorithm")

        linhaMem = QLabel()
        linhaMem.setText("Paging Algorithm")

        layoutC = QGridLayout()
        layoutC.addWidget(linhaCPU)
        layoutC.addWidget(self.comboCPU)

        layoutM = QGridLayout()
        layoutM.addWidget(linhaMem)
        layoutM.addWidget(self.comboMem)

        self.override_sp = QSpinBox()

        self.quantum_sp = QSpinBox()
        self.quantum_sp.setMinimum(1)

        quantum_label = QLabel()
        quantum_label.setText("Quantum Time")

        override_label = QLabel()
        override_label.setText("Override Time")

        QuantumLayout = QGridLayout()
        QuantumLayout.addWidget(quantum_label)
        QuantumLayout.addWidget(self.quantum_sp)

        OverrideLayout = QGridLayout()
        OverrideLayout.addWidget(override_label)
        OverrideLayout.addWidget(self.override_sp)

        selectC = QWidget()
        selectC.setLayout(layoutC)

        selectM = QWidget()
        selectM.setLayout(layoutM)

        Quantum = QWidget()
        Quantum.setLayout(QuantumLayout)

        Override = QWidget()
        Override.setLayout(OverrideLayout)

        Run = QAction(QIcon('run.png'), '&Run', self)
        Run.triggered.connect(self.run)

        self.toolbar = self.addToolBar('Process')
        self.toolbar.addAction(addProcess)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(selectC)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(selectM)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(Quantum)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(Override)
        self.toolbar.addAction(Run)

        self.path = os.path.abspath("Interface.py")


        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)


    def run(self):
        if self.listProcess == []:
            reply = QMessageBox.information(self, 'NO PROCESSES', "Insert Processes to Run", QMessageBox.Ok)
            return
        self.file_open(True)

        self.quantum = self.quantum_sp.value()
        self.override = self.override_sp.value()
        self.type = self.comboCPU.currentText()
        self.typeMMU = self.comboMem.currentText()
        escalonator = Escalonator(self.type.upper(), self.override)
        self.processes = self.listProcess
        disk = Disk()
        vm = VirtualMemory(100, disk)
        mmu = MMU(vm, self.typeMMU.upper(), disk)
        io = IO(mmu, disk)
        io.escalonator = escalonator
        cpu = CPU(escalonator, mmu, io, self.quantum, disk=disk)
        escalonator.cpu = cpu
        n = len(self.processes)
        for i in self.processes:
            i.io = io
            escalonator.insertProcess(i)
            disk.insertProcess(i.id, i.numpages)

        escalonator.not_arrived.sort(key=lambda x: x.start)
        escalonator.queue()
        self.hide()
        self.gantt = Window_Gantt(n, cpu, escalonator, io, self.processes, self)

    def file_save(self, auto=False):
        if not auto:
            name = QFileDialog.getSaveFileName(self, 'Save File')
        else:
            name = "('" + self.path[:-12] + 'autosave' + "', " + "'All Files (*)')"

        if name[0]:


            file = open(name[0], 'w')
            with file:
                for i in self.listProcess:
                    file.write(str(i.id) + ' ' + str(i.start) + ' ' + str(i.execution_time) + ' ' + str(
                        i.numpages) + ' ' + str(i.deadline) + ' ' +
                               "None" + ' ' + str(i.need_io) + ' ' + str(i.priority) + '\n')

    def file_open(self, auto=False):
        if not auto:
            fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        else:
            fname = "('" + self.path[:-12] + 'autosave' + "', " + "'All Files (*)')"

        self.listProcess = []

        if fname[0]:
            f = open(fname[0], 'r')
            with f:
                data = f.read().split('\n')
                index = 0
                for a in data:
                    if a == '':
                        break
                    i = a.split(' ')

                    processo = Process(int(i[0]), int(i[1]), int(i[2]), int(i[3]), int(i[4]))
                    if i[6] == "True":
                        processo.need_io = True
                    else:
                        processo.need_io = False
                    processo.priority = int(i[7])
                    self.listProcess.append(processo)
            self.printProcesses()

    def new_Process(self):

        self.processAux = Window_Process(self.idProcess, self.process, self)
        self.processAux.exec_()
        self.process = self.processAux.process
        if self.process:
            self.listProcess.append(self.process)
            self.idProcess += 1
        self.printProcesses()

    def editProcess(self):
        sender = self.sender()
        index = int(sender.text().split(' ')[1])
        self.processAux = Window_Process(index, self.process, self)
        self.processAux.exec_()
        process = self.processAux.process
        if process:
            self.listProcess[index - 1] = process
            self.printProcesses()

    def removeProcess(self):
        sender = self.sender()
        index = int(sender.text().split(' ')[1])
        reply = QMessageBox.question(self, 'Remove',
                                     "Are you sure to remove ? ", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            self.listProcess.pop(index - 1)
            if not self.listProcess:
                self.idProcess = 1
            self.printProcesses()

    def printProcesses(self):
        self.lista = QTabWidget()
        self.numberTab = 1
        self.file_save(True)
        for i in self.listProcess:
            self.janela = QWidget()
            self.lista.addTab(self.janela, "Processo " + str(i.id))
            self.janelaUi(i)
            self.numberTab += 1

        self.setCentralWidget(self.lista)

    def janelaUi(self, processo):
        layout = QFormLayout()
        linhaStart = QLabel()
        linhaStart.setText(str(processo.start))
        layout.addRow("StartTime", linhaStart)

        linhaExec = QLabel()
        linhaExec.setText(str(processo.execution_time))
        layout.addRow("Execution Time", linhaExec)

        linhaDeadLine = QLabel()
        linhaDeadLine.setText(str(processo.deadline))
        layout.addRow("DeadLine Time", linhaDeadLine)

        linhaPriority = QLabel()
        linhaPriority.setText(str(processo.priority))
        layout.addRow("Priority", linhaPriority)

        linhaPages = QLabel()
        linhaPages.setText(str(processo.numpages))
        layout.addRow("Pages", linhaPages)

        btnEdit = QPushButton('Edit ' + str(self.numberTab) + ' ' + '° Process', self.janela)
        btnRemove = QPushButton('Remove ' + str(self.numberTab) + ' ' + '° Process', self.janela)

        btnEdit.clicked.connect(self.editProcess)
        btnRemove.clicked.connect(self.removeProcess)

        layout.addRow(btnEdit)
        layout.addRow(btnRemove)

        self.lista.setTabText(self.numberTab, "Process " + str(processo.id))
        self.janela.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main_Window()
    sys.exit(app.exec_())
