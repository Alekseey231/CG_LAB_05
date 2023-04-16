import asyncio
import sys
import time
from typing import List

import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPen, QTransform, QPainter, QPixmap, QColor, QImage
from PyQt5.QtWidgets import QGraphicsScene, QTableWidgetItem, QMessageBox, QLabel, QApplication, QTableWidget, \
    QColorDialog, QAction
from fontTools.pens.qtPen import QtPen

from alg import fill_polygon, brezenhem_int
from alg_time import fill_polygon_time
from design_all import Ui_MainWindow


def create_error_window(title, message):
    error = QMessageBox()
    error.setWindowTitle(title)
    error.setText(message)
    error.exec()


# TODO вырождение в линию
# TODO Очистка сцены
class Main_window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.scene = QGraphicsScene()
        self.graphicsView.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.pointSignal.connect(self.add_point)
        self.graphicsView.endSignal.connect(self.complete_polygon)
        self.graphicsView.keySignal.connect(self.key_press)

        self.pen = QPen()
        self.color = QColor(Qt.green)

        self.l_choosen_color.setStyleSheet("background-color: green")
        self.l_choosen_color.clicked.connect(self.set_color)

        self.setup_toolbar()

        self.image = self.graphicsView.image
        self.image.fill(Qt.white)
        transform = QTransform()
        transform.translate(self.image.width() / 2,
                            self.image.height() / 2)  # смещение начала координат в центр изображения
        transform.scale(1, -1)  # инвертируем ось Y
        self.transform = transform
        self.p = QPainter()
        self.p.begin(self.image)
        self.p.setTransform(self.transform)
        self.p.setBrush(Qt.black)
        self.scene.addPixmap(QPixmap.fromImage(self.image))
        self.p.end()

        # self.all_polygon = [[PyQt5.QtCore.QPoint(-137, 124), PyQt5.QtCore.QPoint(-42, -97), PyQt5.QtCore.QPoint(72, 106), PyQt5.QtCore.QPoint(-137, 124)]]
        self.current_polygon = []
        self.all_polygon = []
        self.count_poly = 0
        self.cur_label = []

        self.init_table()
        # self.tableWidget.verticalHeader().setVisible(False)

        self.p_fill.clicked.connect(self.fill)

        self.b_clear.clicked.connect(self.clear_scene)
        self.b_choose_color.clicked.connect(self.set_color)
        self.b_add_point.clicked.connect(self.get_point)
        self.b_get_time.clicked.connect(self.get_time)

        # self.set_validators()

    def get_point(self):
        try:
            x = int(self.l_x.text())
            y = int(self.l_y.text())
        except Exception as e:
            create_error_window("Error!", "Некорретный ввод")
        else:
            self.add_point(QPoint(x, y))

    def set_color(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.l_choosen_color.setStyleSheet("background-color: {}".format(color.name()))
            self.color = color

    def init_table(self):
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(["x", "y"])

        self.tableWidget.horizontalHeaderItem(0).setToolTip("Column 1 ")
        self.tableWidget.horizontalHeaderItem(1).setToolTip("Column 2 ")
        self.tableWidget.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
        self.tableWidget.horizontalHeaderItem(1).setTextAlignment(Qt.AlignRight)

    def clear_scene(self):
        self.image.fill(Qt.transparent)
        self.tableWidget.setRowCount(0)
        self.image = QImage(5000, 5000, QImage.Format_ARGB32)
        self.image.fill(Qt.white)
        self.scene.clear()
        self.scene.addPixmap(QPixmap.fromImage(self.image))
        self.current_polygon = []
        self.all_polygon = []
        self.cur_label = []
        self.count_poly = 0

    def fill(self):
        if len(self.current_polygon):
            create_error_window("Error!", "Необходимо закончить ввод области перед заливкой")
            return
        if len(self.all_polygon) == 0:
            create_error_window("Error!", "Необходимо закончить ввод области перед заливкой")
            return
        # print(self.all_polygon)
        self.image.fill(Qt.white)
        for poly in self.all_polygon:

            for i in range(1, len(poly)):
                try:
                    self.draw_line(poly[i - 1], poly[i])
                except Exception as e:
                    print(e)
        if self.comboBox.currentIndex() == 0:
            if len(self.all_polygon) == 1:
                points = fill_polygon(self.all_polygon[0])
                self.draw_points_all(points)
            else:
                for poly in self.all_polygon:
                    points = fill_polygon(poly)
                    self.draw_points_all(points)
        else:
            for poly in self.all_polygon:
                self.draw_time(poly)
        # self.all_polygon = []

    def add_row(self, num1, num2):
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, QTableWidgetItem(str(num1)))
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, QTableWidgetItem(str(num2)))

    # shift - вертикальное ребро
    def key_press(self, point: QPoint, sign_type: int):
        if len(self.current_polygon) > 0:
            if sign_type == 0:
                point = QPoint(self.current_polygon[-1].x(), point.y())
            else:
                point = QPoint(point.x(), self.current_polygon[-1].y())
        self.add_point(point)

    def add_point(self, point: QPoint):
        if len(self.current_polygon) == 0:
            self.count_poly += 1
            self.cur_label.append("")
            self.add_row("Многоугольник №" + str(self.count_poly), "")
            self.tableWidget.setSpan(self.tableWidget.rowCount() - 1, 0, 1, 2)
            self.tableWidget.setVerticalHeaderLabels(self.cur_label)
        self.current_polygon.append(point)
        self.cur_label.append(str(len(self.current_polygon)))
        self.add_row(point.x(), point.y())
        self.tableWidget.setVerticalHeaderLabels(self.cur_label)
        if len(self.current_polygon) == 1:
            try:
                self.draw_point(point)
            except Exception as e:
                print(e)
        else:
            self.draw_line(self.current_polygon[-1], self.current_polygon[-2])

    def complete_polygon(self, int):
        if len(self.current_polygon) < 3:
            create_error_window("Error!", "Полигон должен состоять минимум из 3-х точек!")
        else:
            # self.count_poly += 1
            # self.cur_label.append("")

            # self.add_row("Многоугольник №" + str(self.count_poly), "")
            # self.tableWidget.setSpan(self.tableWidget.rowCount() - 1, 0, 1, 2)
            # self.tableWidget.setVerticalHeaderLabels(self.cur_label)

            self.current_polygon.append(self.current_polygon[0])
            self.draw_line(self.current_polygon[-1], self.current_polygon[-2])
            self.all_polygon.append(self.current_polygon)
            self.current_polygon = []

            # print(self.all_polygon)

    def draw_point(self, point: QPoint):

        black = QColor(0, 0, 0)
        self.image.setPixel(round(point.x()) + self.image.width() // 2, round(point.y()) * -1 + self.image.width() // 2,
                            black.rgb())

        self.scene.clear()
        self.scene.addPixmap(QPixmap.fromImage(self.image))

    def draw_line(self, start_point: QPoint, end_point: QPoint):
        self.p.begin(self.image)
        self.p.setTransform(self.transform)
        self.p.setPen(self.pen)

        # self.p.drawLine(start_point, end_point)
        self.my_draw_line(start_point, end_point)

        self.scene.clear()
        self.scene.addPixmap(QPixmap.fromImage(self.image))
        self.p.end()

    def my_draw_line(self, start_point, end_point):
        all_points = brezenhem_int(start_point, end_point)
        black = QColor(0, 0, 0)
        for point in all_points:
            self.image.setPixel(round(point[0]) + self.image.width() // 2,
                                (round(point[1]) * -1 + self.image.width() // 2),
                                black.rgb())

    def draw_time(self, poly):
        gen = fill_polygon_time(poly)
        try:
            count = 0
            for row in gen:
                self.draw_points_normaly(row)
                count += 1
                self.graphicsView.update()
                QApplication.processEvents()
                time.sleep(0.0001)

        except Exception as e:
            print(e)

    def draw_points_all(self, all_points: list):
        white = QColor(255, 255, 255)
        black = QColor(0, 0, 0)
        # green = QColor(0, 255, 0)
        green = self.color

        for point in all_points:
            color = QColor(self.image.pixel(round(point[0]) + self.image.width() // 2,
                                            (round(point[1]) * -1 + self.image.width() // 2)))

            if color.rgb() == white.rgb():
                self.image.setPixel(round(point[0]) + self.image.width() // 2,
                                    (round(point[1]) * -1 + self.image.width() // 2),
                                    green.rgb())
            elif color.rgb() == black.rgb():
                pass
            else:
                self.image.setPixel(round(point[0]) + self.image.width() // 2,
                                    (round(point[1]) * -1 + self.image.width() // 2),
                                    white.rgb())

        self.scene.clear()
        self.scene.addPixmap(QPixmap.fromImage(self.image))

    def draw_points_normaly(self, all_points: list):
        white = QColor(255, 255, 255)
        black = QColor(0, 0, 0)
        # green = QColor(0, 255, 0)
        green = self.color

        for point in all_points:
            color = QColor(self.image.pixel(round(point[0]) + self.image.width() // 2,
                                            (round(point[1]) * -1 + self.image.width() // 2)))

            if color.rgb() == white.rgb():
                self.image.setPixel(round(point[0]) + self.image.width() // 2,
                                    (round(point[1]) * -1 + self.image.width() // 2),
                                    green.rgb())
            elif color.rgb() == black.rgb():
                pass
            else:
                self.image.setPixel(round(point[0]) + self.image.width() // 2,
                                    (round(point[1]) * -1 + self.image.width() // 2),
                                    white.rgb())

        self.scene.clear()
        self.scene.addPixmap(QPixmap.fromImage(self.image))

    def draw_points(self, all_points: list):
        new_image = QImage(self.image.width(), self.image.height(), QImage.Format_ARGB32)
        new_image.fill(Qt.transparent)
        white = QColor(255, 255, 255, 255)
        black = QColor(0, 0, 0, 255)
        green = self.color
        try:
            for point in all_points:

                color = new_image.pixel(round(point[0]) + new_image.width() // 2,
                                        (round(point[1]) * -1 + new_image.width() // 2))

                if is_transparent(color) or QColor(color).rgb() == white.rgb():
                    new_image.setPixel(round(point[0]) + new_image.width() // 2,
                                       (round(point[1]) * -1 + new_image.width() // 2),
                                       green.rgba())
                else:
                    new_image.setPixel(round(point[0]) + new_image.width() // 2,
                                       (round(point[1]) * -1 + new_image.width() // 2),
                                       0)
        except Exception as e:
            print(e)
        try:

            self.p.begin(self.image)
            self.p.setCompositionMode(QPainter.CompositionMode_SourceOver)
            self.p.drawImage(0, 0, new_image)

            # self.p.end()
        except Exception as e:
            print(e)

        self.scene.clear()
        self.scene.addPixmap(QPixmap.fromImage(self.image))
        # self.image = res_image

    def get_time(self):
        self.comboBox.setCurrentIndex(0)
        start_time = time.time()
        self.fill()
        end_time = time.time()
        try:
            create_error_window("Замеры времени: ", "{:.3f}".format(end_time - start_time))
        except Exception as e:
            print(e)

    def setup_toolbar(self):
        close = QAction('О программе', self)
        close.triggered.connect(self.about_program)
        self.toolbar = self.addToolBar("О программе")
        self.toolbar.addAction(close)

        close = QAction('Об авторе', self)
        close.triggered.connect(self.about_author)
        self.toolbar = self.addToolBar("Об авторе")
        self.toolbar.addAction(close)

        close = QAction('Справка', self)
        close.triggered.connect(self.info)
        self.toolbar = self.addToolBar("Справка")
        self.toolbar.addAction(close)

        close = QAction('Закрыть', self)
        close.triggered.connect(self.close)
        self.toolbar = self.addToolBar("Закрыть")
        self.toolbar.addAction(close)

    def about_author(self):
        create_error_window("Об авторе", "Толмачев Алексей; ИУ7-45B")

    def about_program(self):
        create_error_window("О программе",
                            "Реализован алгоритм заполнения области по ребрам")

    def info(self):
        create_error_window("Справка",
                            "1) Ввод точек на графическую сцену осуществляется с помощью левой кнопки мыши или с помощью "
                            "ввода в соответствующие поля координат в интерфейсе\n "
                            "2) С помощью правой кнопки мыши можно замкнуть область\n"
                            "3) Для того, чтобы построить вертикальное ребро - после ввода точки нужно удерживать "
                            "shift при вводе следующей точки\n"
                            "4) Для построения горизонтального ребра нужно удерживать Ctrl при вводе следующей точки\n")


def compare_colors(color1, color2):
    """Compare two colors and return True if they are equal, False otherwise."""
    return (color1.red() == color2.red() and
            color1.green() == color2.green() and
            color1.blue() == color2.blue() and
            color1.alpha() == color2.alpha())


def is_transparent(pixel_value):
    alpha = (pixel_value >> 24) & 0xFF  # значение альфа-канала
    if alpha == 0:
        return True
    else:
        red = (pixel_value >> 16) & 0xFF  # значение красного канала
        green = (pixel_value >> 8) & 0xFF  # значение зеленого канала
        blue = pixel_value & 0xFF  # значение синего канала
        # if red == 0 and green == 0 and blue == 0:

        # else:
        # print("Пиксель цветной")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    form = Main_window()
    form.show()
    try:
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
