from time import sleep
from datetime import datetime
import sys
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer, Qt, QPoint, QSize
from PyQt5.QtGui import QFont, QPainter, QColor, QPen


TIME_RELATION = pow(59,3)/(pow(60,2)*24)

def currentDaySecondStandardTime() -> float:
    now = datetime.now()
    return (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()

def clock59()-> list:
    currentSeconds = currentDaySecondStandardTime() * TIME_RELATION
    currentHour = currentSeconds/ pow(59,2)
    currentMinute = (59/100) * ((currentHour - int(currentHour)) * 100)
    currentSecond = (59/100) * ((currentMinute - int(currentMinute)) * 100)
    return [int(currentHour), int(currentMinute), int(currentSecond)]

def formatTime(time:list)->str:
    timeWithFormat = list(map(lambda x: x if x > 9 else f"0{x}" , time))
    return f"{time[0]}:{timeWithFormat[1]}:{timeWithFormat[2]}"

def printTime(time:list)->str:
    timeToPrint = formatTime(time) + " "
    print(timeToPrint, end = "\r")
    return timeToPrint

def toFile(fileName:str, str:str)->None:
    with open(fileName, "w") as myfile:
        myfile.write(str)

class AnalogClock59Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.hour = 0
        self.minute = 0
        self.second = 0
        # Set minimum size for the widget
        self.setMinimumSize(200, 200)
        
    def setTime(self, time_list):
        self.hour = time_list[0]
        self.minute = time_list[1]
        self.second = time_list[2]
        self.update()  # Trigger a repaint
        
    def paintEvent(self, event):
        side = min(self.width(), self.height())
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Move the coordinate system to the center of the widget
        painter.translate(self.width() / 2, self.height() / 2)
        # Scale the coordinate system
        painter.scale(side / 200.0, side / 200.0)
        
        self.drawClockFace(painter)
        self.drawHands(painter)
        
    def drawClockFace(self, painter):
        # Draw the clock face (circle)
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        painter.drawEllipse(QPoint(0, 0), 90, 90)
        
        # Draw hour markers
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        for i in range(59):
            angle = i * 6.1  # 360 degrees / 59 segments = ~6.1 degrees per marker
            # Longer lines for every 5th marker
            if i % 5 == 0:
                outer_radius = 90
                inner_radius = 75
            else:
                outer_radius = 90
                inner_radius = 85
                
            x1 = int(inner_radius * -1 * (angle / 360.0) * 6.283)
            y1 = int(inner_radius * (angle / 360.0) * 6.283)
            x2 = int(outer_radius * -1 * (angle / 360.0) * 6.283)
            y2 = int(outer_radius * (angle / 360.0) * 6.283)
            
            painter.drawLine(x1, y1, x2, y2)
            
    def drawHands(self, painter):
        # Draw hour hand
        hour_angle = (self.hour * 360.0 / 59) + (self.minute * 360.0 / (59 * 59))
        hour_length = 50
        painter.setPen(QPen(QColor(0, 0, 255), 4))  # Blue hand
        self.drawHand(painter, hour_angle, hour_length)
        
        # Draw minute hand
        minute_angle = (self.minute * 360.0 / 59) + (self.second * 360.0 / (59 * 59))
        minute_length = 70
        painter.setPen(QPen(QColor(0, 127, 0), 3))  # Green hand
        self.drawHand(painter, minute_angle, minute_length)
        
        # Draw second hand
        second_angle = self.second * 360.0 / 59
        second_length = 80
        painter.setPen(QPen(QColor(255, 0, 0), 2))  # Red hand
        self.drawHand(painter, second_angle, second_length)
        
        # Draw a small circle at the center
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        painter.setBrush(QColor(0, 0, 0))
        painter.drawEllipse(QPoint(0, 0), 5, 5)
        
    def drawHand(self, painter, angle, length):
        angle = angle - 90  # Adjust for default coordination system (0 degrees at 3 o'clock)
        radians = angle * 3.14159265358979323846 / 180.0
        x = length * -1 * -math.cos(radians)
        y = length * -math.sin(radians)
        painter.drawLine(0, 0, int(x), int(y))

class Clock59Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Set window properties
        self.setWindowTitle('59Times Clock')
        self.setGeometry(300, 300, 300, 400)  # Made the window taller to accommodate both clocks
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout(central_widget)
        
        # Create analog clock widget
        self.analog_clock = AnalogClock59Widget()
        layout.addWidget(self.analog_clock)
        
        # Create time label
        self.time_label = QLabel('', self)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setFont(QFont('Arial', 36, QFont.Bold))
        layout.addWidget(self.time_label)
        
        # Create timer to update the time
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(int(pow(TIME_RELATION, -1) * 1000))  # Convert to milliseconds
        
        # Initial time update
        self.updateTime()
        
    def updateTime(self):
        time = clock59()
        timeToPrint = printTime(time)
        self.time_label.setText(timeToPrint)
        self.analog_clock.setTime(time)  # Update the analog clock
        toFile("clock59.txt", timeToPrint)

def main() -> int:
    app = QApplication(sys.argv)
    window = Clock59Window()
    window.show()
    return app.exec_()

if __name__ == '__main__':
    main()
