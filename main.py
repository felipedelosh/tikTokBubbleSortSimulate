"""
FelipedelosH

2024 - 03 - 13
TikTok

Open a mobile interface and manipulate bubbleSort ALG
"""

from tkinter import *
from random import randint
from threading import *
from time import sleep


class GraphiBubbleSort:
    def __init__(self):
        self._max_x = 540 # width
        self._max_y = 800 # Heigth
        self._sleepTime = 0.01
        self.screem = Tk()
        self.canvasController = Canvas(self.screem, width=self._max_x, height=self._max_y/5, bg="snow")
        self.canvasGraphics = Canvas(self.screem, width=self._max_x, height=self._max_y*0.8, bg="black")
        self.lblNumbersQTY = Label(self.canvasController, text="Insert number QTY: ")
        self.txtNumbersQTY = Entry(self.canvasController, width=6)
        self.btnPlay = Button(self.canvasController, text="PLAY", command=self.play)
        self.btnPause = Button(self.canvasController, text="PAUSE", command=self.pause)
        self.btnReStart = Button(self.canvasController, text="RE-START", command=self.restart)
        self.lblIteration = Label(self.canvasController, text="Iteracion: 0")
        self.lblALG = Label(self.canvasController, text="ALG")

        """Vars"""
        self.iterator = 0
        self._swapsCounter = 0
        self._counter_btn_play_presed = 0
        self.counter_resolver_alg = 0
        self.arrNumbers = []  # Save numbers 640
        self.isRunALG = False  # program  running?

        self.thread = Thread(target=self.run)
        """Preparate launch"""
        self.thread.start()
        self.initArrNumbersDefault()
        self.lenArrNumbers = len(self.arrNumbers)
        self._iCounter = 0
        self._jCounter = 0
        self.dx_item_number_x = self._max_x / self.lenArrNumbers # to graficate numbers in axis x
        self._maxValueInArrNumbers = max(self.arrNumbers) * 1.05
        self._pivot0 = 0 # paint Travel into array arr[j]
        self._pivot1 = 0 # paint Travel into array arr[j+1]
        self._temp = None # To swap

        """Se muestra todo"""
        self.showAndConfigureDisplay()


    def showAndConfigureDisplay(self):
        self.screem.title("BubbleSort By FelipedelosH")
        self.screem.geometry(f"{self._max_x}x{self._max_y}")
        self.canvasController.place(x=0, y=0)
        self.canvasController.create_line(self._max_x*0.38, 0, self._max_x*0.38, self._max_y*0.2)
        self.lblNumbersQTY.place(x=10, y=10)
        self.txtNumbersQTY.place(x=120, y=12)
        self.lblALG.place(x=self._max_x*0.55, y=20)
        self.btnPlay.place(x=10, y=self._max_y*0.15)
        self.btnPause.place(x=60, y=self._max_y*0.15)
        self.btnReStart.place(x=110, y=self._max_y*0.15)
        self.lblIteration.place(x=10, y=50)
        self.canvasGraphics.place(x=0, y=self._max_y*0.2)
        self.showArrayNumbers()
        self.screem.after(0, self.update_graphic)


        self.screem.mainloop()

    def showALG(self):
        # Not optimal bubble sort
        if True:
            txt = f"Total numbers: {self.lenArrNumbers}\n"
            txt = txt + f"Iterations: {self.iterator} of {self.lenArrNumbers**2}\n"
            txt = txt + f"Swaps: {self._swapsCounter}\n"
            txt = txt + f"Comparate: {self.arrNumbers[self._pivot0]}:{self.arrNumbers[self._pivot1]}\n"
        
        
        self.lblALG['text'] = txt


    def calculateKons(self):
        self.lenArrNumbers = len(self.arrNumbers)
        self.dx_item_number_x = self._max_x / self.lenArrNumbers 
        self._maxValueInArrNumbers = max(self.arrNumbers) * 1.05
        self._pivot0 = 0 
        self._pivot1 = 0
        self._temp = None

    def initArrNumbersDefault(self):
        if not self.isRunALG:
            self.arrNumbers.clear()
            for i in range(100):
                self.arrNumbers.append(randint(8, 999))

    def initArrNumbers(self, qty):
        if not self.isRunALG:
            self.arrNumbers.clear()
            for i in range(qty):
                self.arrNumbers.append(randint(8, 999))

    def update_graphic(self):
        if self.isRunALG:
            self.showArrayNumbers()
            self.showALG()
            self.lblIteration["text"] = "Iteracion: " + str(self.iterator)
        self.screem.after(30, self.update_graphic)

    def showArrayNumbers(self):
        self.canvasGraphics.delete("arr")
        for i in range(0, self.lenArrNumbers):
            x0 = self.dx_item_number_x * i
            x1 = x0 + self.dx_item_number_x
            y0 = self._max_y
            dy = self.arrNumbers[i]/self._maxValueInArrNumbers
            y1 = self._max_y * dy

            if i == self._pivot0 or i == self._pivot1 and self.isRunALG:    
                self.canvasGraphics.create_rectangle(
                    x0,
                    y0,
                    x1,
                    y1,
                    fill="red",
                    tags="arr"
                )
                self.canvasGraphics.create_rectangle(
                    x0,
                    y1,
                    x1,
                    0,
                    fill="yellow",
                    tags="arr"
                )
            else:
                self.canvasGraphics.create_rectangle(
                    x0,
                    y1,
                    x1,
                    y0,
                    fill="green",
                    tags="arr"
                )


            if self.iterator >= (self.lenArrNumbers**2)-self.lenArrNumbers:
                print("Epaaa")


    def play(self):
        self.isRunALG = False


        if self._counter_btn_play_presed == 0:
            self.isRunALG = True
            if not self.isValidQtyOfNumbers():
                self.screem.title("Bubble Sort Error in input NQty")
            else:
                self.screem.title(f"Bubble Sort Default")
        else:
            if self.isValidQtyOfNumbers() and self._counter_btn_play_presed != 0:
                self.initArrNumbers(int(self.txtNumbersQTY.get()))
                self.calculateKons()
                self.cleanTxt()
                self.isRunALG = True
                self.screem.title("Bubble Sort By FelipedelosH")
            else:
                self.screem.title("Bubble Sort Error in input NQty")
                self.isRunALG = False

            if self.counter_resolver_alg == 0:
                self.isRunALG = True
        
        self._counter_btn_play_presed = self._counter_btn_play_presed + 1
        

    def pause(self):
        self.screem.title("Burbuja by loko:PAUSE")
        self.isRunALG = False

    def restart(self):
        self.isRunALG = False
        self._iCounter = 0
        self._jCounter = 0
        k = randint(33, 99)
        self.initArrNumbers(k)
        self.calculateKons()
        self._pivot0 = 0
        self._pivot1 = 0
        self.iterator = 0
        self.lblALG['text'] = "ALG"
        self.showArrayNumbers()
        


    def run2(self):
        self.iterator = 0 # Count total program times need to sort
        while True:
            try:
                while self.isRunALG and self._iCounter < self.lenArrNumbers:
                    self._jCounter = 0
                    while self.isRunALG and self._jCounter < len(self.arrNumbers) - (self._iCounter + 1):
                        self._pivot0 = self._jCounter
                        self._pivot1 = self._jCounter + 1
                        if (self.arrNumbers[self._jCounter] < self.arrNumbers[self._jCounter + 1]):
                            aux = self.arrNumbers[self._jCounter + 1]
                            self.arrNumbers[self._jCounter + 1] = self.arrNumbers[self._jCounter]
                            self.arrNumbers[self._jCounter] = aux

                        self.iterator += 1
                        self._jCounter = self._jCounter + 1

                    sleep(self._sleepTime)

                    if self.isRunALG:
                        self._iCounter = self._iCounter + 1
            except:
                sleep(0.3)


   
    def run(self):
        self.iterator = 0
        while True:
            try:
                while self.isRunALG:
                    for _ in range(0, len(self.arrNumbers)):
                        for j in range(0, len(self.arrNumbers)-1):     
                            self._pivot0 = j
                            self._pivot1 = j+1
                            if self.arrNumbers[j] < self.arrNumbers[j+1]:
                                self._temp = self.arrNumbers[j]
                                self.arrNumbers[j] = self.arrNumbers[j+1]
                                self.arrNumbers[j+1] = self._temp
                                self._swapsCounter = self._swapsCounter + 1
                            sleep(self._sleepTime)
                            self.iterator = self.iterator + 1

                    self.counter_resolver_alg = self.counter_resolver_alg + 1
                    self.isRunALG = False
            except:
                sleep(0.3)


    def cleanTxt(self):
        self.txtNumbersQTY.set("")


    def isValidQtyOfNumbers(self):
        try:
            return int(self.txtNumbersQTY.get()) > 0
        except:
            return False

sw = GraphiBubbleSort()