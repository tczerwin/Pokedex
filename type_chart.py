# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PokemonDatabase import TYPE_COLORS, TYPE_ADVANTAGE

class Ui_TypeChart(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("TypeChart")
        MainWindow.resize(800, 650)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Title
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(20, 10, 760, 40))
        self.title.setObjectName("title")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setStyleSheet("color: black; font-weight: bold; font-size: 24pt;")
        self.title.setText("Type Effectiveness Chart")

        # Create type chart table
        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setGeometry(QtCore.QRect(20, 60, 760, 550))
        self.table.setObjectName("table")
        self.table.setColumnCount(3)
        self.table.setRowCount(18)
        self.table.setHorizontalHeaderLabels(["Type", "Strong Against", "Weak To"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 350)

        # Populate the table
        types = sorted(TYPE_ADVANTAGE.keys())
        for i, ptype in enumerate(types):
            # Type name
            type_item = QtWidgets.QTableWidgetItem(ptype.capitalize())
            type_item.setBackground(QtGui.QColor(TYPE_COLORS.get(ptype, "#999999")))
            type_item.setForeground(QtGui.QColor("white"))
            type_item.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
            self.table.setItem(i, 0, type_item)

            # Strong against
            strong_against = ", ".join([t.capitalize() for t in TYPE_ADVANTAGE[ptype]])
            strong_item = QtWidgets.QTableWidgetItem(strong_against)
            self.table.setItem(i, 1, strong_item)

            # Weak to - find what's strong against this type
            weak_to = []
            for attacker_type, defender_types in TYPE_ADVANTAGE.items():
                if ptype in defender_types:
                    weak_to.append(attacker_type.capitalize())
            weak_item = QtWidgets.QTableWidgetItem(", ".join(sorted(weak_to)))
            self.table.setItem(i, 2, weak_item)

        self.table.setRowHeight(i, 30)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Type Effectiveness Chart"))
