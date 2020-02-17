import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QMessageBox
#from PyQt5.QtCore import pyqtSignal, pyqtSlot  ## may need later

import numpy as np

#################################################################
#### import matplotlib classes to enable plots in PyQt5
#################################################################
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)


version = "0.1"

#### Initialize Death Prob Arrays based on 2016 data                          ####
#### These stats are taken from: https://www.ssa.gov/oact/STATS/table4c6.html ####
####                                                                          ####
#### Originally had these as part of the uiMainWindow class not sure what the ####
#### standard practice should be.  Pulled them out as globas vars to experiment ##
deathProbAge = np.array([50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,
                80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,
                108,109,110,111,112,113,114,115,116,117,118,119])

deathProbMale = np.array([0.005007,0.005493,0.006016,0.006575,0.00717,0.007805,0.008477,0.009181,0.009916,0.010683,
                0.011533,0.012434,0.013302,0.014109,0.014913,0.015808,0.016868,0.018101,0.019544,0.021206,
                0.023122,0.025265,0.027585,0.03007,0.032794,0.035963,0.039588,0.043511,0.04772,0.052358,
                0.057712,0.063886,0.070782,0.078442,0.086997,0.096603,0.10739,0.119456,0.132853,0.147599,
                0.163689,0.181104,0.19981,0.219765,0.240913,0.261868,0.282225,0.301555,0.319421,0.335392,
                0.352162,0.36977,0.388259,0.407672,0.428055,0.449458,0.471931,0.495527,0.520304,0.546319,
                0.573635,0.602317,0.632432,0.664054,0.697257,0.732119,0.768725,0.807162,0.84752,0.889896])

deathProbFemale = np.array([0.003193,0.003492,0.003803,0.004126,0.004462,0.004829,0.00522,0.005612,0.006,0.006397,
                    0.006848,0.007358,0.007893,0.008453,0.009063,0.009761,0.010581,0.011535,0.012646,0.013919,
                    0.015413,0.017089,0.018861,0.020705,0.022703,0.025035,0.027766,0.030822,0.034227,0.038062,
                    0.042539,0.047663,0.053278,0.059378,0.066132,0.073763,0.082465,0.09237,0.103546,0.115997,
                    0.129706,0.144636,0.160741,0.177971,0.19627,0.214769,0.233174,0.251158,0.268378,0.284481,
                    0.30155,0.319643,0.338821,0.359151,0.3807,0.403542,0.427754,0.45342,0.480625,0.509462,0.54003,
                    0.572432,0.606778,0.643184,0.681775,0.722682,0.766043,0.807162,0.84752,0.889896])
#### Initialize these arrays to zero ####
probLiveMale = np.zeros(40)
probLiveFemale = np.zeros(40)
probLiveJoint = np.zeros(40)



class MplFigure(object):
    def __init__(self, parent):
        self.figure = plt.figure(facecolor='white')
        self.canvas = FigureCanvas(self.figure)
        #self.toolbar = NavigationToolbar(self.canvas, parent) # not needed in simple plot


        

class uiMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Mortality UI.ui', self)  #### load Qt Designer UI design
        self.setWindowTitle("Mortality Plot Generator v" + version)
       
        self.actionAbout.triggered.connect(lambda: self.clicked("About Was Clicked"))
        self.actionExit.triggered.connect(sys.exit)
        
        #### Populate values into age combo boxes (50 to 80)  ####
        self.ageSelectionList = np.linspace(50, 80, 31, dtype=int)
        for age in self.ageSelectionList:
            self.ageMComboBox.addItem(str(age))
            self.ageFComboBox.addItem(str(age))
        self.ageMComboBox.setCurrentIndex(15) # default index = 15 (65 yrs)
        self.ageFComboBox.setCurrentIndex(15) # default index = 15 (65 yrs)
        self.ageMComboBox.currentIndexChanged.connect(self.onValueChanged)
        self.ageFComboBox.currentIndexChanged.connect(self.onValueChanged)
    
        #### Setup and initialize plotting area in the verticalLayout box ####
        self.main_figure = MplFigure(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        #self.verticalLayout.addWidget(self.main_figure.toolbar)
        self.verticalLayout.addWidget(self.main_figure.canvas)
        self.initMplWidget()



    #################################################################
    #### initialize MatPlotLib plot and update with default values
    #################################################################
    def initMplWidget(self):
        self.ax = self.main_figure.figure.add_subplot(111)
        '''
        self.ax.set_ylim(0,100) #are these even needed, since we need to redo them after clearing?
        self.ax.set_xlim(50, 100) #are these even needed?
        self.ax.set_xlabel('Age when Withdrawals Begin', fontsize=6) #are these even needed?
        self.ax.set_ylabel('Probability of Being Alive (%)') #are these even needed?
        self.ax.grid(True) #are these even needed?
        '''
        #self.ax.figure.canvas.show() # does not seem to do anything

        self.onValueChanged() # call event handler that reads input and updates plot
    #################################################################


    #################################################################
    #### added this method to handle clicking menu items and display
	#### text that is passed using the triggered/clicked connects
    #################################################################
    def clicked(self, text):
        self.setStatusTip(text)
        if text == 'About Was Clicked':
            QMessageBox.about(self,"Mortality Calculator", 
                                    "Mortaility Calculator \n" +
                                    "Version: " + version + "\n" +
                                    "Author: Steve Harbin \n" +
                                    "Date: Feb 11, 2020 \n" + 
                                    "----------------------- \n" +
                                    "Probability of living past a given age \n" +
                                    "Based on mortality statistics provided by SSA \n" +
                                    "Website: https://www.ssa.gov/oact/STATS/table4c6.html")

        # To Do: Add handlers for other menu actions if added                            
    #################################################################

    #################################################################
    #### added this method to handle changes in spinner boxes and 
	#### display new value calculations then update plot
    #################################################################
    #@pyqtSlot()   # Do I need this??
    def onValueChanged(self):
        self.ageMSelected = int(self.ageMComboBox.currentText())
        self.ageFSelected = int(self.ageFComboBox.currentText())

        ####  Calculate probability of living based on SSA death stats arrays  ####
        ####  and values selected for M and F age when calculations start      ####
        probLiveMale[0] = 1   # Assumes male is alive when selected age is reached
        probLiveFemale[0] = 1 # Assumes female is alive when selected age is reached
        probLiveJoint[0] = 1
        for year in range(1, 40): 
            indexM = self.ageMSelected - deathProbAge[0] + year
            indexF = self.ageFSelected - deathProbAge[0] + year

            probLiveMale[year] = (1-deathProbMale[indexM]) * probLiveMale[year-1]
            probLiveFemale[year] = (1-deathProbFemale[indexF]) * probLiveFemale[year-1]
            probLiveJoint[year] = 1 - ( (1-probLiveMale[year]) * (1-probLiveFemale[year]) ) 

        self.updatePlot() 
    #################################################################


    ############ Recalculate and Redraw plot when values changed from the User Interface ############
    def updatePlot(self):
        
        self.ax.clear()  #also clears titles and gridlines, etc.  Is there a better way to do this?

        self.ax.set_title('Probability of Living Past an Entered Age') 

        self.ax.set_xlabel('Additional Years', fontsize=10) 
        self.ax.set_ylabel('Probability of Being Alive (%)') 

        self.ax.set_xlim(0, 40) 
        self.ax.set_ylim(0, 100) 
        
        # Change major ticks to show every 10.
        self.ax.xaxis.set_major_locator(MultipleLocator(10))
        self.ax.yaxis.set_major_locator(MultipleLocator(10))

        # Change minor ticks to show every 5. (10/2 = 5)
        self.ax.xaxis.set_minor_locator(AutoMinorLocator(2))
        self.ax.yaxis.set_minor_locator(AutoMinorLocator(2))

        # Turn grid on for both major and minor ticks and style minor differently.
        self.ax.grid(which='major', color='#CCCCCC', linestyle='-')
        self.ax.grid(which='minor', color='#CCCCCC', linestyle=':')
        #self.ax.grid(True) # above grid statements supercede this one

        retirementYr = np.linspace(0, 39, 40)
        self.ax.plot(retirementYr, probLiveMale*100)
        self.ax.plot(retirementYr, probLiveFemale*100)
        self.ax.plot(retirementYr, probLiveJoint*100)

        self.ax.legend(["Male", "Female", "Joint"], fontsize =6)

        self.ax.figure.canvas.draw()        
    #####################################################################################

        


#### Start application and UI Loop ####
if __name__ == "__main__":
    app = QApplication(sys.argv)        
    ui = uiMainWindow()
    ui.show()
    sys.exit(app.exec_())
######### End of application ##########

