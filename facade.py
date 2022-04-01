from database import Database
from stack import Stack

class Facade:
    """
    Класс фасада
    """
    def __init__(self, name='Database.db'):
        """
        Создание объекта базы данных, структуры данных.
        :param name: имя базы данных
        """
        self.DB = Database(name)

        list = []
        if self.DB.get_lastVersion() != None:
            nums = self.DB.get_lastVersion()[0][1:-1].split(',')
            if nums != ['']:
                for num in nums:
                    list.append(int(num))

        self.S = Stack(stack=list)

    def save(self):
        """
        Сохранение новой версии в базу данных.
        :return: None
        """
        data = self.S.get_json_data()
        self.DB.Insert_in_Table(data)
        self.S.version.clear()

    def push(self, current, data):
        """
        Функция добавления введённого элемента в стек.
        :param current: выбранная версия стека
        :param data: добавляемый элемент
        :return: None
        """
        self.S.push(current, data)
        self.save()

    def pop(self, current):
        """
        Функция удаления последнего элемента из стека.
        :param current: выбранная версия стека
        :return: None
        """
        self.S.pop(current)
        self.save()

    def get(self):
        """
        Функция получения последней версии стека из базы данных.
        :return: None
        """
        version = []
        if self.DB.get_lastVersion() != None:
            nums = self.DB.get_lastVersion()[0][1:-1].split(',')
            if nums != ['']:
                for num in nums:
                    version.append(int(num))
        # print('vers', version)
        return version

    def get_id(self):
        """
        Функция получения списка id версий из базы данных для comboBox.
        :return: None
        """
        list_id = self.DB.get_id()
        return list_id

    def get_select(self, id):
        """
        Функция получения выбранной версии.
        :param id: айди выбранной версии
        :return: None
        """
        select = []
        if self.DB.select(id) != None:
            nums = self.DB.select(id)[0][1:-1].split(',')
            if nums != ['']:
                for num in nums:
                    select.append(int(num))
        return select

    def delete_all(self):
        """
        Функция, удаляющая все данные.
        :return:
        """
        vers = self.get()
        if vers is not None:
            self.DB.delete_all()
        else:
            print("Стек уже пустой!")