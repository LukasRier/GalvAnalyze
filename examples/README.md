# Example data
This folder contains datasets exported from two different battery cyclers which can be used to demonstrate the full functionality of GalvAnalyze.

## Case 1
File Case1_ActiveMass_18mg_CurrentThreshold_0.15mA.txt

Description
Cell cycled for 50 cycles in total, beginning with a charge (First cycle is charge default setting).

The active mass for this cell was 18 mg.

A variable current was applied (0.17 mA for 2 cycles and 1.7 mA for the subsequent 48 cycles). Analysis of this dataset requires use of the "Applied current varies" option.
Given the minimum current of 0.17 mA we recomend a threshold of 0.15 mA).

## Case 2
File Case2_ActiveMass_1000mg_CurrentThreshold_0.25mA.txt

Description
Cell cycled for 6 cycles and beginning with a discharge (First cycle is charge needs to be un-ticked)

The active mass for this cell was 1000 mg.

A constant current was applied (0.283 mA for 6 cycles).

## Case 3

File Case3_ActiveMass_18mg_CurrentThreshold_0.15mA.txt

Same data as in Case 1 but without final discharge cycle. Given the unequal number of charge and discharge cycles, the final charging cycle is discarded, resulting in 49 pairs.

# Error cases

## Case 4

File Case4_nonsense_headings.txt
Column headings are not compatible with GalvAnalyze. Only a specific set of headings is currently supported:

**Potential**: “Ecell/V”, “E /V”, “Ewe/V”, “E/V”, “Voltage/V” or “Voltage(V)”

**Current**: “<I>/mA”, “I /mA”, “I/mA”, “Current/mA”, or “Current(A)”

**Time**: “time/s” or “time /s”


## Case 5

File Case5_empty.txt

File is emplty. Error is described in the log file.

## Case 6

File Case6_no_data.txt

Valid column headings are provided, however no data is contained in the file. Error is described in the log file.

## Case 7

File Case7_single_discharge.txt

Valid file with correct column headings and data. Data for a single discharge is provided. Given the lack of a paired charge cycle, GalvAnalyze rejects the cycle and returns an error message in the log file.