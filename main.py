# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

import sys
import os

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import (QSize, QFile, Qt, QDate, QSortFilterProxyModel,
                          QRegExp)
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QAbstractItemView,
    QHBoxLayout,
    QTableView,
    QVBoxLayout,
    QGridLayout,
    QCalendarWidget,
    QFrame,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton, )

from PyQt5.QtSql import (QSqlRelation, QSqlRelationalTableModel,
                         QSqlRelationalDelegate, QSqlDatabase, QSqlQuery,
                         QSqlTableModel, QSqlRelationalDelegate)

import initDb
from FlipProxyDelegate import FlipProxyDelegate

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Food Log')
        self.resize(600, 577)

        initDb.setupModel()

        self.widget = MyWidget()
        self.setCentralWidget(self.widget)
        self.setWindowIcon(QIcon("images/apple.png"))


class MyWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        horizontalLayout = QHBoxLayout()
        self.dayView = QTableView()
        self.dayView.setFrameShape(QFrame.Box)
        self.dayView.horizontalHeader().setStretchLastSection(True)
        self.dayView.verticalHeader().setVisible(False)
        horizontalLayout.addWidget(self.dayView)

        verticalLayout = QVBoxLayout()
        self.calendarWidget = QCalendarWidget()
        self.calendarWidget.setMinimumSize(QSize(250, 200))
        self.calendarWidget.setMaximumSize(QSize(250, 200))
        self.calendarWidget.setMinimumDate(QDate(2017, 1, 1))
        self.calendarWidget.setMaximumDate(QDate(2030, 1, 1))
        self.calendarWidget.selectionChanged.connect(self.dataChange)
        self.calendarWidget.setSelectedDate(QDate.currentDate())

        verticalLayout.addWidget(self.calendarWidget)

        titleFV = QLabel('Food View')
        verticalLayout.addWidget(titleFV)

        self.filterLine = QLineEdit()
        self.filterLine.setMaximumSize(QSize(200, 25))

        self.filterLine.textChanged.connect(self.filterChange)

        buttonAdd = QPushButton(QIcon("images/add.png"), '', None)
        buttonAdd.setMaximumSize(QSize(20, 30))
        buttonAdd.clicked.connect(self.addFood)
        buttonDell = QPushButton(QIcon("images/del.png"), '', None)
        buttonDell.setMaximumSize(QSize(20, 30))
        buttonAdd.clicked.connect(self.delFood)

        lineEditLayout = QHBoxLayout()
        lineEditLayout.addWidget(self.filterLine)
        lineEditLayout.addWidget(buttonAdd)
        lineEditLayout.addWidget(buttonDell)

        verticalLayout.addLayout(lineEditLayout)

        self.foodView = QTableView()
        self.foodView.setMinimumSize(QSize(0, 0))
        self.foodView.setMaximumSize(QSize(250, 1000))
        self.foodView.verticalHeader().setVisible(False)
        self.foodView.horizontalHeader().setStretchLastSection(True)

        verticalLayout.addWidget(self.foodView)
        horizontalLayout.addLayout(verticalLayout)

        self.setLayout(horizontalLayout)

        model_in = QSqlRelationalTableModel()
        model_in.setEditStrategy(QSqlTableModel.OnFieldChange)
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

        self.proxyModel_in = QSortFilterProxyModel()
        self.proxyModel_in.setSourceModel(model_in)
        self.proxyModel_in.setFilterKeyColumn(2)

        self.dayView.setItemDelegate(FlipProxyDelegate())
        self.dayView.setModel(self.proxyModel_in)
        self.dayView.setColumnHidden(0, True)
        self.dayView.setColumnHidden(2, True)
        self.dayView.setSelectionMode(QAbstractItemView.SingleSelection)
        # filter day food by calendar widget
        self.dataChange()

        self.model_f = QSqlRelationalTableModel()
        self.model_f.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model_f.setTable("food")

        self.model_f.setHeaderData(1, Qt.Horizontal, "Food")
        self.model_f.setHeaderData(2, Qt.Horizontal, "Rate")

        if not self.model_f.select():
            self.showError(self.model_f.lastError())
            return

        self.proxyModel_f = QSortFilterProxyModel()
        self.proxyModel_f.setSourceModel(self.model_f)
        self.proxyModel_f.setFilterKeyColumn(1)

        self.foodView.setModel(self.proxyModel_f)
        self.foodView.setColumnHidden(0, True)
        self.foodView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.foodView.setColumnWidth(1, 150)
        self.foodView.setColumnWidth(2, 90)

    def showError(self, err):

        QMessageBox.critical(self, "Unable to initialize Database",
                             "Error initializing database: " + err.text())

    def filterChange(self):
        regExp = QRegExp(self.filterLine.text(), Qt.CaseInsensitive,
                         QRegExp.FixedString)
        self.proxyModel_f.setFilterRegExp(regExp)

    def dataChange(self):
        date = self.calendarWidget.selectedDate().toString('dd.MM.yyyy')
        regExp = QRegExp(date, Qt.CaseInsensitive, QRegExp.FixedString)
        self.proxyModel_in.setFilterRegExp(regExp)

    def addFood(self):
        self.model_f.addrow(self.model_f.columnCount())

    def delFood(self):
        print(self.foodView.selectedIndexes())

    def resizeEvent(self, event):
        self.dayView.setColumnWidth(1, self.dayView.width() * 0.7)
        self.dayView.setColumnWidth(3, self.dayView.width() * 0.2)

        QWidget.resizeEvent(self, event)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()
