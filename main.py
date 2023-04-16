import sys
from typing import List

import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPen, QTransform, QPainter, QPixmap, QColor, QImage
from PyQt5.QtWidgets import QGraphicsScene, QTableWidgetItem, QMessageBox
from fontTools.pens.qtPen import QtPen

from alg import fill_polygon, brezenhem_int
from design_all import Ui_MainWindow


def create_error_window(title, message):
    error = QMessageBox()
    error.setWindowTitle(title)
    error.setText(message)
    error.exec()


class Main_window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.scene = QGraphicsScene()
        self.graphicsView.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.pointSignal.connect(self.add_point)
        self.graphicsView.endSignal.connect(self.complete_polygon)
        self.pen = QPen()
        self.pen.setColor(Qt.green)

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

        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(["x", "y"])

        self.tableWidget.horizontalHeaderItem(0).setToolTip("Column 1 ")
        self.tableWidget.horizontalHeaderItem(1).setToolTip("Column 2 ")
        self.tableWidget.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
        self.tableWidget.horizontalHeaderItem(1).setTextAlignment(Qt.AlignRight)
        self.add_row(10, 15)
        self.add_row(20, 20)

        self.p_fill.clicked.connect(self.fill)
        # print(self.tableWidget.item().text())

        # self.tableWidget.insertColumn(self.tableWidget.rowCount())
        # self.tableWidget.insertColumn(self.tableWidget.rowCount())
        # self.tableWidget.insertRow(self.tableWidget.rowCount())

        # self.set_validators()

    def fill(self):
        if len(self.all_polygon) == 1:
            points = fill_polygon(self.all_polygon[0])
            self.draw_points(points)
        else:
            for poly in self.all_polygon:
                points = fill_polygon(poly)
                self.draw_points_normaly(points)

        """
        for poly in self.all_polygon:
            for i in range(1, len(poly)):
                try:
                    self.draw_line(poly[i - 1], poly[i])
                except Exception as e:
                    print(e)"""

    def add_row(self, num1, num2):
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, QTableWidgetItem(str(num1)))
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, QTableWidgetItem(str(num2)))

    def add_point(self, point: QPoint):
        self.current_polygon.append(point)
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
            self.current_polygon.append(self.current_polygon[0])
            self.draw_line(self.current_polygon[-1], self.current_polygon[-2])
            self.all_polygon.append(self.current_polygon)
            self.current_polygon = []
            print(self.all_polygon)

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

    def draw_points_normaly(self, all_points: list):
        # self.image.fill(Qt.white)
        #new_image = QImage(self.image.width(), self.image.height(), QImage.Format_ARGB32)
        #new_image.fill(Qt.transparent)

        #res_image = QImage(self.image.width(), self.image.height(), QImage.Format_ARGB32)
        #res_image.fill(Qt.transparent)
        # print(self.p.pen().color().getRgb())
        white = QColor(255, 255, 255)
        black = QColor(0, 0, 0)
        green = QColor(0, 255, 0)
        # print(color.rgb())
        # self.image.setPixel(0 + self.image.width() / 2, 0 + self.image.width() / 2, self.p.pen().color().rgb())

        # color = QColor(self.image.pixel(0, 0))
        # print(color.getRgb())

        # print(QColor(self.image.pixel(0, 0)).getRgb() == (255, 255, 255, 255))

        for point in all_points:
            color = QColor(self.image.pixel(round(point[0]) + self.image.width() // 2,
                                           (round(point[1]) * -1 + self.image.width() // 2)))

            if color.rgb() == white.rgb():
                self.image.setPixel(round(point[0]) + self.image.width() // 2,
                                   (round(point[1]) * -1 + self.image.width() // 2),
                                   green.rgb())
            else:
                self.image.setPixel(round(point[0]) + self.image.width() // 2,
                                   (round(point[1]) * -1 + self.image.width() // 2),
                                   white.rgb())
        try:

            #self.p.begin(self.image)
            #self.p.setCompositionMode(QPainter.CompositionMode_SourceOver)
            #self.p.drawImage(0, 0, new_image)


            self.all_polygon = []

            #self.p.end()
        except Exception as e:
            print(e)

        self.scene.clear()
        self.scene.addPixmap(QPixmap.fromImage(self.image))
        #self.image = res_image



    def draw_points(self, all_points: list):
        # self.image.fill(Qt.white)
        new_image = QImage(self.image.width(), self.image.height(), QImage.Format_ARGB32)
        new_image.fill(Qt.transparent)

        # res_image = QImage(self.image.width(), self.image.height(), QImage.Format_ARGB32)
        # res_image.fill(Qt.transparent)
        # print(self.p.pen().color().getRgb())
        white = QColor(255, 255, 255, 255)
        black = QColor(0, 0, 0, 255)
        green = QColor(0, 255, 0, 255)
        # print(color.rgb())
        # self.image.setPixel(0 + self.image.width() / 2, 0 + self.image.width() / 2, self.p.pen().color().rgb())

        # color = QColor(self.image.pixel(0, 0))
        # print(color.getRgb())

        # print(QColor(self.image.pixel(0, 0)).getRgb() == (255, 255, 255, 255))
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

            self.all_polygon = []

            # self.p.end()
        except Exception as e:
            print(e)

        self.scene.clear()
        self.scene.addPixmap(QPixmap.fromImage(self.image))
        # self.image = res_image


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