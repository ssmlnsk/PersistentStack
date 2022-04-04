from sqlite3 import connect
import json


class Database:
    """
    Класс с функциями для взаимодействия с базой данных.
    """

    def __init__(self, name):
        """
        Создание базы данных.
        :param name: имя базы данных
        """
        self.conn = connect(f"{name}")
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS versions (id INTEGER PRIMARY KEY AUTOINCREMENT, version TEXT)")
        self.conn.commit()
        cursor.close()

    def insert(self, data):
        """
        Функция для вставки данных в базу данных.
        :param data: данные, которые вставляются в базу данных
        :return: None
        """
        if data == 'None':
            data = None
        cursor = self.conn.cursor()
        cursor.execute(f"""INSERT INTO versions (version) VALUES ('{data}')""")
        self.conn.commit()
        cursor.close()

    def get_last_version(self):
        """
        Функция получения последней версии стека.
        :return: None
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT version FROM versions WHERE id = (SELECT MAX(id) FROM versions);")
        last_version_json = json.dumps(cursor.fetchone())
        last_version = json.loads(last_version_json)
        self.conn.commit()
        cursor.close()
        return last_version

    def get_id(self):
        """
        Функция получения списка id версий, хранящихся в базе данных.
        :return: None
        """
        cursor = self.conn.cursor()
        list_id = [str(i)[1:-2] for i in cursor.execute("SELECT id FROM versions")]
        cursor.close()
        return list_id

    def select(self, id):
        """
        Функция получения выбранной версии стека.
        :param id: айди выбранной версии
        :return: None
        """
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT version FROM versions WHERE id = ('{id}')")
        select_json = json.dumps(cursor.fetchone())
        select = json.loads(select_json)
        self.conn.commit()
        cursor.close()
        return select

    def delete_all(self):
        """
        Функция удаления версий.
        :return: None
        """
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM versions")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'versions'")
        cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'versions'")
        self.conn.commit()
        cursor.close()
