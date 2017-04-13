from PyQt5.QtSql import (QSqlRelation, QSqlRelationalTableModel,
                         QSqlRelationalDelegate, QSqlDatabase, QSqlQuery,
                         QSqlTableModel)
import os, sys
from PyQt5.QtCore import (QFile)

from PyQt5.QtWidgets import QMessageBox


def setupModel():
    filename = os.path.join(os.path.dirname(__file__), "log.db")
    create = not QFile.exists(filename)

    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(filename)
    if not db.open():
        QMessageBox.warning(None, "log.db", "Database not open. Error: %s" %
                            (db.lastError().text()))
        sys.exit(1)
    if create:

        query = QSqlQuery()
        query.exec("""CREATE TABLE food(
            id INTEGER PRIMARY KEY  NOT NULL,
            name VARCHAR(40) NOT NULL,
            rate INTEGER)""")

        query.exec("""CREATE TABLE intake_food(
            id INTEGER PRIMARY KEY  NOT NULL,
            id_food Integer,
            food_date VARCHAR,
            massa INTEGER,
            FOREIGN KEY(id_food) REFERENCES food(id))""")

        for name in (("meat", 5), ("fish", 4), ("bread", 3)):
            query.exec("INSERT INTO food(name,rate) VALUES ('%s', %d)" %
                       (name[0], name[1]))
