# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

import sys
import os

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QFile
from PyQt5.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, QTableView,
                             QVBoxLayout, QCalendarWidget, QFrame, QDialog,
                             QLabel, QTextEdit, QMessageBox)

from PyQt5.QtSql import (QSqlRelation, QSqlRelationalTableModel,
                         QSqlRelationalDelegate, QSqlDatabase, QSqlQuery,
                         QSqlTableModel)

import initDb



class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Food Log')
        self.resize(925, 577)

        initDb.setupModel()

        self.widget = MyDialog()
        self.setCentralWidget(self.widget)


class MyDialog(QDialog):
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
        verticalLayout.addWidget(calendarWidget)

        titleFV = QLabel('Food View')
        verticalLayout.addWidget(titleFV)

        lineEdit = QTextEdit()
        lineEdit.setMaximumSize(QSize(250, 25))
        verticalLayout.addWidget(lineEdit)

        foodView = QTableView()
        foodView.setMinimumSize(QSize(0, 0))
        foodView.setMaximumSize(QSize(250, 1000))
        verticalLayout.addWidget(foodView)
        horizontalLayout.addLayout(verticalLayout)

        self.setLayout(horizontalLayout)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()
