from tkinter import *
import tkinter as tk
from tkinter import filedialog
import tkinter.scrolledtext as scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Managing GUI
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class MyWindow1(Page):
    # All GUI components and placements
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        ## First section

        self.cryptoLabel = Label(self, text='Stock/Crypto:').place(x=10, y=10)
        self.crypto = Entry(self).place(x=100, y=10)

        self.timeFrameLabel = Label(self, text='Time-frame:').place(x=10, y=40)
        self.timeFrame = Entry(self).place(x=100, y=40)

        self.retrieveDataFromLabel = Label(self, text='From: ').place(x=250, y=10)
        self.retrieveDataFrom = Entry(self).place(x=300, y=10)
        self.retrieveDataToLabel = Label(self, text='To: ').place(x=250, y=40)
        self.retrieveDataTo = Entry(self).place(x=300, y=40)

        self.retrieveDataButton = Button(self, text='Retrieve Data', height=1, width=13,
                                         command=self.retrieveData).place(x=440, y=7)

        self.initializeDataButton = Button(self, text='Initialize Data', height=1, width=13,
                                           command=self.initializeData).place(x=440, y=35)

        self.startLiveTradingButton = Button(self, text='Live Trader', height=1, width=13,
                                             command=self.liveTrader).place(x=550, y=7)

        self.stopLiveTraderButton = Button(self, text='Stop Live Trader', height=1, width=13,
                                           command=self.stopStrategy).place(x=550, y=35)



        self.numberOfPreviousCandlesticksLabel = Label(self, text='Previous Candlestticks:').place(x=660, y=10)
        self.numberOfPreviousCandlesticks = Entry(self).place(x=790, y=10)

        self.resetStrategyButton = Button(self, text='Reset Strategy', height=1, width=13,
                                          command=self.stopStrategy).place(x=660, y=35)



        ## Second section
        self.secondSectionLabel = Label(self, text='Backtrader',font=("TkDefaultFont", 20)).place(x=10, y=70)

        self.commandLabel = Label(self, text='Command:').place(x=10, y=110)
        self.command = Entry(self).place(x=100, y=110)

        self.sendCommandButton = Button(self, text='Send', height=1, width=13,
                                         command=self.sendCommand).place(x=240, y=103)
        self.plotButton = Button(self, text='Send', height=1, width=13,
                                        command=self.plot).place(x=340, y=203)



    def retrieveData(self):
        pass

    def stopStrategy(self):
        pass

    def initializeData(self):
        pass
    def liveTrader(self):
        pass
    def stopLiveTrader(self):
        pass
    def sendCommand(self):
        pass

    def plot(self):
        figure = plt.Figure(figsize=(10, 3), dpi=100)
        ax = figure.add_subplot(111)
        chart_type = FigureCanvasTkAgg(figure, root)
        chart_type.get_tk_widget().place(x=0, y=300)
        ax.scatter([0, 1, 2], [2, 3, 4])
        ax.set_title('The Title for your chart')


# Setting the GUI for page 2
class MyWindow2(Page):
    # GUI Components
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)


# Managing both pages
class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = MyWindow1(self)
        p2 = MyWindow2(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Trader", command=p1.lift)
        b2 = tk.Button(buttonframe, text="Backtester", command=p2.lift)

        b1.pack(side="left")
        b2.pack(side="left")

        p1.show()


if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("1200x700+10+10")

    root.mainloop()
