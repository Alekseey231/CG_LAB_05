# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\design.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
from typing import List, Union

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QPointF
from PyQt5.QtGui import QTransform, QImage
from PyQt5.QtWidgets import QGraphicsView


class CustomGraphicsView(QGraphicsView):
    pointSignal = pyqtSignal(QPoint)
    endSignal = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = QImage(5000, 5000, QImage.Format_ARGB32)
        self.image.fill(Qt.transparent)
        self.zoom = 0
        self.setTransform(QTransform().scale(1, -1))

    def resizeEvent(self, event):
        # Вызываем родительский метод для обработки изменения размера виджета
        super().resizeEvent(event)
        self.centerOn(self.image.width() / 2, self.image.height() / 2)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            try:
                pos_scene = self.mapToScene(event.pos())

                # Преобразуем координаты в координаты QGraphicsView
                pos_view = self.mapFromScene(pos_scene)

                # Вычисляем разницу между координатами и центром QGraphicsView
                center = self.viewport().rect().center()
                diff = pos_view - center

            except Exception as e:
                print(e)

            try:
                pass
                self.pointSignal.emit(diff)
            except Exception as e:
                print(e)
            event.accept()
        elif event.button() == Qt.RightButton:
            self.endSignal.emit(0)
        else:
            super().mousePressEvent(event)


"""
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.ClosedHandCursor)
            self._start_pos = event.pos()  # запоминаем начальное положение мыши
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._start_pos is not None:
            delta = event.pos() - self._start_pos  # вычисляем вектор смещения
            self._start_pos = event.pos()  # обновляем начальное положение мыши
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.ArrowCursor)
            self._start_pos = None  # очищаем начальное положение мыши
            event.accept()
        else:
            super().mouseReleaseEvent(event)
"""


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(714, 609)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setMaximumSize(QtCore.QSize(250, 16777215))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.widget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.p_fill = QtWidgets.QPushButton(self.widget)
        self.p_fill.setObjectName("p_fill")
        self.verticalLayout.addWidget(self.p_fill)
        self.horizontalLayout.addWidget(self.widget)
        self.graphicsView = CustomGraphicsView()
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 714, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.p_fill.setText(_translate("MainWindow", "Fill"))
