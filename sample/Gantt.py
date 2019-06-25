from PyQt5 import QtTest
from PyQt5.QtCore import Qt, QTime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QIcon
from pathlib import Path
import os
import sys


class Window_Gantt(QWidget):
    def __init__(self, n, cpu, escalonator, io, processes, SOWindow):
        super().__init__()
        self.timer = QTime()
        self.SO = SOWindow
        self.tickClock = 0
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(processes))
        self.tableWidget.setColumnCount(1)

        nameMem = QTableWidgetItem()
        nameMem.setText("RAM")

        nameDisk = QTableWidgetItem()
        nameDisk.setText("Disk")

        self.tableMem = QTableWidget()
        self.tableMem.setRowCount(50)
        self.tableMem.setColumnCount(1)
        self.tableMem.setHorizontalHeaderItem(0, nameMem)
        self.tableMem.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.tableDisk = QTableWidget()
        self.tableDisk.setRowCount(len(cpu.disk.memory))
        self.tableDisk.setColumnCount(1)
        self.tableDisk.setHorizontalHeaderItem(0, nameDisk)
        self.tableDisk.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.dicionary = {}
        index = 0
        for i in processes:
            self.dicionary[i.pid] = index
            index += 1

        self.setWindowTitle("Gantt Processes")
        self.layout = QVBoxLayout()
        self.tickRun = QPushButton("Tick", self)
        self.tickRun.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.layout2 = QHBoxLayout()
        self.tickRun.clicked.connect(self.tick)
        self.ticksQuant = QSpinBox()
        self.ticksQuant.setMinimum(1)
        self.ticksQuant.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.AutoTickQuant = QSpinBox()
        self.AutoTickQuant.setMinimum(1)
        self.AutoTickQuant.setMaximum(2000)
        self.AutoTickQuant.setValue(1000)
        self.AutoTickQuant.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.checkAutoTick = QCheckBox("Auto Tick")
        self.checkAutoTick.setChecked(False)
        self.checkAutoTick.stateChanged.connect(self.autoTick)
        self.checkAutoTick.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.info = {
            "CPU Scheduler": self.SO.type,
            "Pagination Algorithm": self.SO.typeMMU,
            "Quantum": self.SO.quantum,
            "Override": self.SO.override
            }

        labels = []
        for x, y in self.info.items():
            labels.append("{}: {}\n" .format(x, y))
        label = ''.join(labels)
        self.Info = QLabel(label)

        self.Info.setStyleSheet("color: red;")
        self.Info.setAlignment(Qt.AlignCenter)

        self.layout3 = QVBoxLayout()
        labelCheck = QLabel("Mark to Run Automatic")
        self.layout3.addWidget(labelCheck)
        self.layout3.addWidget(self.checkAutoTick)
        C = QWidget()
        C.setLayout(self.layout3)
        self.layout2.addWidget(C)

        self.layout3 = QVBoxLayout()
        labelCheck = QLabel("Time in ms to AutoRun")
        self.layout3.addWidget(labelCheck)
        self.layout3.addWidget(self.AutoTickQuant)
        D = QWidget()
        D.setLayout(self.layout3)
        self.layout2.addWidget(D)

        self.layout3 = QVBoxLayout()
        self.labelCheck1 = QLabel("Click to Run {} ticks"
                                  .format(self.ticksQuant.value()))
        self.layout3.addWidget(self.labelCheck1)
        self.layout3.addWidget(self.tickRun)
        E = QWidget()
        E.setLayout(self.layout3)
        self.layout2.addWidget(E)

        self.layout3 = QVBoxLayout()
        labelCheck = QLabel("Ticks to Run")
        self.layout3.addWidget(labelCheck)
        self.layout3.addWidget(self.ticksQuant)
        self.ticksQuant.valueChanged.connect(self.ticksQuantUpdate)
        F = QWidget()
        F.setLayout(self.layout3)
        self.layout2.addWidget(F)

        A = QWidget()
        A.setLayout(self.layout2)
        self.layout.addWidget(self.Info)
        self.layout.addWidget(A)
        layoutTables = QHBoxLayout()
        layoutTables.addWidget(self.tableWidget)
        layoutTables.addWidget(self.tableMem)
        layoutTables.addWidget(self.tableDisk)
        B = QWidget()
        B.setLayout(layoutTables)
        self.layout.addWidget(B)
        self.LastLabel = QLabel("Running")
        G = QWidget()
        layoutLegenda = QHBoxLayout()
        tableLegenda = QTableWidget()
        tableLegenda.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        tableLegenda.setRowCount(1)
        tableLegenda.setColumnCount(7)

        teste = QTableWidgetItem()
        teste.setText("in IO list")
        tableLegenda.setItem(0, 0, QTableWidgetItem())
        tableLegenda.item(0, 0).setBackground(QColor(139, 0, 0))
        tableLegenda.item(0, 0).setFlags(Qt.NoItemFlags)
        tableLegenda.setHorizontalHeaderItem(0, teste)

        teste1 = QTableWidgetItem()
        teste1.setText("Override")
        tableLegenda.setItem(0, 1, QTableWidgetItem())
        tableLegenda.item(0, 1).setBackground(Qt.red)
        tableLegenda.item(0, 1).setFlags(Qt.NoItemFlags)
        tableLegenda.setHorizontalHeaderItem(1, teste1)

        teste2 = QTableWidgetItem()
        teste2.setText("Executing")
        tableLegenda.setItem(0, 2, QTableWidgetItem())
        tableLegenda.item(0, 2).setBackground(Qt.green)
        tableLegenda.item(0, 2).setFlags(Qt.NoItemFlags)
        tableLegenda.setHorizontalHeaderItem(2, teste2)

        teste3 = QTableWidgetItem()
        teste3.setText("Executing, dead")
        tableLegenda.setItem(0, 3, QTableWidgetItem())
        tableLegenda.item(0, 3).setBackground(QColor(0, 100, 0))
        tableLegenda.item(0, 3).setFlags(Qt.NoItemFlags)
        tableLegenda.setHorizontalHeaderItem(3, teste3)

        teste4 = QTableWidgetItem()
        teste4.setText("in Ready")
        tableLegenda.setItem(0, 4, QTableWidgetItem())
        tableLegenda.item(0, 4).setBackground(Qt.yellow)
        tableLegenda.item(0, 4).setFlags(Qt.NoItemFlags)
        tableLegenda.setHorizontalHeaderItem(4, teste4)

        teste5 = QTableWidgetItem()
        teste5.setText("in Ready, dead")
        tableLegenda.setItem(0, 5, QTableWidgetItem())
        tableLegenda.item(0, 5).setBackground(QColor(189, 183, 107))
        tableLegenda.item(0, 5).setFlags(Qt.NoItemFlags)
        tableLegenda.setHorizontalHeaderItem(5, teste5)

        teste6 = QTableWidgetItem()
        teste6.setText("Not Started/ Finished")
        tableLegenda.setItem(0, 6, QTableWidgetItem())
        tableLegenda.item(0, 6).setBackground(Qt.gray)
        tableLegenda.item(0, 6).setFlags(Qt.NoItemFlags)
        tableLegenda.setColumnWidth(6, 240)
        tableLegenda.setHorizontalHeaderItem(6, teste6)

        self.tableDisk.setColumnWidth(0, 100)
        self.tableDisk.setFixedWidth(180)
        self.tableMem.setColumnWidth(0, 100)
        self.tableMem.setFixedWidth(180)

        layoutLegenda.addWidget(tableLegenda)
        G.setLayout(layoutLegenda)
        self.layout.addWidget(G)
        self.layout.addWidget(self.LastLabel)
        self.setGeometry(300, 300, 1400, 1000)
        self.setLayout(self.layout)
        if sys.version_info.minor >= 6:
            images = Path("sample/images/")
        else:
            images = "sample/images/"
        edit_image = os.path.join(images, "edit-image.png")
        self.setWindowIcon(QIcon(edit_image))
        self.show()

        self.cpu = cpu
        self.escalonator = escalonator
        self.io = io
        self.n = n

    def ticksQuantUpdate(self):
        self.labelCheck1.setText("Click to Run {} ticks"
                                 .format(self.ticksQuant.value()))

    def updategantt(self, tick, escalonator, io, cpu):
        for i in range(self.tableWidget.rowCount()):
            self.tableWidget.setItem(i, tick, QTableWidgetItem())
            self.tableWidget.item(i, tick,).setBackground(Qt.gray)
            self.tableWidget.item(i, tick).setFlags(Qt.NoItemFlags)

        for i in escalonator.ready_queue:
            if escalonator.real_time_over(i):
                self.tableWidget.setItem(self.dicionary[i.pid],
                                         tick,
                                         QTableWidgetItem())
                self.tableWidget.item(self.dicionary[i.pid],
                                      tick).setBackground(
                                          QColor(189, 183, 107))
                self.tableWidget.item(self.dicionary[i.pid],
                                      tick).setFlags(Qt.NoItemFlags)
            else:
                self.tableWidget.setItem(self.dicionary[i.pid],
                                         tick,
                                         QTableWidgetItem())
                self.tableWidget.item(self.dicionary[i.pid],
                                      tick).setBackground(Qt.yellow)
                self.tableWidget.item(self.dicionary[i.pid],
                                      tick).setFlags(Qt.NoItemFlags)

        for i in io.queue:
            self.tableWidget.setItem(self.dicionary[i.pid],
                                     tick,
                                     QTableWidgetItem())
            self.tableWidget.item(self.dicionary[i.pid],
                                  tick).setBackground(QColor(139, 0, 0))
            self.tableWidget.item(self.dicionary[i.pid],
                                  tick).setFlags(Qt.NoItemFlags)

        executing_states = ["Executando", "PreSobrecarga", "Pronto"]
        override_states = ["PosSobrecarga", "Sobrecarga"]

        if cpu.state in executing_states:
            if escalonator.real_time_over(cpu.process):
                self.tableWidget.setItem(self.dicionary[cpu.process.pid],
                                         tick,
                                         QTableWidgetItem())
                self.tableWidget.item(self.dicionary[cpu.process.pid],
                                      tick).setBackground(QColor(0, 100, 0))
                self.tableWidget.item(self.dicionary[cpu.process.pid],
                                      tick).setFlags(Qt.NoItemFlags)
            else:
                self.tableWidget.setItem(self.dicionary[cpu.process.pid],
                                         tick,
                                         QTableWidgetItem())
                self.tableWidget.item(self.dicionary[cpu.process.pid],
                                      tick).setBackground(Qt.green)
                self.tableWidget.item(self.dicionary[cpu.process.pid],
                                      tick).setFlags(Qt.NoItemFlags)

        if cpu.state in override_states:
            self.tableWidget.setItem(self.dicionary[cpu.process.pid],
                                     tick,
                                     QTableWidgetItem())
            self.tableWidget.item(self.dicionary[cpu.process.pid],
                                  tick).setBackground(Qt.red)
            self.tableWidget.item(self.dicionary[cpu.process.pid],
                                  tick).setFlags(Qt.NoItemFlags)

        if self.n != len(self.cpu.concluded_process_time):
            self.tableWidget.setColumnCount(
                self.tableWidget.columnCount() + 1)

    def updateMem(self):

        index = 0
        for i in self.cpu.mmu.vm.mem_ram.queue:
            if self.cpu.mmu.vm.mem_ram.is_allocated(i):
                self.tableMem.setItem(index, 0, QTableWidgetItem())
                self.tableMem.item(index,
                                   0).setBackground(QColor(30, 144, 255))
                self.tableMem.item(index, 0).setForeground(Qt.yellow)
                self.tableMem.item(index, 0).setTextAlignment(Qt.AlignHCenter)
                self.tableMem.item(index, 0).setText(str(i.num))
                self.tableMem.item(index, 0).setFlags(Qt.NoItemFlags)
            else:
                self.tableMem.setItem(index, 0, QTableWidgetItem())
                self.tableMem.item(index, 0).setBackground(Qt.gray)
                self.tableMem.item(index, 0).setFlags(Qt.NoItemFlags)
            index += 1

    def updateDisk(self):
        index = 0

        for i in self.cpu.disk.memory:
            if i.is_allocated:
                self.tableDisk.setItem(index, 0, QTableWidgetItem())
                self.tableDisk.item(index,
                                    0).setBackground(QColor(30, 144, 255))
                self.tableDisk.item(index, 0).setForeground(Qt.yellow)
                self.tableDisk.item(index,
                                    0).setTextAlignment(Qt.AlignHCenter)
                self.tableDisk.item(index, 0).setText(str(i.proc_id))
                self.tableDisk.item(index, 0).setFlags(Qt.NoItemFlags)
            else:
                self.tableDisk.setItem(index, 0, QTableWidgetItem())
                self.tableDisk.item(index, 0).setBackground(Qt.gray)
                self.tableDisk.item(index, 0).setFlags(Qt.NoItemFlags)
            index += 1

    def tick(self):
        if self.n == len(self.cpu.concluded_process_time):
            self.cpu.mmu.vm.mem_ram.clear()
            self.cpu.mmu.vm.clear()
            if self.ticksQuant.value() > 1:
                self.ticksQuant.setValue(1)
            self.checkAutoTick.setChecked(False)
            turnaround = sum(self.cpu.concluded_process_time) / self.n
            self.LastLabel.setText("TURNAROUND: {:.2f} " .format(turnaround))
            self.info["TURNAROUND"] = turnaround
            labels = []
            for x, y in self.info.items():
                if x == "TURNAROUND":
                    labels.append("{}: {:.2f}\n" .format(x, round(y, 0)))
                else:
                    labels.append("{}: {}\n" .format(x, y))
            text = ''.join(labels)
#            QMessageBox.information(self,
#                                    'FINISHED',
#                                    text,
#                                    QMessageBox.Ok)                        
            return
        self.escalonator.next_process()
        self.io.wait_for_resource(self.cpu)
        self.cpu.run_clock()

        self.updategantt(self.cpu.clock, self.escalonator, self.io, self.cpu)
        self.updateMem()
        self.updateDisk()
        print(self.cpu.clock)
        self.cpu.clock += 1
        self.tickClock = self.cpu.clock

        if self.ticksQuant.value() > 1:
            self.ticksQuant.setValue(self.ticksQuant.value() - 1)
            self.tick()

    def autoTick(self):
        while self.checkAutoTick.isChecked():
            self.tick()
            QtTest.QTest.qWait(self.AutoTickQuant.value())

    def closeEvent(self, e):
        self.SO.show()
        self.close()
