# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

import sys
import os

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QFile, Qt, QDate
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QAbstractItemView, QHBoxLayout, QTableView,
                             QVBoxLayout,QGridLayout, QCalendarWidget, QFrame, QLabel,
                             QTextEdit, QMessageBox, QPushButton)

from PyQt5.QtSql import (QSqlRelation, QSqlRelationalTableModel,
                         QSqlRelationalDelegate, QSqlDatabase, QSqlQuery,
                         QSqlTableModel, QSqlRelationalDelegate)

import initDb


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Food Log')
        self.resize(925, 577)

        initDb.setupModel()

        self.widget = MyWidget()
        self.setCentralWidget(self.widget)


class MyWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        horizontalLayout = QHBoxLayout()
        dayView = QTableView()
        dayView.setFrameShape(QFrame.Box)
        horizontalLayout.addWidget(dayView)

        verticalLayout = QVBoxLayout()
        calendarWidget = QCalendarWidget()
        calendarWidget.setMinimumSize(QSize(250, 200))
        calendarWidget.setMaximumSize(QSize(250, 200))
        calendarWidget.setMinimumDate(QDate(2017, 1, 1))
        calendarWidget.setMaximumDate(QDate(2030, 1, 1))
        calendarWidget.setSelectedDate(QDate.currentDate())
        verticalLayout.addWidget(calendarWidget)

        titleFV = QLabel('Food View')
        verticalLayout.addWidget(titleFV)

        lineEdit = QTextEdit()
        lineEdit.setMaximumSize(QSize(200, 25))
        buttonAdd = QPushButton(QIcon("images/add.png"),'',None)
        buttonAdd.setMaximumSize(QSize(20, 30))
        buttonDell = QPushButton(QIcon("images/del.png"),'',None)
        buttonDell.setMaximumSize(QSize(20, 30))

        lineEditLayout = QHBoxLayout()
        lineEditLayout.addWidget(lineEdit)
        lineEditLayout.addWidget(buttonAdd)
        lineEditLayout.addWidget(buttonDell)
        
        verticalLayout.addLayout(lineEditLayout)

        foodView = QTableView()
        foodView.setMinimumSize(QSize(0, 0))
        foodView.setMaximumSize(QSize(250, 1000))
        verticalLayout.addWidget(foodView)
        horizontalLayout.addLayout(verticalLayout)

        self.setLayout(horizontalLayout)

        model_in = QSqlRelationalTableModel()
        model_in.setEditStrategy(QSqlTableModel.OnManualSubmit)
        model_in.setTable("intake_food")

        id_food = model_in.fieldIndex("id_food")
        date = model_in.fieldIndex("food_date")
        mass = model_in.fieldIndex("mass")

        # Set model, hide ID column
        model_in.setRelation(id_food, QSqlRelation("food", "id", "name"))
        model_in.setHeaderData(id_food, Qt.Horizontal, "Food")
        model_in.setHeaderData(date, Qt.Horizontal, "Date")
        model_in.setHeaderData(mass, Qt.Horizontal, "Mass")

        if not model_in.select():
            self.showError(model_in.lastError())
            return

        dayView.setModel(model_in)
        dayView.setItemDelegate(QSqlRelationalDelegate())
        dayView.setColumnHidden(0, True)
        dayView.setSelectionMode(QAbstractItemView.SingleSelection)

        model_f = QSqlRelationalTableModel()
        model_f.setEditStrategy(QSqlTableModel.OnManualSubmit)
        model_f.setFilter("mea")
        model_f.setTable("food")

        name = model_f.fieldIndex("name")

        if not model_f.select():
            self.showError(model_f.lastError())
            return

        foodView.setModel(model_f)
        foodView.setColumnHidden(0, True)
        foodView.setSelectionMode(QAbstractItemView.SingleSelection)

    def showError(self, err):

        QMessageBox.critical(self, "Unable to initialize Database",
                             "Error initializing database: " + err.text())


if __name__ == '__main__':

    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()
