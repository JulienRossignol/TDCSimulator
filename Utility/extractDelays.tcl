set folder [lindex $argv 0]

for {set c 0} {$c < 2} {incr c} {

report_property -file $folder/MAX_LOGIC_DELAY_CO_$c.txt [get_timing_paths -from signal_in0 -to design_1_i/channel_$c/inst/TDL_0/inst/tdl_carryChain/co_out_reg[0]/D] DATAPATH_LOGIC_DELAY
report_property -file $folder/MAX_LOGIC_DELAY_O_$c.txt [get_timing_paths -from signal_in0 -to design_1_i/channel_$c/inst/TDL_0/inst/tdl_carryChain/o_out_reg[0]/D] DATAPATH_LOGIC_DELAY
report_property -file $folder/MAX_NET_DELAY_CO_$c.txt [get_timing_paths -from signal_in0 -to design_1_i/channel_$c/inst/TDL_0/inst/tdl_carryChain/co_out_reg[0]/D] DATAPATH_NET_DELAY
report_property -file $folder/MAX_NET_DELAY_O_$c.txt [get_timing_paths -from signal_in0 -to design_1_i/channel_$c/inst/TDL_0/inst/tdl_carryChain/o_out_reg[0]/D] DATAPATH_NET_DELAY
report_property -file $folder/MAX_CLOCK_SKEW_CO_$c.txt [get_timing_paths -from signal_in0 -to design_1_i/channel_$c/inst/TDL_0/inst/tdl_carryChain/co_out_reg[0]/D] SKEW
report_property -file $folder/MAX_CLOCK_SKEW_O_$c.txt [get_timing_paths -from signal_in0 -to design_1_i/channel_$c/inst/TDL_0/inst/tdl_carryChain/o_out_reg[0]/D] SKEW

report_property -file $folder/MIN_LOGIC_DELAY_CO_$c.txt [get_timing_paths -delay_type min -from signal_in0 -to design_1_i/channel_$c/inst/TDL_0/inst/tdl_carryChain/co_out_reg[0]/D] DATAPATH_LOGIC_DELAY
report_property -file $folder/MIN_LOGIC_DELAY_O_$c.txt [get_timing_paths  -delay_type min -from signal_in0 -to design_1_i/channel_$c/inst/TDL_0/inst/tdl_carryChain/o_out_reg[0]/D] DATAPATH_LOGIC_DELAY
report_property -file $folder/MIN_NET_DELAY_CO_$c.txt [get_timing_paths   -delay_type min -from signal_in0 -to design_1_i/channel_$c/inst/TDL_0/inst/tdl_carryChain/co_out_reg[0]/D] DATAPATH_NET_DELAY
report_property -file $folder/MIN_NET_DELAY_O_$c.txt [get_timing_paths    -delay_type min -from signal_in0 -to design_1_i/channel_$c/inst/TDL_0/inst/tdl_carryChain/o_out_reg[0]/D] DATAPATH_NET_DELAY
report_property -file $folder/MIN_CLOCK_SKEW_CO_$c.txt [get_timing_paths  -delay_type min -from signal_in0 -to design_1_i/channel_$c/inst/TDL_0/inst/tdl_carryChain/co_out_reg[0]/D] SKEW
report_property -file $folder/MIN_CLOCK_SKEW_O_$c.txt [get_timing_paths   -delay_type min -from signal_in0 -to design_1_i/channel_$c/inst/TDL_0/inst/tdl_carryChain/o_out_reg[0]/D] SKEW


for {set i 1} {$i < 480} {incr i} {
	report_property -file $folder/MAX_LOGIC_DELAY_CO_$c.txt -append [get_timing_paths -from signal_in0 -to design_1_i/channel_$c/inst/TDL_0/inst/tdl_carryChain/co_out_reg[$i]/D] DATAPATH_LOGIC_DELAY
	report_property -file $folder/MAX_LOGIC_DELAY_O_$c.txt -append [get_timing_paths -from signal_in0 -to design_1_i/channel_$c/inst/TDL_0/inst/tdl_carryChain/o_out_reg[$i]/D] DATAPATH_LOGIC_DELAY
	report_property -file $folder/MAX_NET_DELAY_CO_$c.txt -append [get_timing_paths -from signal_in0 -to design_1_i/channel_$c/inst/TDL_0/inst/tdl_carryChain/co_out_reg[$i]/D] DATAPATH_NET_DELAY
	report_property -file $folder/MAX_NET_DELAY_O_$c.txt -append [get_timing_paths -from signal_in0 -to design_1_i/channel_$c/inst/TDL_0/inst/tdl_carryChain/o_out_reg[$i]/D] DATAPATH_NET_DELAY
	report_property -file $folder/MAX_CLOCK_SKEW_CO_$c.txt -append [get_timing_paths -from signal_in0 -to design_1_i/channel_$c/inst/TDL_0/inst/tdl_carryChain/co_out_reg[$i]/D] SKEW
	report_property -file $folder/MAX_CLOCK_SKEW_O_$c.txt -append [get_timing_paths -from signal_in0 -to design_1_i/channel_$c/inst/TDL_0/inst/tdl_carryChain/o_out_reg[$i]/D] SKEW
	report_property -file $folder/MIN_LOGIC_DELAY_CO_$c.txt -append [get_timing_paths -delay_type min -from signal_in0 -to design_1_i/channel_$c/inst/TDL_0/inst/tdl_carryChain/co_out_reg[$i]/D] DATAPATH_LOGIC_DELAY
	report_property -file $folder/MIN_LOGIC_DELAY_O_$c.txt -append [get_timing_paths  -delay_type min -from signal_in0 -to design_1_i/channel_$c/inst/TDL_0/inst/tdl_carryChain/o_out_reg[$i]/D] DATAPATH_LOGIC_DELAY
	report_property -file $folder/MIN_NET_DELAY_CO_$c.txt -append [get_timing_paths   -delay_type min -from signal_in0 -to design_1_i/channel_$c/inst/TDL_0/inst/tdl_carryChain/co_out_reg[$i]/D] DATAPATH_NET_DELAY
	report_property -file $folder/MIN_NET_DELAY_O_$c.txt -append [get_timing_paths    -delay_type min -from signal_in0 -to design_1_i/channel_$c/inst/TDL_0/inst/tdl_carryChain/o_out_reg[$i]/D] DATAPATH_NET_DELAY
	report_property -file $folder/MIN_CLOCK_SKEW_CO_$c.txt -append [get_timing_paths  -delay_type min -from signal_in0 -to design_1_i/channel_$c/inst/TDL_0/inst/tdl_carryChain/co_out_reg[$i]/D] SKEW
	report_property -file $folder/MIN_CLOCK_SKEW_O_$c.txt -append [get_timing_paths   -delay_type min -from signal_in0 -to design_1_i/channel_$c/inst/TDL_0/inst/tdl_carryChain/o_out_reg[$i]/D] SKEW
}
}