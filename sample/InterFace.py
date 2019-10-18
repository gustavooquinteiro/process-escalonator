import platform
from PySide2 import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from process import Process
from WProcess import Window_Process
from escalonator import Escalonator
from ioqueue import IO
from cpu import CPU
from disk import Disk
from mmu import MMU, VirtualMemory
from Gantt import Window_Gantt
from pathlib import Path
import sys
import os



class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.idProcess = 1
        self.process = None
        self.listProcess = []
        if sys.version_info.minor >= 6:
            images = Path("sample/images/")
        else:
            images = "sample/images/"
        icon = os.path.join(images, "computer.png")

        self.setWindowIcon(QIcon(icon))

        self.setGeometry(300, 300, 900, 400)
        self.setWindowTitle('OS SIMULATOR')
        self.show()

        self.statusBar()
        open_icon = os.path.join(images, "openThing.jpg")

        openFile = QAction(QIcon(open_icon), '&Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open File')
        openFile.triggered.connect(self.file_open)

        save_icon = os.path.join(images, "saveThing.jpg")
        saveFile = QAction(QIcon(save_icon), '&Save', self)
        saveFile.setShortcut("Ctrl+S")
        saveFile.setStatusTip('Save File')
        saveFile.triggered.connect(self.file_save)
        new_icon = os.path.join(images, "newThing.png")
        addProcess = QAction(QIcon(new_icon), '&NewProcess', self)
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
        self.comboCPU.addItem("MLF")

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
        run_icon = os.path.join(images, "run.png")
        Run = QAction(QIcon(run_icon), '&Run', self)
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
        if not self.listProcess:
            QMessageBox.information(self,
                                    'NO PROCESSES',
                                    "Insert Processes to Run",
                                    QMessageBox.Ok)
            return
        #self.file_open(True)
        self.quantum = self.quantum_sp.value()
        self.override = self.override_sp.value()
        self.type = self.comboCPU.currentText()
        self.typeMMU = self.comboMem.currentText()
        escalonator = Escalonator(self.type.upper(), self.override)
        self.processes = self.listProcess
        disk = Disk()
        vm = VirtualMemory(disk)
        mmu = MMU(vm, self.typeMMU.upper(), disk)
        io = IO(mmu, disk)
        io.escalonator = escalonator
        cpu = CPU(escalonator, mmu, io, self.quantum, disk=disk)
        escalonator.cpu = cpu
        n = len(self.processes)
        for i in self.processes:
            escalonator.insert_process(i)
            disk.insert_process(i.pid, i.numpages)

        escalonator.not_arrived.sort(key=lambda x: x.start)
        escalonator.queue()
        self.hide()
        self.gantt = Window_Gantt(n, cpu, escalonator,
                                  io, self.processes, self)

    def file_save(self, auto=False):
        if not auto:
            name = QFileDialog.getSaveFileName(self, 'Save File')
        else:
            name = "('" + self.path[:-12] + \
                'autosave' + "', " + "'All Files (*)')"

        if name[0]:
            with open(name[0], 'w') as file:
                for i in self.listProcess:
                    file.write("{} {} {} {} {} {}\n"
                               .format(i.pid, i.start, i.execution_time,
                                       i.numpages, i.deadline,
                                       i.priority))

    def file_open(self, auto=False):
        if not auto:
            fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        else:
            fname = "('" + self.path[:-12] + \
                'autosave' + "', " + "'All Files (*)')"

        self.listProcess = []

        if fname[0]:
            with open(fname[0], 'r') as f:
                data = f.read().split('\n')
                for a in data:
                    if a == '':
                        break
                    i = a.split(' ')
                    processo = Process(int(i[0]), int(i[1]),
                                       int(i[2]), int(i[3]),
                                       int(i[4]), int(i[5]))
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
                                     "Are you sure to remove ? ",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.Yes)
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
            self.lista.addTab(self.janela, "Processo {} " .format(i.pid))
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

        btnEdit = QPushButton('Edit {} ° Process'
                              .format(self.numberTab),
                              self.janela)
        btnRemove = QPushButton('Remove {} ° Process'
                                .format(self.numberTab),
                                self.janela)
        btnEdit.clicked.connect(self.editProcess)
        btnRemove.clicked.connect(self.removeProcess)
        layout.addRow(btnEdit)
        layout.addRow(btnRemove)
        self.lista.setTabText(self.numberTab,
                              "Process {}" .format(processo.pid))
        self.janela.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main_Window()
    sys.exit(app.exec_())
