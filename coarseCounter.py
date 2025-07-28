import math
import random

class CoarseCounter:
    def __init__(self, period, jitter):
        self.period = period
        self.jitter = jitter
 
    def measure(self, time, counter=-1, nextClkRisingEdge=0):
        #The counter and nextClkRisingEdge allow to simulate a coarse counter that continues another measurement
        while(nextClkRisingEdge < time):
            nextClkRisingEdge += self.period + random.gauss(sigma=self.jitter)
            counter += 1
        return (counter, nextClkRisingEdge)
        
    def retrieveTime(self, code):
        return code*self.period