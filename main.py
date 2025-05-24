from time import sleep
from datetime import datetime
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont


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

class Clock59Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Set window properties
        self.setWindowTitle('59Times Clock')
        self.setGeometry(300, 300, 300, 150)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout(central_widget)
        
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
        toFile("clock59.txt", timeToPrint)

def main() -> int:
    app = QApplication(sys.argv)
    window = Clock59Window()
    window.show()
    return app.exec_()

if __name__ == '__main__':
    main()
