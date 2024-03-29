"""
FelipedelosH

2024 - 03 - 13
TikTok

Open a mobile interface and manipulate bubbleSort ALG
"""

from tkinter import *
from tkinter import ttk
import random
from threading import *
from time import sleep


_isSystemAudioEnabled = False

try:
    import winsound
    _isSystemAudioEnabled = False
except:
    print("Error: windows sound library not found.")
 

class GraphicSortAGL:
    def __init__(self):
        self._max_x = 540 # width
        self._max_y = 800 # Heigth
        self._sleepTime = 0.01
        self.screem = Tk()
        self.canvasController = Canvas(self.screem, width=self._max_x, height=self._max_y/5, bg="snow")
        self.canvasGraphics = Canvas(self.screem, width=self._max_x, height=self._max_y*0.8, bg="black")
        self.txt_alg_cbx_selection = StringVar(value='Brute Bubble Sort')
        self.alg_registred = ['Brute Bubble Sort', 'Optimal Bubble Sort']
        self.cbx_selected_alg = ttk.Combobox(self.canvasController, textvariable=self.txt_alg_cbx_selection, state='readonly')
        self.cbx_selected_alg['values'] = self.alg_registred
        self.cbx_selected_alg.bind('<<ComboboxSelected>>', self.cbx_changed)
        self.lblNumbersQTY = Label(self.canvasController, text="Insert number QTY: ")
        self.txtNumbersQTY = Entry(self.canvasController, width=6)
        self.lblTimeSleep = Label(self.canvasController, text="Velocity = 100%")
        self.sliderTimeSleep = Scale(self.canvasController, from_=0, to=100, orient="horizontal", command=self.modifyTimeSleep)
        self.sliderTimeSleep.set(50)
        self.btnPlay = Button(self.canvasController, text="PLAY", command=self.play)
        self.btnPause = Button(self.canvasController, text="PAUSE", command=self.pause)
        self.btnReStart = Button(self.canvasController, text="RE-START", command=self.restart)
        self.lblALG = Label(self.canvasController, text="ALG")

        """Vars"""
        self.iterator = 0
        self._swapsCounter = 0
        self._counter_btn_play_presed = 0
        self.counter_resolver_alg = 0
        self.arrNumbers = []  # Save numbers 640
        self._pressed_play = False  # program  running?
        self._pressed_pause = False

        self.thread = Thread(target=self.run)
        """Preparate launch"""
        self.thread.start()
        self.initArrNumbersDefault()
        self.lenArrNumbers = len(self.arrNumbers)
        self._iCounter = 0
        self._jCounter = 0
        self.dx_item_number_x = self._max_x / self.lenArrNumbers # to graficate numbers in axis x
        self._maxValueInArrNumbers = max(self.arrNumbers) * 1.05
        self.var_calc_max_iterators = 0
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
        self.cbx_selected_alg.place(x=220, y=12)
        self.lblNumbersQTY.place(x=10, y=10)
        self.txtNumbersQTY.place(x=120, y=12)
        self.lblTimeSleep.place(x=10, y=40)
        self.sliderTimeSleep.place(x=10, y=60)
        self.lblALG.place(x=self._max_x*0.55, y=60)
        self.btnPlay.place(x=10, y=self._max_y*0.15)
        self.btnPause.place(x=60, y=self._max_y*0.15)
        self.btnReStart.place(x=110, y=self._max_y*0.15)
        self.canvasGraphics.place(x=0, y=self._max_y*0.2)
        self.showArrayNumbers()
        self.screem.after(0, self.update_graphic)


        self.screem.mainloop()

    def showALG(self):
        if self._pressed_play:
            # Not optimal bubble sort
            if str(self.txt_alg_cbx_selection.get()) == self.alg_registred[0]:
                txt = f"Total numbers: {self.lenArrNumbers}\n"
                txt = txt + f"Iterations: {self.iterator} of {self.var_calc_max_iterators}\n"
                txt = txt + f"Swaps: {self._swapsCounter}\n"
                txt = txt + f"Comparate: {self.arrNumbers[self._pivot0]}:{self.arrNumbers[self._pivot1]}\n"
                self.lblALG['text'] = txt


            if str(self.txt_alg_cbx_selection.get()) == self.alg_registred[1]:
                txt = f"Total numbers: {self.lenArrNumbers}\n"
                txt = txt + f"Iterations: {self.iterator} of {self.var_calc_max_iterators}\n"
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
        self.calculateMaxIterators()

    def modifyTimeSleep(self, value):
        k = int(value)
        self.lblTimeSleep['text'] = f"Velocity = {value}%"
        if k > 80:
            self.lblTimeSleep['text'] = "Velocity = HiGh SpEed"
        elif k > 50:
            self.lblTimeSleep['text'] = "Velocity = Medium Speed"
        elif k > 30:
            self.lblTimeSleep['text'] = "Velocity = Moderate"
        elif k > 10:
            self.lblTimeSleep['text'] = "Velocity = Slow"
        elif k > 2:
            self.lblTimeSleep['text'] = "Velocity = Too Slow"
        elif k >= 0:
            self.lblTimeSleep['text'] = "Velocity = -272C"

        self._sleepTime = 0.005 + (0.1 * (1-(k/100)))


    def initArrNumbersDefault(self):
        self.arrNumbers.clear()
        for i in range(100):
            self.arrNumbers.append(i)
        mixArrNumbers = self.arrNumbers.copy()
        random.shuffle(mixArrNumbers)
        self.arrNumbers = mixArrNumbers

    def calculateMaxIterators(self):
        # Brute bubble sort
        if str(self.txt_alg_cbx_selection.get()) == self.alg_registred[0]:
            _sum = 0
            for i in range(self.lenArrNumbers):
                _sum = _sum + self.lenArrNumbers - 1
            self.var_calc_max_iterators = _sum

        # Optimal
        if str(self.txt_alg_cbx_selection.get()) == self.alg_registred[1]:
            _sum = 0
            for i in range(self.lenArrNumbers):
                _sum = _sum + i
            self.var_calc_max_iterators = _sum

        

    def initArrNumbers(self, qty):
        self.arrNumbers.clear()
        for i in range(qty):
            self.arrNumbers.append(i)
        mixArrNumbers = self.arrNumbers.copy()
        random.shuffle(mixArrNumbers)
        self.arrNumbers = mixArrNumbers

    def update_graphic(self):
        try:
            if self._pressed_play:
                self.showArrayNumbers()
                self.showALG()
            self.screem.after(40, self.update_graphic)
        except:
            self.restart()


    def showArrayNumbers(self):
        self.canvasGraphics.delete("arr")
        for i in range(0, self.lenArrNumbers):
            x0 = self.dx_item_number_x * i
            x1 = x0 + self.dx_item_number_x
            y0 = self._max_y
            dy = self.arrNumbers[i]/self._maxValueInArrNumbers
            y1 = self._max_y * dy
            
            if (i == self._pivot0 or i == self._pivot1) and self._pressed_play and self._counter_btn_play_presed != 0:    
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


    def cbx_changed(self, event):
        if not self.isValidQtyOfNumbers():
            self.restartDefault()
        else:
            self.restart()


    def play(self):
        if self._counter_btn_play_presed == 0:
            if not self.isValidQtyOfNumbers():
                self.screem.title("Not Valur in NumberQTY Start with Deafult Value")
            else:
                self.restart()
                self.screem.title(f"Bubble Sort {self.lenArrNumbers} + PLAY")
                self.cleanTxt()

            self.calculateMaxIterators()
            self._pressed_play = True
        else:
            if not self._pressed_pause:

                if not self.isValidQtyOfNumbers():
                    self.screem.title("Not Valur in NumberQTY")
                    self.cleanTxt()
                else:
                    self.restart()
                    self._pressed_play = True
                    self.cleanTxt()
                

                self._pressed_pause = True

        self._counter_btn_play_presed = self._counter_btn_play_presed + 1

        

    def pause(self):
        self.screem.title("Burbuja by loko:PAUSE")
        self._pressed_pause = True
        self._pressed_play = False

    def restartDefault(self):
        self._pressed_play = False
        self._iCounter = 0
        self._jCounter = 0
        k = random.randint(33, 99)
        self.initArrNumbers(k)
        self.calculateKons()
        self._pivot0 = 0
        self._pivot1 = 0
        self.iterator = 0
        self.lblALG['text'] = "ALG"
        self.showArrayNumbers()
        
    def restart(self):
        self._pressed_play = False
        self._iCounter = 0
        self._jCounter = 0
        self._pivot0 = 0
        self._pivot1 = 0
        self.iterator = 0
        try:
            k = self.txtNumbersQTY.get()
            k = int(k)
            self.initArrNumbers(k)
        except:
            k = random.randint(33, 99)
            self.initArrNumbers(k)

        self.calculateKons()
        self.lblALG['text'] = "ALG"
        self.showArrayNumbers()
        

    def run(self):
        self.iterator = 0 # Count total program times need to sort
        while True:
            try:
                # Brute Bubble Sort
                isBruteBubbleSort = str(self.txt_alg_cbx_selection.get()) == self.alg_registred[0]
                if isBruteBubbleSort:
                    _arrCounter = 0
                    while _arrCounter < self.lenArrNumbers and self._pressed_play:
                        _itemCounter = 0
                        while _itemCounter < self.lenArrNumbers-1 and self._pressed_play:
                            self._pivot0 = _itemCounter
                            self._pivot1 = _itemCounter + 1
                            if self.arrNumbers[self._pivot0] < self.arrNumbers[self._pivot1]:
                                self._temp = self.arrNumbers[self._pivot0]
                                self.arrNumbers[self._pivot0] = self.arrNumbers[self._pivot1]
                                self.arrNumbers[self._pivot1] = self._temp
                                self._swapsCounter = self._swapsCounter + 1

                            sleep(self._sleepTime)
                            self.iterator = self.iterator + 1
                            _itemCounter = _itemCounter + 1


                        _arrCounter = _arrCounter + 1
                    self._pressed_play = False


                isOptimalBubbleSort = str(self.txt_alg_cbx_selection.get()) == self.alg_registred[1]
                if isOptimalBubbleSort and self._pressed_play:
                    _arrCounter = 0
                    while _arrCounter < self.lenArrNumbers and self._pressed_play:
                        _itemCounter = 0
                        while _itemCounter < self.lenArrNumbers - (_arrCounter + 1) and self._pressed_play:
                            self._pivot0 = _itemCounter
                            self._pivot1 = _itemCounter + 1
                            if self.arrNumbers[self._pivot0] < self.arrNumbers[self._pivot1]:
                                self._temp = self.arrNumbers[self._pivot0]
                                self.arrNumbers[self._pivot0] = self.arrNumbers[self._pivot1]
                                self.arrNumbers[self._pivot1] = self._temp
                                self._swapsCounter = self._swapsCounter + 1

                            sleep(self._sleepTime)
                            self.iterator = self.iterator + 1
                            _itemCounter = _itemCounter + 1

                        _arrCounter = _arrCounter + 1
                    self._pressed_play = False

                sleep(0.0001)
            except:
                sleep(0.3)



    def cleanTxt(self):
        self.txtNumbersQTY.delete(0, END)


    def isValidQtyOfNumbers(self):
        try:
            return int(self.txtNumbersQTY.get()) > 0
        except:
            return False

sw = GraphicSortAGL()
