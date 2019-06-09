import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QLayout, QGridLayout, QHBoxLayout,
                             QInputDialog,QFrame, QColorDialog, QApplication, QFontDialog, QMessageBox,
                             QSizePolicy,QDialog,  QLabel, QTextEdit, QAction, QFileDialog, QMainWindow, QVBoxLayout, QSpinBox)
from PyQt5.QtGui import QColor, QIcon
from process import Process

class Window_Process(QDialog):
    def __init__(self, id, process, parent):
        super().__init__(parent)

        self.id = id
        self.startTime = 0
        self.executionTime = 1
        self.deadlineTime = 1
        self.priorityTime = 0
        self.pagesNumber = 1
        self.process = process

        self.setWindowIcon(QIcon('feature.png'))

        layout = QGridLayout()

        self.start = QLabel("Start Time")
        self.start.setAlignment(Qt.AlignCenter)
        self.start_sp = QSpinBox()

        self.execution = QLabel("Execution Time")
        self.execution.setAlignment(Qt.AlignCenter)
        self.execution_sp = QSpinBox()
        self.execution_sp.setMinimum(1)

        self.deadline = QLabel("DeadLine Time")
        self.deadline.setAlignment(Qt.AlignCenter)
        self.deadline_sp = QSpinBox()
        self.deadline_sp.setMinimum(self.executionTime)

        self.priority = QLabel("Priority")
        self.priority.setAlignment(Qt.AlignCenter)
        self.priority_sp = QSpinBox()

        self.pages = QLabel("Pages")
        self.pages.setAlignment(Qt.AlignCenter)
        self.pages_sp = QSpinBox()
        self.pages_sp.setMaximum(10)
        self.pages_sp.setMinimum(1)

        self.btnOK = QPushButton('Create', self)
        self.btnOK.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.btnCancel = QPushButton('Cancel', self)
        self.btnCancel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        layoutBtn = QHBoxLayout()
        layoutBtn.addWidget(self.btnOK)
        layoutBtn.addWidget(self.btnCancel)

        layout.addWidget(self.start)
        layout.addWidget(self.start_sp)
        layout.addWidget(self.execution)
        layout.addWidget(self.execution_sp)
        layout.addWidget(self.deadline)
        layout.addWidget(self.deadline_sp)
        layout.addWidget(self.priority)
        layout.addWidget(self.priority_sp)
        layout.addWidget(self.pages)
        layout.addWidget(self.pages_sp)
        layout.addItem(layoutBtn)


        self.start_sp.valueChanged.connect(self.startvalue)
        self.execution_sp.valueChanged.connect(self.executionvalue)
        self.deadline_sp.valueChanged.connect(self.deadlinevalue)
        self.priority_sp.valueChanged.connect(self.priorityvalue)
        self.pages_sp.valueChanged.connect(self.pagesvalue)
        self.btnOK.clicked.connect(self.createProcess)
        self.btnCancel.clicked.connect(self.cancelProcess)


        self.setLayout(layout)
        self.setWindowTitle("Process "+ str(id))


    def startvalue(self):
        self.start.setText("Start Value : " + str(self.start_sp.value()))
        self.startTime = self.start_sp.value()

    def executionvalue(self):
        self.execution.setText("Execution Value : " + str(self.execution_sp.value()))
        self.executionTime = self.execution_sp.value()
        if self.deadlineTime < self.executionTime :
            self.deadline_sp.setValue(self.executionTime)
        self.deadline_sp.setMinimum(self.executionTime)

    def deadlinevalue(self):
        self.deadline.setText("Deadline Value : " + str(self.deadline_sp.value()))
        self.deadlineTime = self.deadline_sp.value()

    def priorityvalue(self):
        self.priority.setText("Priority Value : " + str(self.priority_sp.value()))
        self.priorityTime = self.priority_sp.value()

    def pagesvalue(self):
        self.pages.setText("Pages : " + str(self.pages_sp.value()))
        self.pagesNumber = self.pages_sp.value()

    def createProcess(self):
        reply = QMessageBox.question(self, 'Create',
                                     "Are you sure to create ? ", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            self.process = Process(self.id, self.startTime, self.executionTime,self.pagesNumber, self.deadlineTime, priority=self.priorityTime)

            self.close()


    def cancelProcess(self):
        reply = QMessageBox.question(self, 'Cancel',
                                     "Are you sure to cancel ? ", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.process = None
            self.close()


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = Window_Process(1)
#     sys.exit(app.exec_())