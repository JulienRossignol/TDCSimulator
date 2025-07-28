import numpy as np
import matplotlib.pyplot as plt

class FineInterpolator:
    def loadClkSkew(self, filepath):
        clkSkew = []
        with open(filepath, "r") as csvfile:
            csvfile.readline()
            while(line:= csvfile.readline()):
                clkSkew.append(float(line.split(',')[1]))
            
        clkSkewA = np.array(clkSkew)  
        minSkew = np.min(clkSkewA)
        clkSkewA = clkSkewA - minSkew
        return clkSkewA*1000000 #Clock skew is measured in ns, change it to femtosecond
    
    def loadTapDelay(self, filepathLogic, filepathNet):
        logicTapDelay = []
        netTapDelay = []
        
        with open(filepathLogic, "r") as csvfile:
            csvfile.readline()
            while(line:= csvfile.readline()):
                logicTapDelay.append(float(line.split(',')[1]))
                
        with open(filepathNet, "r") as csvfile:
            csvfile.readline()
            while(line:= csvfile.readline()):
                netTapDelay.append(float(line.split(',')[1]))
     
        logicTapDelayA = np.array(logicTapDelay)  
        netTapDelayA = np.array(netTapDelay)
        totalTapDelay = logicTapDelayA + netTapDelayA

        return totalTapDelay*1000000 #tap delay is measured in ns, change it to femtosecond
       
    def addSkewToDelay(self, delay, skew):
        tap_arrival = delay - skew
        minDelay = np.min(tap_arrival)
        self.tapStart = tap_arrival - minDelay
     
    def computeCalibrationTable(self):
        orderedStartTime = np.sort(self.tapStart)
        self.calibrationTable = [0]
        for i in range(0, len(orderedStartTime)-1):
            self.calibrationTable.append(orderedStartTime[i]+((orderedStartTime[i+1]-orderedStartTime[i])/2))
        
    def loadTapTriggerTime(self):
        #load tap delay from vivado
        if(self.architecture == "u" or self.architecture == "u+"):
            signal_reach_tap_max = np.append(self.loadTapDelay(self.modelFolderPath + "/MAX_LOGIC_DELAY_CO"+ self.channelSuffix + ".csv",self.modelFolderPath + "/MAX_NET_DELAY_CO"+ self.channelSuffix + ".csv"), self.loadTapDelay(self.modelFolderPath + "/MAX_LOGIC_DELAY_O"+ self.channelSuffix + ".csv",self.modelFolderPath + "/MAX_NET_DELAY_O"+ self.channelSuffix + ".csv"))
            signal_reach_tap_min = np.append(self.loadTapDelay(self.modelFolderPath + "/MIN_LOGIC_DELAY_CO"+ self.channelSuffix + ".csv",self.modelFolderPath + "/MIN_NET_DELAY_CO"+ self.channelSuffix + ".csv"), self.loadTapDelay(self.modelFolderPath + "/MIN_LOGIC_DELAY_O"+ self.channelSuffix + ".csv",self.modelFolderPath + "/MIN_NET_DELAY_O"+ self.channelSuffix + ".csv"))
            signal_reach_tap_avg = (signal_reach_tap_max + signal_reach_tap_min)/2
            
            clkSkew_max = np.append(self.loadClkSkew(self.modelFolderPath + "/MAX_CLOCK_SKEW_CO"+ self.channelSuffix + ".csv"),self.loadClkSkew(self.modelFolderPath + "/MAX_CLOCK_SKEW_O"+ self.channelSuffix + ".csv"))
            clkSkew_min = np.append(self.loadClkSkew(self.modelFolderPath + "/MIN_CLOCK_SKEW_CO"+ self.channelSuffix + ".csv"),self.loadClkSkew(self.modelFolderPath + "/MIN_CLOCK_SKEW_O"+ self.channelSuffix + ".csv"))
            clkSkew_avg = (clkSkew_max+clkSkew_min)/2
        
        else:
            signal_reach_tap_max = self.loadTapDelay(self.modelFolderPath + "/MAX_LOGIC_DELAY_CO"+ self.channelSuffix + ".csv",self.modelFolderPath + "/MAX_NET_DELAY_CO"+ self.channelSuffix + ".csv")
            signal_reach_tap_min = self.loadTapDelay(self.modelFolderPath + "/MIN_LOGIC_DELAY_CO"+ self.channelSuffix + ".csv",self.modelFolderPath + "/MIN_NET_DELAY_CO"+ self.channelSuffix + ".csv")
            signal_reach_tap_avg = (signal_reach_tap_max + signal_reach_tap_min)/2
            
            clkSkew_max = self.loadClkSkew(self.modelFolderPath + "/MAX_CLOCK_SKEW_CO"+ self.channelSuffix + ".csv")
            clkSkew_min = self.loadClkSkew(self.modelFolderPath + "/MIN_CLOCK_SKEW_CO"+ self.channelSuffix + ".csv")
            clkSkew_avg = (clkSkew_max+clkSkew_min)/2
       
        if(self.analysis == "max"):
            clkSkew = clkSkew_max
            signal_reach_tap = signal_reach_tap_max
        elif(self.analysis == "min"):
            clkSkew = clkSkew_min
            signal_reach_tap = signal_reach_tap_min    
        else:
            clkSkew = clkSkew_avg
            signal_reach_tap = signal_reach_tap_avg
          
        #if you want to simulate with specific tap delays or skew, you can just assign clkSkew of signal_reach_tap with your values here         
          
        self.addSkewToDelay(signal_reach_tap,clkSkew)
        self.computeCalibrationTable()  

    def __init__(self, modelFolderPath, architecture = "u", channelSuffix = "", analysis = "avg"):
        self.architecture = architecture
        self.modelFolderPath = modelFolderPath
        self.analysis = analysis
        self.channelSuffix = channelSuffix
        self.loadTapTriggerTime()
        self.LSB = np.max(self.tapStart)/len(self.tapStart)
        self.computeBinWidth()
        self.computeNL()
        self.computeError()
        self.simulatedPrecision = self.quantizationError
        
    def measure(self, time):
        ones = time > self.tapStart 
        return np.sum(ones)      
        
    def retrieveTime(self, code, calibrated=True):
        if(calibrated):
            return self.calibrationTable[code]
        else:
            return (code-0.5)*self.LSB
        
    def computeBinWidth(self):
        self.binWidth = np.diff(np.sort(self.tapStart))
        
    def computeNL(self):
        self.DNL = self.binWidth - self.LSB
        self.INL = np.cumsum(self.DNL)
    
    def computeError(self):
        self.quantizationError = ((self.LSB**2)/12 + (1/(4*len(self.tapStart)))*(np.sum(np.square(self.DNL))) + (1/(12*np.max(self.tapStart)))*(np.sum(np.power(self.DNL,3))) )**0.5
    
    def getMaxCodeForRange(self, rangeTime):
        return self.measure(rangeTime)
    
    def setLSB(self, LSB):
        self.LSB = LSB
        self.computeNL()
        self.computeError()