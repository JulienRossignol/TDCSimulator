from fineInterpolator import FineInterpolator
from coarseCounter import CoarseCounter
import numpy as np
import matplotlib.pyplot as plt

class TDC:
    def __init__(self, clkPeriod, clkJitter):
        self.fineInterpolators = []
        self.coarseCounter = CoarseCounter(clkPeriod, clkJitter)
        self.period = clkPeriod
        self.channelDelay = []
        
    def addFineInterpolator(self, data_folder, architecture, channelSuffix, analysis, channelDelay):
        self.fineInterpolators.append(FineInterpolator(data_folder, architecture, channelSuffix, analysis))
        self.channelDelay.append(channelDelay)
    
    def plotCodeDensity(self, bins, countsPerCode, LSB, output_folder, channelNumber):
        plt.hist(bins[:-1],bins=bins, weights=countsPerCode/LSB)
        plt.title(f'Code density LSB = {LSB/1000}')
        plt.xlabel('Code index')
        plt.ylabel('Bin width (LSB)')
        plt.savefig(output_folder+"/CodeDensity_"+channelNumber+".png")
        plt.close()

    def plotDNL(self, DNL, computedDNL, LSB, output_folder, channelNumber):
        plt.plot(DNL, color="red")
        plt.plot(computedDNL, color="blue")
        plt.title(f'DNL LSB = {LSB/1000}')
        plt.xlabel('Code index')
        plt.ylabel('Bin width (LSB)')
        plt.savefig(output_folder+"/DNL_"+channelNumber+".png")
        plt.close()

    def plotINL(self, INL, computedINL, LSB, output_folder, channelNumber):
        plt.plot(INL, color="red")
        plt.plot(computedINL, color="blue")
        plt.title(f'INL LSB = {LSB/1000}')
        plt.xlabel('Code index')
        plt.ylabel('Bin width (LSB)')
        plt.savefig(output_folder+"/INL_"+channelNumber+".png")
        plt.close()
    
    def measure2Channel(self, time1, time2, channelIndex1, channelIndex2):
        timeDelayed1 = time1 + self.channelDelay[channelIndex1]
        timeDelayed2 = time2 + self.channelDelay[channelIndex2]
        
        if(timeDelayed1 < timeDelayed2):
            (coarseCode1,nextClkRisingEdge) = self.coarseCounter.measure(timeDelayed1)
            fineCode1 = self.fineInterpolators[channelIndex1].measure(nextClkRisingEdge-(timeDelayed1)) 
            (coarseCode2,nextClkRisingEdge) = self.coarseCounter.measure(timeDelayed2, coarseCode1, nextClkRisingEdge)
            fineCode2 = self.fineInterpolators[channelIndex2].measure(nextClkRisingEdge-(timeDelayed2))
        else:
            (coarseCode2,nextClkRisingEdge) = self.coarseCounter.measure(timeDelayed2)
            fineCode2 = self.fineInterpolators[channelIndex2].measure(nextClkRisingEdge-(timeDelayed2)) 
            (coarseCode1,nextClkRisingEdge) = self.coarseCounter.measure(timeDelayed1, coarseCode2, nextClkRisingEdge)
            fineCode1 = self.fineInterpolators[channelIndex1].measure(nextClkRisingEdge-(timeDelayed1))
        
        return ((fineCode1, coarseCode1),(fineCode2, coarseCode2))
        
    def retrieveTime(self, codeList, channelList, calibrated=True):
        timeList = []
        index = 0
        for code in codeList:
            timeList.append(self.coarseCounter.retrieveTime(code[1]+1) - self.fineInterpolators[channelList[index]].retrieveTime(code[0], calibrated))
            index += 1 
        return timeList
            
    def testFineInterpolator(self, interpolatorIndex, rangeTest, output_folder):
        #Run a code density for the fine interpolator and evaluate precision and non linearity
        codeList = []
        errorListCalib = []
        errorListNoCalib = []
        trueTimeList = []
        calibTimeList = []
        noCalibTimeList = []
        
        for time in range(0,rangeTest):
            code = self.fineInterpolators[interpolatorIndex].measure(time)
            codeList.append(code)
        
        #events with code = 0 are skipped because then the tdc would not have triggered, therefore the histogram is produced from 1 to nbTaps
        (countsPerCode, bins) = np.histogram(codeList,bins=range(1,len(self.fineInterpolators[interpolatorIndex].tapStart)+2)) 
        filledCode = np.max(np.nonzero(countsPerCode)) + 1 #This retrieve the number of codes with value in it, the +1 is because np.nonzero returns the zero-based index.
        LSB = self.period/filledCode

        simulatedDNLTime = (countsPerCode[0:filledCode]-LSB)
        simulatedDNL = simulatedDNLTime/LSB

        simulatedINL = np.cumsum(simulatedDNL[0:filledCode])
        simulatedINLTime = np.cumsum(simulatedDNLTime[0:filledCode])  
        
        #If you don't set LSB from simulation results, you'll get the LSB based on the whole TDL, which is close, but leads to innacuracy in precision
        self.fineInterpolators[interpolatorIndex].setLSB(LSB) 
        
        time = 0
        for code in codeList:
            measuredTimeCalibrated= self.fineInterpolators[interpolatorIndex].retrieveTime(code, True)
            measuredTimeNoCalibration = self.fineInterpolators[interpolatorIndex].retrieveTime(code, False)
            errorListCalib.append(time-measuredTimeCalibrated)
            errorListNoCalib.append(time-measuredTimeNoCalibration)
            trueTimeList.append(time)
            calibTimeList.append(measuredTimeCalibrated)
            noCalibTimeList.append(measuredTimeNoCalibration)
            time += 1
        
        #Generate a png file with code density, DNL and INL
        self.plotCodeDensity(bins, countsPerCode, LSB, output_folder, "ch" + str(interpolatorIndex) )
        self.plotDNL(simulatedDNLTime, self.fineInterpolators[interpolatorIndex].DNL, LSB, output_folder, "ch" + str(interpolatorIndex))
        self.plotINL(simulatedINLTime, self.fineInterpolators[interpolatorIndex].INL, LSB, output_folder, "ch" + str(interpolatorIndex))
        
        np.savez(output_folder + "/ch" + str(interpolatorIndex) + ".npz", countsPerCode, simulatedDNLTime/1000, simulatedINLTime/1000)

        #Compute quantization error with and withouth calibration analytically from the bin widths. 
        BinSizeError = ((1/(filledCode*LSB*12))*(np.sum(countsPerCode[0:filledCode]**3)))**0.5
        BinSizeErrorNoCalib = (BinSizeError**2 + ((1/(filledCode*LSB))*np.sum(countsPerCode[1:filledCode]*np.square(simulatedINLTime[1:filledCode]-0.5*simulatedDNLTime[1:filledCode]))))**0.5
        
        #Write the simulated error and the analytical error to a file.
        with open(output_folder+"/resultsCH" + str(interpolatorIndex) + ".txt", "w") as textFile:
            textFile.write(f"No calibration ----- Measured error: {((np.mean(np.square(errorListNoCalib)))**0.5)/1000} ps, From INL, DNL and bin size: {BinSizeErrorNoCalib/1000}\n")
            textFile.write(f"With calibration ---- Measured error: {(np.mean(np.square(errorListCalib))**0.5)/1000} ps, From bin size: {BinSizeError/1000} ps\n")
        
        #Update precision in fineInterpolator based on measurement, the difference comes from using only used code instead of all taps.
        self.fineInterpolators[interpolatorIndex].simulatedPrecision = BinSizeError