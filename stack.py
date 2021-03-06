import json


class Stack:
    """
    Структура данных персистентный стек.
    """
    def __init__(self, json_data=None, stack=None):
        """
        Структура данных персистентный стек.
        :param json_data: версия стека в формате json
        :param stack: стек
        """
        self.stack = stack
        self.version = []
        self.json_data = json_data

    def push(self, current, item):
        """
        Функция, осуществляющая добавление элемента в стек.
        :param current: выбранная версия, куда вставляется элемент
        :param item: добавляемый элемент
        :return: None
        """
        self.stack = current
        self.stack.append(item)
        self.save_version()
        self.json_data = json.dumps(self.stack, indent=4)

    def pop(self, current):
        """
        Функция, осуществляющая удаление последнего элемента из выбранной версии стека.
        :param current: выбранная версия, откуда удаляется последний элемент
        :return: None
        """
        self.stack = current
        if len(self.stack) == 0:
            return self
        else:
            remove = self.stack.pop()
            self.save_version()
            self.json_data = json.dumps(self.stack, indent=4)
            return remove

    def save_version(self):
        """
        Функция сохранения версии стека.
        :return: None
        """
        self.version.append(self.stack.copy())

    def get_json_data(self):
        """
        Функция получения json-строки с сохранённой версией стека.
        :return: json_data
        """
        return self.json_data
