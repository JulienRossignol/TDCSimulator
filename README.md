# TDCSimulator
TDC simulator used for article Model and optimization of tapped delay line for time-to-digital converters in FPGA

## Requirements 
Tested with Python 3.13.5, but should work with most python 3 releases.
Requires numpy and matplotlib 

## Usage
usage: simulator.py directory
directory is a directory containing csv files extracted from Vivado, following the naming convention explained in: [10.6084/m9.figshare.29237618](https://dx.doi.org/10.6084/m9.figshare.29237618)

Folder utility contains an exemple TCL script to extract the delays from Vivado. To adapt this script to your design you'll need to:
- Change first line to set folder to the desired output folder
- Change first for loop to account for your number of channel (2 in the exemple file)
- Change second for loop to account for the number of taps (480 in exemple) note that CO and O taps are counted separately in the exemple.
- Change -from in all report_property to match your input signal name
- Change -to in all report_property to match your TDL architecture and point to the flip-flops of your TDL.

Once the delays are extracted, you can use tclToCsv.py found in the utility folder to get csv file. 

## Default simulation
The default simulation use the average value of the delays and use the folder name to find the architecture and clock period. You'll probably want to change this.
It then fine interpolator of two channels and make a biletaral (meaning either channel can trigger first) simulation of these two channels on a range of 5 clock period with a clock cycle-to-cycle jitter of 1.25 ps. 
Results are directly outputed in the provided directory.
