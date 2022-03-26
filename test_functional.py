import sys
from unittest import TestCase
from unittest.mock import MagicMock

from PyQt5 import QtCore
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication

from facade import Facade
from gui import MainWindow, InsertWidget


class FunctionalTest(TestCase):
    def setUp(self):
        self.qapp = QApplication(sys.argv)
        name = 'DB_test.db'
        self.facade = Facade(name)
        self.window = MainWindow(self.facade)

    # def test_push(self):
    #     btn_open_add = self.window.ui.btn_open_add
    #     QTest.mouseClick(btn_open_add, QtCore.Qt.MouseButton.LeftButton)
    #     for window in self.qapp.topLevelWidgets():
    #         if isinstance(window, InsertWidget):
    #             dialog = window
    #             break
    #         else:
    #             self.fail()
    #
    #     dialog.key_input.setValue(10)
    #     dialog.data_input.setText("1234")         # записываем данные в поля
    #     QTest.mouseClick(dialog.btn_insert, QtCore.Qt.MouseButton.LeftButton)

    def test_pop(self):


        btn_pop = self.window.ui.btn_delete
        self.facade.push([1, 2], 4)
        self.facade.pop = MagicMock()
        QTest.mouseClick(btn_pop, QtCore.Qt.MouseButton.LeftButton)
        QTest.mouseClick(btn_pop, QtCore.Qt.MouseButton.LeftButton)
        #self.facade.pop.assert_called_with([1, 2], 4])


if __name__ == '__main__':
    pass


