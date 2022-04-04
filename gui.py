import sys
import logging

from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from facade import Facade

logging.basicConfig(level=logging.INFO)


class MainWindow(QMainWindow):
    """
    Класс создания главного окна.
    """

    def __init__(self, facade):
        """
        Загрузка основного окна, прикрепление действий к кнопкам
        и отображение последней версии стека в listWidget.
        """
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi('forms/MainWindow.ui', self)
        self.setWindowIcon(QIcon('img/icon.jpg'))
        self.facade = facade
        self.list = []
        self.string = '123'
        self.btn_open_add.clicked.connect(lambda: self.add_elem())
        self.btn_delete.clicked.connect(lambda: self.delete_elem())
        self.btn_delete_all.clicked.connect(lambda: self.del_all())
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

    def add_elem(self):
        """
        Функция открытия окна добавления элемента.
        :return: None
        """
        self.ui = InsertWidget(self.facade, self)
        self.ui.show()
        logging.log(logging.INFO, 'Открыто окно "Добавление элемента"')

    def del_all(self):
        """
        Функция определения пустой ли стек для удаления данных.
        :return: None
        """
        if self.facade.get() == []:
            self.dialog_del_one_elem()
        else:
            self.dialog_del_all()

    def delete_elem(self):
        """
        Функция удаления элемента через графический интерфейс.
        :return: None
        """
        current = []
        if self.list is not None:
            nums = self.list[0][1:-1].split(',')
            if nums != ['']:
                for num in nums:
                    current.append(int(num))

        if (type(current)) == (type(self.string)):
            current = [current]

        if current is not None:
            if current == []:
                self.dialog_del_one_elem()
                logging.log(logging.INFO, 'Стек уже пуст!')
            else:
                self.facade.pop(current)
                self.build_combobox()
                self.build()
                logging.log(logging.INFO, 'Последний элемент удалён!')

    def delete_all(self, button):
        """
        Функция удаления всех данных из базы данных.
        :param button: нажатая кнопка
        :return:
        """
        if button.text() == "OK":
            self.facade.delete_all()
            self.build_combobox()
            self.build()
            logging.log(logging.INFO, 'Данные удалены')
        else:
            logging.log(logging.INFO, 'Данные не удалены')

    def dialog_del_all(self):
        """
        Создание MessageBox при нажатии кнопки "Удалить всё".
        :return: None
        """
        messagebox_del_all = QMessageBox(self)
        messagebox_del_all.setWindowTitle("Удаление")
        messagebox_del_all.setText("Вы уверены, что хотите удалить все данные?")
        messagebox_del_all.setIcon(QMessageBox.Question)
        messagebox_del_all.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)

        messagebox_del_all.buttonClicked.connect(self.delete_all)
        messagebox_del_all.show()
        logging.log(logging.INFO, 'Открыто диалоговое окно "Удаление данных"')

    def dialog_del_one_elem(self):
        """
        Создание MessageBox при нажатии кнопки "Удалить".
        :return: None
        """
        messagebox_del = QMessageBox(self)
        messagebox_del.setWindowTitle("Удаление")
        messagebox_del.setText("Стек уже пустой!")
        messagebox_del.setIcon(QMessageBox.Warning)
        messagebox_del.setStandardButtons(QMessageBox.Ok)

        messagebox_del.show()
        logging.log(logging.INFO, 'Открыто диалоговое окно "Удаление элемента"')

    def build_select(self):
        """
        Функция построения выбранной в comboBox версии стека в listWidget.
        :return: None
        """
        self.listWidget.clear()
        if (type(self.list)) == (type(self.string)):
            self.list = [self.list]

        if self.list is not None:
            self.listWidget.addItems(self.list)

        logging.log(logging.INFO, 'ListWidget обновлён')

    def build(self):
        """
        Функция построения последней версии стека в listWidget.
        :return: None
        """
        self.list = str(self.facade.get())
        self.listWidget.clear()
        if (type(self.list)) == (type(self.string)):
            self.list = [self.list]

        if self.list is not None:
            self.listWidget.addItems(self.list)

        logging.log(logging.INFO, 'ListWidget обновлён')

    def build_combobox(self):
        """
        Функция передачи списка id версий, хранящихся в базе данных.
        :return: None
        """
        list_id = self.facade.get_id()
        self.comboBox.clear()
        if self.comboBox is not None:
            self.comboBox.addItems(list_id)
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
        self.setWindowIcon(QIcon('img/add.jpg'))
        self.btn_add.clicked.connect(self.add)

    def add(self):
        """
        Функция действия при нажатии на кнопку "Добавить"
        Осуществляется добавление элемента в выбранную версию стека.
        :return: None
        """
        current = []
        data = self.lineEdit.text()
        if data == '':
            self.warning_no_nums()
        elif data.isnumeric() == False:
            self.warning_no_int()
        else:
            data = int(data)
            if self.link.list is not None:
                nums = self.link.list[0][1:-1].split(',')
                if nums != ['']:
                    for num in nums:
                        current.append(int(num))

            if (type(current)) == (type(self.link.string)):
                current = [current]

            if current is not None:
                self.link.facade.push(current, data)

            self.label_info.setText(f"Вы ввели: {data}")
            self.link.build_combobox()
            self.link.build()
            logging.log(logging.INFO, f"Добавлен элемент: {data}")

    def warning_no_int(self):
        """
        Создание MessageBox, если данные содержат буквы и символы.
        :return: None
        """
        messagebox_del = QMessageBox(self)
        messagebox_del.setWindowTitle("Ошибка ввода")
        messagebox_del.setText("Введите число!")
        messagebox_del.setIcon(QMessageBox.Warning)
        messagebox_del.setStandardButtons(QMessageBox.Ok)

        messagebox_del.show()
        logging.log(logging.INFO, 'Открыто диалоговое окно "Ошибка ввода"')

    def warning_no_nums(self):
        """
        Создание MessageBox, если данные не введены.
        :return: None
        """
        messagebox_del = QMessageBox(self)
        messagebox_del.setWindowTitle("Ошибка ввода")
        messagebox_del.setText("Заполните поле!")
        messagebox_del.setIcon(QMessageBox.Warning)
        messagebox_del.setStandardButtons(QMessageBox.Ok)

        messagebox_del.show()
        logging.log(logging.INFO, 'Открыто диалоговое окно "Ошибка ввода"')


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
