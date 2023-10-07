# подключение нужных библиотек
import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem


class MyWidget(QWidget):  # создание класса окна
    def __init__(self):  # инициализация класса
        super().__init__()
        uic.loadUi('interface.ui', self)  # подключение интерфейса, созданного в Qt Designer
        # создание необходимых словарей, которые потребуются в работе с выдвижными списками
        self.params_blood = {}
        self.params_donor_id = {}
        self.params_request_id = {}
        # создание переменных для удобства запросов в обе таблицы
        self.updating_donor = 'SELECT sd.ID, sd.name, sgb.group_name '\
                              'FROM storage_donor sd, storage_group_blood sgb '\
                              'WHERE sd.group_blood = sgb.ID'
        self.updating_request = 'SELECT sq.ID, sq.name, sgb.group_name ' \
                                'FROM storage_request sq, storage_group_blood sgb ' \
                                'WHERE sq.group_blood = sgb.ID'
        self.con = sqlite3.connect('storage.db')  # подключение к БД
        self.select_blood_group()  # включение функции для выдвижного списка группы крови
        self.select_id_donor()  # включение функции для выдвижного списка ID доноров
        self.select_id_request()  # включение функции для выдвижного списка ID запросов
        #
        self.search_of_donor.clicked.connect(self.search_donor)  # подключение кнопки для поиска доноров
        self.search_of_request.clicked.connect(self.search_request)  # подключение кнопки для поиска запросов
        self.delete_button.clicked.connect(self.delete_function)  # подключение кнопки для удаления запроса и донора
        self.create_of_donor.clicked.connect(self.create_donor)  # подключение кнопки для создания донора
        self.create_of_request.clicked.connect(self.create_request)  # подключение кнопки для создания запроса
        self.ndbutton_donor.clicked.connect(self.go_to_all_donors)  # подключение кнопки для сбрасывания
        # фильтра по группе крови для доноров
        self.ndbutton_request.clicked.connect(self.go_to_all_requests)  # подключение кнопки для сбрасывания
        # фильтра по группе крови для запросов
        self.setWindowTitle('Донорство крови')  # установка наименования окна
        # активация функций, ответсвенных за обновления двух таблиц (доноров и запросов соответственно
        self.execute_query_and_fill_table_of_donor(self.updating_donor)
        self.execute_query_and_fill_table_of_request(self.updating_request)

    def select_blood_group(self):  # создание функции для выбора группы крови в выдвижном списке
        # поиск по базе данных группы крови
        req = 'SELECT id, group_name from storage_group_blood'
        cur = self.con.cursor()
        for value, key in cur.execute(req).fetchall():
            self.params_blood[key] = value
        self.filter_donor.addItems(list(self.params_blood.keys()))  # добавление списка к фильтру по донорам
        self.filter_request.addItems(list(self.params_blood.keys()))  # добавление списка  к фильтру по запросам
        self.create_group_request.addItems(list(self.params_blood.keys()))  # добавление списка к выбору группы крови
        # для создания запроса
        self.create_group_donor.addItems(list(self.params_blood.keys()))  # добавление списка к выбору группы крови
        # для создания донора

    def select_id_donor(self):  # создание функции для выбора ID в выдвижном списке для донора
        # поиск по базе данных доноров, откуда берём ID и имя
        req = 'SELECT id, name from storage_donor'
        cur = self.con.cursor()
        for key, value in cur.execute(req).fetchall():
            self.params_donor_id[str(key)] = key
        self.select_donor_id.addItems(list(self.params_donor_id.keys()))  # добавление списка к выбору ID при создании
        # донора

    def select_id_request(self):  # создание функции для выбора ID в выдвижном списке для запроса
        # поиск по базе данных запросов, откуда берём ID и имя
        req = 'SELECT id, name from storage_request'
        cur = self.con.cursor()
        for key, value in cur.execute(req).fetchall():
            self.params_request_id[str(key)] = key
        self.select_request_id.addItems(list(self.params_request_id.keys()))  # добавление списка к выбору
        # ID при создании
    def search_donor(self):  # создание функции для поиска запросов при нажатии кнопки
        req = 'SELECT sd.ID, sd.name, sgb.group_name FROM storage_donor sd, storage_group_blood sgb '\
              'WHERE sd.group_blood = sgb.ID AND sd.group_blood = {}'.format(
            self.params_blood.get(self.filter_donor.currentText()))  # формирование запроса, где находим и сортируем
        # всех доноров по данной группе крови
        self.execute_query_and_fill_table_of_donor(req)  # обновление таблицы доноров

    def search_request(self):  # создание функции для поиска запросов при нажатии кнопки
        req = 'SELECT sq.ID, sq.name, sgb.group_name FROM storage_request sq, storage_group_blood sgb ' \
              'WHERE sq.group_blood = sgb.ID AND sq.group_blood = {}'.format(
            self.params_blood.get(self.filter_request.currentText()))  # формирование запроса в базу данных,
        # где находим и сортируем все запросы по данной группе крови
        self.execute_query_and_fill_table_of_request(req)  # обновление таблицы запросов

    def execute_query_and_fill_table_of_donor(self, query):  # создание функции обновления таблицы доноров
        # поиск доноров по введенному запросу "query"
        cur = self.con.cursor()
        result = cur.execute(query).fetchall()
        # создание параметров таблицы
        self.table_of_donor.setRowCount(len(result))
        self.table_of_donor.setColumnCount(3)
        self.table_of_donor.setHorizontalHeaderLabels(['ID', 'Название', 'Группа крови'])
        # добавление в таблицу элементов из результата введенного запроса
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.table_of_donor.setItem(i, j, QTableWidgetItem(str(val)))

    def execute_query_and_fill_table_of_request(self, query):  # создание функции обновления таблицы запросов
        # поиск запросов по введенному запросу "query"
        cur = self.con.cursor()
        result = cur.execute(query).fetchall()
        # создание параметров таблицы
        self.table_of_request.setRowCount(len(result))
        self.table_of_request.setColumnCount(3)
        self.table_of_request.setHorizontalHeaderLabels(['ID', 'Название', 'Группа крови'])
        # обавление в таблицу элементов из результата введенного запроса
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.table_of_request.setItem(i, j, QTableWidgetItem(str(val)))

    def create_donor(self):  # создание функции для создания донора
        # проверка на ошибку, если пользователь введет неожиданные данные
        try:
            cur = self.con.cursor()
            id = self.id_edit_donor.text()  # считывание ID с соответствующего поля для ввода
            name = self.create_name_of_donor.text()  # считывание названия с соответствующего поля для ввода
            group = self.params_blood.get(self.filter_request.currentText())  # считывание группы крови донора,
            # выбранного пользователем
            cur.execute(f'INSERT INTO storage_donor (id, name, group_blood) VALUES ({id}, {name}, {group})')  # в базу
            # данных добавляется элемент с параметрами, заданными пользователем
            self.execute_query_and_fill_table_of_donor(self.updating_donor)  # обновление таблицы доноров
            self.con.commit() # завершение работы с базой данных для этой функции
        except sqlite3.OperationalError:
            self.errorLabel.setText('Неправильный ID или название')  # в случае ошибки пользователь увидит это

    def create_request(self):  # создание функции для создания запроса
        # проверка на ошибку, если пользователь введет неожиданные данные
        try:
            cur = self.con.cursor()
            id = self.id_edit_request.text()  # считывание ID с соответствующего поля для ввода
            name = self.create_name_of_request.text()   # считывание названия с соответствующего поля для ввода
            group = self.params_blood.get(self.filter_request.currentText())  # считывание группы крови запроса,
            # выбранного пользователем
            cur.execute(f'INSERT INTO storage_request (id, name, group_blood) VALUES ({id}, {name}, {group})')  # в базу
            # данных добавляется элемент с параметрами, заданными пользователем
            self.execute_query_and_fill_table_of_request(self.updating_request) # обновление таблицы доноров
            self.con.commit()  # завершение работы с базой данных для этой функции
        except sqlite3.OperationalError:
            self.errorLabel.setText('Неправильный ID или название')  # в случае ошибки пользователь увидит это

    def delete_function(self):  # создание функции удаления донора и запроса, если их группы крови подходят
        cur = self.con.cursor()
        result_1 = cur.execute('SELECT group_blood FROM storage_donor WHERE ID = {}'.format(
            self.params_donor_id.get(self.select_donor_id.currentText()))).fetchall()  # считывание группы крови
        # у донора
        result_2 = cur.execute('SELECT group_blood FROM storage_request WHERE ID = {}'.format(
            self.params_request_id.get(self.select_request_id.currentText()))).fetchall()  # считывание группы крови
        # у запроса
        if result_1 == result_2:  # сравнение групп крови
            cur.execute('DELETE FROM storage_donor WHERE ID = {}'.format(
            self.params_donor_id.get(self.select_donor_id.currentText())))  # удаление донора из своей таблицы
            cur.execute('DELETE FROM storage_request WHERE ID = {}'.format(
            self.params_request_id.get(self.select_request_id.currentText())))  # удаление запроса из своей таблицы
            self.con.commit()  # завершение работы с базой данных для этой функции
            # обновления таблиц
            self.execute_query_and_fill_table_of_donor(self.search_donor)
            self.execute_query_and_fill_table_of_request(self.search_request)
        # в противном случае пользователь увидит несоответствие
        else:
            self.errorLabel.setText('Группа крови не совпадает')

    def go_to_all_donors(self):  # создание функции возврата таблицы доноров в безфильтерное состояние (отменяет фильтр)
        req = 'SELECT id, name, group_blood FROM storage_donor'
        self.execute_query_and_fill_table_of_donor(req)

    def go_to_all_requests(self):  # создание функции возврата таблицы запросов в безфильтерное состояние
        # (отменяет фильтр)
        req = 'SELECT id, name, group_blood FROM storage_request'
        self.execute_query_and_fill_table_of_donor(req)


# финальная часть и запуск самой программы
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())