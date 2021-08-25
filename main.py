from time import sleep
from datetime import datetime


TIME_RELATION = pow(59,3)/(pow(60,2)*24)

def currentDaySecondStandardTime() -> float:
    now = datetime.now()
    return (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()

def clock59()-> int:
    currentSeconds = currentDaySecondStandardTime() * TIME_RELATION
    currentHour = currentSeconds/ pow(59,2)
    currentMinute = (59/100) * ((currentHour - int(currentHour)) * 100)
    currentSecond = (59/100) * ((currentMinute - int(currentMinute)) * 100)
    return [int(currentHour), int(currentMinute), int(currentSecond)]

def printTime(time:list)->None:
    timeWithFormat = list(map(lambda x: x if x > 9 else f"0{x}" , time))
    timeToPrint = (f"{time[0]}:{timeWithFormat[1]}:{timeWithFormat[2]} ")
    print(timeToPrint, end = "\r")
    return timeToPrint

def toFile(fileName:str, str:str)->None:
    with open(fileName, "w") as myfile:
        myfile.write(str)

def main() -> int:
    
    while True:
        time = clock59()
        timeToPrint = printTime(time)
        toFile("clock59.txt", timeToPrint)
        sleep(pow(TIME_RELATION, -1))
    return 1

if __name__ == '__main__':
    main()
