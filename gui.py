import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from facade import Facade

import logging

logging.basicConfig(level=logging.INFO)
# logging.disable(logging.INFO)

class MainWindow(QMainWindow):
    """
    Класс создания главного окна.
    """
    def __init__(self, facade):
        """
        Загрузка основного окна, прикрепление действий к кнопкам (вызов функций) и отображение последней версии стека в listWidget.
        """
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi('forms/MainWindow.ui', self)
        self.facade = facade
        self.list = []
        self.strin = '123'
        self.btn_open_add.clicked.connect(lambda: self.add_elem())
        self.btn_delete.clicked.connect(lambda: self.delete_elem())
        self.btn_delete_all.clicked.connect(lambda: self.DialogDelAll())
        self.comboBox.addItems(self.facade.get_id())
        self.build()
        self.comboBox.currentIndexChanged.connect(lambda: self.select())
        logging.log(logging.INFO, 'Приложение запущено')

    def select(self):
        """
        Функция выбора версии через comboBox для просмотра на listWidget.
        :return: None
        """
        id = self.comboBox.currentText()
        self.list = str(self.facade.get_select(id))
        self.build_select()
        logging.log(logging.INFO, 'Выбрана версия ' + id)

    def delete_elem(self):
        """
        Функция удаления элемента через графический интерфейс.
        :return: None
        """
        self.current = []
        if self.list != None:
            nums = self.list[0][1:-1].split(',')
            if nums != ['']:
                for num in nums:
                    self.current.append(int(num))

        if type(self.current) == type(self.strin):
            self.current = [self.current]

        if self.current != None:
            if self.current == []:
                self.DialogDel()
                logging.log(logging.INFO, 'Стек уже пуст!')
            else:
                self.facade.pop(self.current)
                self.build_CB()
                self.build()
                logging.log(logging.INFO, 'Последний элемент удалён!')

    def add_elem(self):
        """
        Функция открытия окна добавления элемента.
        :return: None
        """
        self.ui = InsertWidget(self.facade, self)
        self.ui.show()
        logging.log(logging.INFO, 'Открыто окно "Добавление элемента"')

    def delete_all(self, button):
        if button.text() == "OK":
            self.facade.delete_all()
            self.build_CB()
            self.build()
            logging.log(logging.INFO, 'Данные удалены')
        else:
            logging.log(logging.INFO, 'Данные не удалены')

    def DialogDelAll(self):
        """
        Создание MessageBox при нажатии кнопки "Удалить всё".
        :return: None
        """
        self.messagebox_del_all = QMessageBox(self)
        self.messagebox_del_all.setWindowTitle("Удаление данных")
        self.messagebox_del_all.setText("Вы уверены, что хотите удалить все данные?")
        self.messagebox_del_all.setInformativeText("После сохранения данные будут утеряны!")
        self.messagebox_del_all.setIcon(QMessageBox.Question)
        self.messagebox_del_all.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)

        self.messagebox_del_all.buttonClicked.connect(self.delete_all)
        self.messagebox_del_all.show()
        logging.log(logging.INFO, 'Открыто диалоговое окно "Удаление данных"')

    def DialogDel(self):
        """
        Создание MessageBox при нажатии кнопки "Удалить".
        :return: None
        """
        self.messagebox_del_all = QMessageBox(self)
        self.messagebox_del_all.setWindowTitle("Удаление элемента'")
        self.messagebox_del_all.setText("Стек уже пустой!")
        self.messagebox_del_all.setIcon(QMessageBox.Warning)
        self.messagebox_del_all.setStandardButtons(QMessageBox.Ok)

        self.messagebox_del_all.show()
        logging.log(logging.INFO, 'Открыто диалоговое окно "Удаление элемента"')

    def build_select(self):
        """
        Функция построения выбранной в comboBox версии стека в listWidget.
        :return: None
        """
        self.listWidget.clear()
        strin = '123'
        if type(self.list) == type(strin):
            self.list = [self.list]

        if self.list != None:
            self.listWidget.addItems(self.list)

        logging.log(logging.INFO, 'ListWidget обновлён')

    def build(self):
        """
        Функция построения последней версии стека в listWidget.
        :return: None
        """
        self.list = str(self.facade.get())
        self.listWidget.clear()
        if type(self.list) == type(self.strin):
            self.list = [self.list]

        if self.list != None:
            self.listWidget.addItems(self.list)

        logging.log(logging.INFO, 'ListWidget обновлён')

    def build_CB(self):
        """
        Функция передачи списка id версий, хранящихся в базе данных.
        :return: None
        """
        self.list_id = self.facade.get_id()
        self.comboBox.clear()
        if self.comboBox != None:
            self.comboBox.addItems(self.list_id)
        logging.log(logging.INFO, 'ComboBox обновлён')



class InsertWidget(QtWidgets.QWidget):
    """
    Класс инициализации окна ввода элементов в стек.
    """
    def __init__(self, facade, link=None):
        """
        Загрузка основного окна
        :param link: ссылка на родительское окно
        """
        self.facade = facade
        self.link = link
        super(InsertWidget, self).__init__()
        self.ui = uic.loadUi('forms/InsertWidget.ui', self)
        self.btn_add.clicked.connect(self.add)

    def add(self):
        """
        Функция действия при нажатии на кнопку "Добавить"
        Осуществляется добавление элемента в выбранную версию стека.
        :return: None
        """
        self.current = []
        self.data = int(self.lineEdit.text())

        if self.link.list != None:
            nums = self.link.list[0][1:-1].split(',')
            if nums != ['']:
                for num in nums:
                    self.current.append(int(num))

        if type(self.current) == type(self.link.strin):
            self.current = [self.current]

        if self.current != None:
            self.link.facade.push(self.current, self.data)

        # print("Вы ввели: ", self.data)
        self.label_info.setText(f"Вы ввели: {self.data}")
        self.link.build_CB()
        self.link.build()
        logging.log(logging.INFO, f"Добавлен элемент: {self.data}")



class Builder:
    """
    Паттерн строитель.
    Это порождающий паттерн проектирования, который позволяет создавать сложные объекты пошагово.
    """

    def __init__(self):
        """
        Объявление переменных facade и gui.
        """
        self.facade = None
        self.gui = None

    def create_facade(self):
        """
        Создание ссылки на объект фасада (Facade).
        :return: None
        """
        self.facade = Facade()

    def create_gui(self):
        """
        Создание ссылки на объект графики (MainWindow), если создана ссылка на фасад.
        :return: None
        """
        if self.facade is not None:
            self.gui = MainWindow(self.facade)

    def get_result(self):
        """
        Получение ссылки на объект графики (MainWindow).
        :return: gui - ссылка на объект графики.
        """
        if self.facade is not None and self.gui is not None:
            return self.gui



if __name__ == '__main__':
    qapp = QtWidgets.QApplication(sys.argv)
    builder = Builder()
    builder.create_facade()
    builder.create_gui()
    window = builder.get_result()
    window.show()

    qapp.exec()