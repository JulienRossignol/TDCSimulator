import sys
import matplotlib.pyplot as plt
import os

files = ["MAX_CLOCK_SKEW","MIN_CLOCK_SKEW", "MAX_LOGIC_DELAY", "MIN_LOGIC_DELAY", "MAX_NET_DELAY", "MIN_NET_DELAY","MAX_CLOCK_SKEW_CO","MIN_CLOCK_SKEW_CO", "MAX_LOGIC_DELAY_CO", "MIN_LOGIC_DELAY_CO", "MAX_NET_DELAY_CO", "MIN_NET_DELAY_CO", "MAX_NET_DELAY_O", "MIN_NET_DELAY_O","MAX_CLOCK_SKEW_O","MIN_CLOCK_SKEW_O", "MAX_LOGIC_DELAY_O", "MIN_LOGIC_DELAY_O"]

channelNb = 2

folders = next(os.walk('.'))[1]

for folder in folders:
    subfolders = next(os.walk('./'+folder))[1]
    for subfolder in subfolders:
        for i in range(channelNb):
            if(channelNb == 1):
                channelPrefix = ""
            else:
                channelPrefix = "_" + str(i)
            for file in files:
                filepath = folder + "/" + subfolder + "/" + file + channelPrefix + ".txt"
                outFilepath = folder + "/" + subfolder + "/" + file + channelPrefix +".csv"
                i = 0
                try:
                    with open(filepath, "r") as tclFile:
                        with open(outFilepath, "w") as csvFile:
                            csvFile.write("index, value \n")
                            while(tclFile.readline()): #skip useless line
                                line = tclFile.readline()
                                csvFile.write(f"{i},{float(line.split()[3])}\n")
                                i += 1    
                except:
                    pass