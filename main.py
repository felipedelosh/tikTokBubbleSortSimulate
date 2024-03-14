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
        self.btnPlay = Button(self.canvasController, text="PLAY", command=self.play)
        self.btnPause = Button(self.canvasController, text="PAUSE", command=self.pause)
        self.btnReStart = Button(self.canvasController, text="RE-START", command=self.restart)
        self.lblIteration = Label(self.canvasController, text="Iteracion: 0")
        self.lblALG = Label(self.canvasController, text="ALG")

        """Vars"""
        self.iterator = 0
        self._swapsCounter = 0
        self.arrNumbers = []  # Save numbers 640
        self.isRunALG = False  # program  running?

        self.thread = Thread(target=self.run)
        """Preparate launch"""
        self.thread.start()
        self.initArrNumbers()
        self.dx_item_number_x = self._max_x / len(self.arrNumbers) # to graficate numbers in axis x
        self._maxValueInArrNumbers = max(self.arrNumbers)
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
            txt = f"Total numbers: {len(self.arrNumbers)}\n"
            txt = txt + f"Iterations: {self.iterator} of {len(self.arrNumbers)**2}\n"
            txt = txt + f"Swaps: {self._swapsCounter}\n"
            txt = txt + f"Comparate: {self.arrNumbers[self._pivot0]}:{self.arrNumbers[self._pivot1]}\n"
        
        
        self.lblALG['text'] = txt

    def initArrNumbers(self):
        if not self.isRunALG:
            self.arrNumbers.clear()
            for i in range(40):
                self.arrNumbers.append(randint(1, 999))

    def update_graphic(self):
        if self.isRunALG:
            self.showArrayNumbers()
            self.showALG()
            self.lblIteration["text"] = "Iteracion: " + str(self.iterator)
        self.screem.after(30, self.update_graphic)

    def showArrayNumbers(self):
        self.canvasGraphics.delete("arr")
        for i in range(0, len(self.arrNumbers)):
            x0 = self.dx_item_number_x * i
            x1 = x0 + self.dx_item_number_x
            y0 = 0
            y1 = (self.arrNumbers[i]/self._maxValueInArrNumbers) * self._max_y 

            if i == self._pivot0 or i == self._pivot1:    
                self.canvasGraphics.create_rectangle(
                    x0,
                    y1,
                    x1,
                    y0,
                    fill="red",
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


    def play(self):
        self.screem.title("Burbuja by loko:PLAY")
        self.isRunALG = True

    def pause(self):
        self.screem.title("Burbuja by loko:PAUSE")
        self.isRunALG = False

    def restart(self):
        self.isRunALG = False
        self.initArrNumbers()
        self._pivot0 = 0
        self._pivot1 = 0
        self.iterator = 0
        self.lblALG['text'] = "ALG"


    def run2(self):
        iCounter = 0
        jCounter = 0
        aux = 0
        self.iterator = 0 # Count total program times need to sort
        while True:
            while self.isRunALG and iCounter < len(self.arrNumbers):
                jCounter = 0
                while self.isRunALG and jCounter < len(self.arrNumbers) - (iCounter + 1):
                    self._pivot0 = jCounter
                    self._pivot1 = jCounter+1
                    if (self.arrNumbers[jCounter] < self.arrNumbers[jCounter + 1]):
                        aux = self.arrNumbers[jCounter + 1]
                        self.arrNumbers[jCounter + 1] = self.arrNumbers[jCounter]
                        self.arrNumbers[jCounter] = aux

                    self.iterator += 1
                    jCounter = jCounter + 1

                sleep(self._sleepTime)
                """Se incrementa i"""
                if self.isRunALG:
                    iCounter = iCounter + 1

   
    def run(self):
        self.iterator = 0
        while True:
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

                self.isRunALG = False


sw = GraphiBubbleSort()