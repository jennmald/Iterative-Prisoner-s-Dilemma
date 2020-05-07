#!/usr/bin/env python3
from tkinter import *
from tkinter.ttk import *
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np
from Evolution import *

class GUI():
    def __init__(self):
        root = Tk()

        figure = plt.figure( figsize=(8,4) )
        axes = plt.gca()
        canvas = FigureCanvasTkAgg(figure, master=root)
        canvas.get_tk_widget().grid(row=0, column=0)
        canvas.draw()

        # if you set a limit the graph will not dynamically resize
        # axes.set( xlim=(0,2), ylim=(0,4) )

        # plot the points
        # linestyle: solid, dashed, dotted, dashdot
        lineDataC = plt.plot([], [], linewidth=2, linestyle="solid", color="red", label="All-C")[0]
        lineDataD = plt.plot([], [], linewidth=2, linestyle="solid", color="blue", label="All-D")[0]
        lineDataTFT = plt.plot([], [], linewidth=2, linestyle="solid", color="green", label="TFT")[0]
        plt.legend(loc="upper left", fontsize=12)
        plt.xlabel('Tournament Number')
        plt.ylabel('Number of Agents')
        plt.title('Iterated Prisoners Dilemma Simulation')

        AllCLabel = Label(root, text = "All C Population")
        AllCEntry = Entry(root)
        AllCEntry.grid(row = 1, column = 0)
        AllCLabel.grid(row = 2, column = 0)

        AllDLabel = Label(root, text = "All D Population")
        AllDEntry = Entry(root)
        AllDEntry.grid(row=3, column=0)
        AllDLabel.grid(row=4, column=0)

        TFTLabel = Label(root, text = "TFT Population")
        TFTEntry = Entry(root)
        TFTEntry.grid(row=5, column=0)
        TFTLabel.grid(row=6, column=0)

        tLabel = Label(root, text = "Number of Tournaments")
        numofTEntry = Entry(root)
        numofTEntry.grid(row=7, column=0)
        tLabel.grid(row=8, column=0)
        

        runModelButton = Button(root, text="Run Model")
        runModelButton.grid(row=9, column=0)

        def runModel():
            allCP = int( AllCEntry.get() )
            allDP = int( AllDEntry.get() )
            TFTP = int( TFTEntry.get() )
            numOfTournaments = int( numofTEntry.get() )

            allC = Agent(1,1,1, "All-C")
            allD = Agent(0,0,0, "All-D")
            TFT  = Agent(1,1,0, "T-F-T")

            testPopulation = [{"agent":allC, "count":allCP}, {"agent":TFT, "count":TFTP}, {"agent":allD, "count":allDP}]
            evolution = Evolution(allCP, allDP, TFTP)
            tempAgentCounts = evolution.run(testPopulation, numOfTournaments)

            for n in range(0, numOfTournaments+1):
                
                lineDataC.set_xdata( evolution.round_history[0:n+1] )
                lineDataC.set_ydata( evolution.C_history[0:n+1] )

                lineDataD.set_xdata( evolution.round_history[0:n+1] )
                lineDataD.set_ydata( evolution.D_history[0:n+1] )

                lineDataTFT.set_xdata( evolution.round_history[0:n+1] )
                lineDataTFT.set_ydata( evolution.TFT_history[0:n+1] )

                # also points!
                axes.plot( evolution.round_history[n-1], evolution.C_history[n-1], color="red", marker="o" )
                axes.plot( evolution.round_history[n-1], evolution.D_history[n-1], color="blue", marker="o" )
                axes.plot( evolution.round_history[n-1], evolution.TFT_history[n-1], color="green", marker="o" )

                canvas.draw()

        runModelButton["command"] = runModel

        root.mainloop()

# run this program
gui = GUI()
