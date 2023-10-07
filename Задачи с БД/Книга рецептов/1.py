import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("untitled.ui", self)
        self.con = sqlite3.connect("book.db")
        cur = self.con.cursor()
        self.modified = {}
        self.titles = None
        self.comboBox.addItems(
            [item[0] for item in cur.execute("SELECT name FROM allergens").fetchall()])
        self.pushButton_2.clicked.connect(self.filter)
        self.pushButton.clicked.connect(self.run)
        self.pushButton_3.clicked.connect(self.delete)
        self.pushButton_4.clicked.connect(self.add)
        result = cur.execute(f"""SELECT * FROM dishes""").fetchall()
        self.tableWidget_2.setRowCount(len(result))
        self.tableWidget_2.setColumnCount(len(result[0]))
        self.tableWidget_2.setHorizontalHeaderLabels([description[0] for description in cur.description])
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget_2.setItem(i, j, QTableWidgetItem(str(val)))

    def filter(self):
        cur = self.con.cursor()
        result = cur.execute(f"""SELECT DISTINCT dishes.name as Блюдо, 
        allergens.name as Аллерген, dishes.receipt as Рецепт 
        FROM dishes, allergens JOIN dishes_allergens 
        ON dishes.id = dishes_allergens.id_dish AND 
        allergens.id = dishes_allergens.id_allergen
        WHERE id_allergen = {self.comboBox.currentIndex() + 1}
        """).fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setHorizontalHeaderLabels([description[0] for description in cur.description])
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def run(self):
        cur = self.con.cursor()
        if self.lineEdit.text():
            result = cur.execute(f"{self.lineEdit.text()}").fetchall()
        else:
            result = cur.execute(
                f"""SELECT DISTINCT dishes.name as Блюдо, 
                allergens.name as Аллерген, dishes.receipt as Рецепт 
                FROM dishes, allergens JOIN dishes_allergens 
                ON dishes.id = dishes_allergens.id_dish AND 
                allergens.id = dishes_allergens.id_allergen
                ORDER BY dishes.name""").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setHorizontalHeaderLabels([description[0] for description in cur.description])
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def delete(self):
        rows = list(set([i.row() for i in self.tableWidget_2.selectedItems()]))
        ids = [self.tableWidget_2.item(i, 0).text() for i in rows]
        # Спрашиваем у пользователя подтверждение на удаление элементов
        valid = QMessageBox.question(
            self, '', "Действительно удалить элементы с id " + ",".join(ids),
            QMessageBox.Yes, QMessageBox.No)
        # Если пользователь ответил утвердительно, удаляем элементы.
        # Не забываем зафиксировать изменения
        if valid == QMessageBox.Yes:
            cur = self.con.cursor()
            cur.execute("DELETE FROM dishes WHERE id IN (" + ", ".join('?' * len(ids)) + ")", ids)
            self.con.commit()

    def add(self):
        cur = self.con.cursor()
        que = f"INSERT INTO dishes(name, receipt) VALUES " \
              f"('{self.lineEdit_2.text()}', '{self.lineEdit_3.text()}')"
        print(que)
        cur.execute(que)
        self.con.commit()

    def save_results(self):
        if self.modified:
            cur = self.con.cursor()
            que = "UPDATE dishes SET\n"
            que += ", ".join([f"{key}='{self.modified.get(key)}'"
                              for key in self.modified.keys()])
            que += "WHERE id = ?"
            print(que)
            cur.execute(que, (self.spinBox.text(),))
            self.con.commit()
            self.modified.clear()

    def hello(self):
        print('Author by Elena Kuzmina')
        print('my first git program')
        print('i am learning GIT')
        print('version2')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
