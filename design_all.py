from typing import List, Union

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QPointF, QEvent
from PyQt5.QtGui import QTransform, QImage, QMouseEvent
from PyQt5.QtWidgets import QGraphicsView, QApplication, QLabel


class ClickableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        self.clicked.emit()

    clicked = QtCore.pyqtSignal()


class CustomGraphicsView(QGraphicsView):
    pointSignal = pyqtSignal(QPoint)
    endSignal = pyqtSignal(int)
    keySignal = pyqtSignal(QPoint, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.last_x = None
        self.last_y = None
        self.last_mouse_pos = None
        self.image = QImage(5000, 5000, QImage.Format_ARGB32)
        self.image.fill(Qt.transparent)
        self.zoom = 0
        self.setTransform(QTransform().scale(1, -1))
        self.shift_pressed = False
        # self.installEventFilter(self)
        self.setMouseTracking(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def resizeEvent(self, event):
        # Вызываем родительский метод для обработки изменения размера виджета
        super().resizeEvent(event)
        self.centerOn(self.image.width() / 2, self.image.height() / 2)

    def mousePressEvent(self, event):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        # print(modifiers == QtCore.Qt.ShiftModifier)
        if event.button() == Qt.LeftButton:
            pos_scene = self.mapToScene(event.pos())

            # Преобразуем координаты в координаты QGraphicsView
            pos_view = self.mapFromScene(pos_scene)

            # Вычисляем разницу между координатами и центром QGraphicsView
            center = self.viewport().rect().center()
            diff = pos_view - center
            try:
                if modifiers == QtCore.Qt.ShiftModifier:
                    self.keySignal.emit(diff, 0)
                elif modifiers == QtCore.Qt.ControlModifier:
                    self.keySignal.emit(diff, 1)
                else:
                    self.pointSignal.emit(diff)
            except Exception as e:
                print(e)

            event.accept()
        elif event.button() == Qt.RightButton:
            self.endSignal.emit(0)
        else:
            super().mousePressEvent(event)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(696, 647)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setMinimumSize(QtCore.QSize(230, 0))
        self.widget.setMaximumSize(QtCore.QSize(250, 16777215))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.comboBox = QtWidgets.QComboBox(self.widget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.verticalLayout.addWidget(self.comboBox)
        self.tableWidget = QtWidgets.QTableWidget(self.widget)
        self.tableWidget.setMinimumSize(QtCore.QSize(230, 0))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.groupBox = QtWidgets.QGroupBox(self.widget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.l_x = QtWidgets.QLineEdit(self.groupBox)
        self.l_x.setObjectName("l_x")
        self.horizontalLayout_2.addWidget(self.l_x)
        self.l_y = QtWidgets.QLineEdit(self.groupBox)
        self.l_y.setObjectName("l_y")
        self.horizontalLayout_2.addWidget(self.l_y)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.b_add_point = QtWidgets.QPushButton(self.groupBox)
        self.b_add_point.setObjectName("b_add_point")
        self.verticalLayout_2.addWidget(self.b_add_point)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.widget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.l_choosen_color = ClickableLabel(self.groupBox_2)
        self.l_choosen_color.setText("")
        self.l_choosen_color.setObjectName("l_choosen_color")
        self.verticalLayout_3.addWidget(self.l_choosen_color)
        self.b_choose_color = QtWidgets.QPushButton(self.groupBox_2)
        self.b_choose_color.setObjectName("b_choose_color")
        self.verticalLayout_3.addWidget(self.b_choose_color)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.b_get_time = QtWidgets.QPushButton(self.widget)
        self.b_get_time.setObjectName("b_get_time")
        self.verticalLayout.addWidget(self.b_get_time)
        self.p_fill = QtWidgets.QPushButton(self.widget)
        self.p_fill.setObjectName("p_fill")
        self.verticalLayout.addWidget(self.p_fill)
        self.b_clear = QtWidgets.QPushButton(self.widget)
        self.b_clear.setObjectName("b_clear")
        self.verticalLayout.addWidget(self.b_clear)
        self.horizontalLayout.addWidget(self.widget)
        self.graphicsView = CustomGraphicsView()
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 696, 21))
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
        self.comboBox.setItemText(0, _translate("MainWindow", "Без задержки"))
        self.comboBox.setItemText(1, _translate("MainWindow", "С задержкой"))
        self.groupBox.setTitle(_translate("MainWindow", "Добавление точки"))
        self.b_add_point.setText(_translate("MainWindow", "Добавить точку"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Выбор цвета"))
        self.b_choose_color.setText(_translate("MainWindow", "Выбрать цвет"))
        self.b_get_time.setText(_translate("MainWindow", "Замерить время"))
        self.p_fill.setText(_translate("MainWindow", "Закрасить"))
        self.b_clear.setText(_translate("MainWindow", "Очистить сцену"))
