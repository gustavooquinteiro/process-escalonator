sys.path.append("../sample")
from InterFace import Main_Window
from process import Process
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import unittest
import sys


class TestApp(unittest.TestCase):
    """docstring for TestApp."""

    def setUp(self, interface=QApplication(sys.argv), file="test0.txt"):
        self.interface = Main_Window()
        with open(file, 'r') as target:
            lines = target.read().split('\n')
            for line in lines:
                if not line:
                    break
                params = line.split(' ')
                processo = Process(int(params[0]), int(params[1]),
                                   int(params[2]), int(params[3]),
                                   int(params[4]), int(params[5]))
                self.interface.listProcess.append(processo)

    def test_RR_FIFO(self):
        self.interface.quantum_sp.setValue(2)
        self.interface.override_sp.setValue(1)
        self.interface.comboCPU.setCurrentText("RR")
        self.interface.comboMem.setCurrentText("FIFO")
        self.interface.run()
        self.interface.gantt.hide()
        self.interface.gantt.AutoTickQuant.setValue(1)
        self.interface.gantt.checkAutoTick.setChecked(True)
        result = round(self.interface.gantt.info["TURNAROUND"], 0)
        self.assertEqual(result, 33.0)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(
        unittest.TestLoader().loadTestsFromTestCase(TestApp)
    )
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
