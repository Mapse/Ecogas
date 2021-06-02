# -*- coding: utf-8 -*-					#per poter usare caratteri speciali come
####### script per estrarre valori corrente a HV desiderata e per le camere desiderate
import ROOT
from ROOT import gROOT
from ROOT import TCanvas, TH1, TH2, TGraph, gPad, TF1, kRed, TMultiGraph, TLegend, gStyle, TPaveStats, TStyle, TText, TList, TLatex, TGraphErrors, TFile
from array import array
import math
import string
from datetime import datetime								
import time
import os		
import glob
import numpy	
space= "	"
newline= "\n"	

#############################################

# Dictionary with scan ID and Absortion factor.
scan_list={'000157': '6.9', '000156': '10', '000155': '15',
           '000154': '22', '000152': '69'}

# HV points considered to extract the parameters
HVlistch1={'6.9': [11200, 11300, 11400, 11500]}
HVlistch2={'10': [11200, 11300, 11400, 11500]}
HVlistch3={'15': [11200, 11300, 11400, 11500]}
HVlistch4={'22': [11200, 11300, 11400, 11500]}
HVlistch5={'69': [11400, 11700, 11800, 11900]}

## Creation of a csv file with the important parameters to provides to the plotting code.

# Name of the output file
name_file_output="extract_current.csv"	
# Creates the file with the option 'w' (write)
file_output=open(name_file_output, "w")	

# Header for the csv file
header= "#ID-Scan	HV(V)	current_tot_GT(uA)	IBOT(uA)	ITOP(uA)	 Rate(Hz/cm^2)	Cluster_rate(Hz/cm^2)	ABS" + newline

# Writes the content on the file
file_output.write(header)

# Detectors name
detectors=["CMS-GT-2-0"]

# Gaps name

gapBOT5= "CMS-GT-2-0-BOT"
gapTOP5= "CMS-GT-2-0-TOP"

# Dimension of the gaps

SBOTGT = 7000 #cm²
STOPGT = 7000 # cm²

## Partitions dimensions

# SA + SB + SC = 11920.82

# GT-Chamber (ECO-GAS)

SA_GT = SBOTGT/2
SB_GT = SBOTGT/2

strip_mask_a = [0]
strip_mask_b = [0]

show = list()
##### Function to calculate the rate:
# Sum of rates/ number of strips
def rate_calc(histo):				

	# Takes the number of strips in a partition.
	n_bin= histo.GetNbinsX()				
	# Counter for sum the rate per trip
	count_rate = 0			
	# Counter for the number of strips
	index = 1				

	# Loop for sum all contributions
	while index <= n_bin:			
		# Takes the rate [Hz/cm²] per strip (index)	

		if (histo == histoInstant_NoiseA5):
			if (index not in strip_mask_a):
				y_value=histo.GetBinContent(index)
				# Sums all contributions		
				count_rate= count_rate+y_value
		elif (histo == histoInstant_NoiseB5):
			if (index not in strip_mask_b):
				y_value=histo.GetBinContent(index)
				# Sums all contributions		
				count_rate= count_rate+y_value
		# Compute the number of strips 				
		index=index+1						
	# Normalize the sum of the rates per the number of strips
	mean_y= count_rate/n_bin			

	return mean_y

############# Loop in the scan list considered

for scan in scan_list:
   
    # Variables for total current
	I_TOT5=0 	
	# Variables for the total currents errors 
	I_TOT5_err=0
	# Variables for the total rate 
	Rate_TOT5=0

	# Uses glob to take a list with all ROOT files in the path.
	list_rootfile_no_ordinati= glob.glob('/eos/user/m/mabarros/RPC/Gif++/ecogas/rate_scan/Scan_'+scan+'/*_CAEN.root')
	list_rootfile= sorted(list_rootfile_no_ordinati) 
	
	# HV list for ABS 6.9
	if (HVlistch1.keys()[0] == scan_list[scan]):
		HVlist = HVlistch1.values()[0]
	# HV list for ABS 10
	if (HVlistch2.keys()[0] == scan_list[scan]):
		HVlist = HVlistch2.values()[0]
	# HV list for ABS 15
	if (HVlistch3.keys()[0] == scan_list[scan]):
		HVlist = HVlistch3.values()[0]
	# HV list for ABS 22
	if (HVlistch4.keys()[0] == scan_list[scan]):
		HVlist = HVlistch4.values()[0]
	# HV list for ABS 69
	if (HVlistch5.keys()[0] == scan_list[scan]):
		HVlist = HVlistch5.values()[0]

	# Loop in the root files for each scan.
	for file_in in list_rootfile:
		input_root = TFile(file_in)	
		for det in detectors:
			for volt in HVlist:
			
				# Takes the effective voltage for the gaps.
				histoHV_eff_BOT5 = input_root.Get("HVeff_" + gapBOT5) 
				HV_eff_BOT5= histoHV_eff_BOT5.GetMean()

				histoHV_eff_TOP5 = input_root.Get("HVeff_" + gapTOP5)
				HV_eff_TOP5= histoHV_eff_TOP5.GetMean()

				# If the voltage is equal to the HV considered we do the analysis.
				if HV_eff_BOT5 == volt and HV_eff_TOP5 == volt: 

					## Calculates the density current for each GAP as well as their RMS error: Current/Area 

					#BOT
					histoADC_BOT5 = input_root.Get("Imon_" + gapBOT5)
					ADC_BOT5= histoADC_BOT5.GetMean()	
					ADC_err_BOT5= histoADC_BOT5.GetRMS()/SBOTGT

					#TOP
					histoADC_TOP5 = input_root.Get("Imon_" + gapTOP5)
					ADC_TOP5= histoADC_TOP5.GetMean()	
					ADC_err_TOP5= histoADC_TOP5.GetRMS()/STOPGT
					#TOT
					I_TOT5= ( (ADC_BOT5)+(ADC_TOP5))/(2)
					I_TOT5_err= SBOTGT* ( (ADC_err_BOT5*SBOTGT)+(ADC_err_TOP5*STOPGT))/(SBOTGT*2)

					### Rate
					# Opens the files for offline
					rate_file= file_in.replace("CAEN", "Offline")	
					input_rate = TFile(rate_file)		

					# Takes the histogram with the rate/area for the partition A
					histoInstant_NoiseA5 = input_rate.Get("Strip_Mean_Noise_"+det+"_A")		
					# Uses the function rate_calc to return the rate normalized per strip.			
					Instant_NoiseA5=rate_calc(histoInstant_NoiseA5)		

					# Takes the histogram with the rate/area for the partition B
					histoInstant_NoiseB5 = input_rate.Get("Strip_Mean_Noise_"+det+"_B")		
					# Uses the function rate_calc to return the rate normalized per strip.		
					Instant_NoiseB5=rate_calc(histoInstant_NoiseB5)		

					# Calculates the total normalized rate.
					Rate_TOT5= (Instant_NoiseA5*SA_GT + Instant_NoiseB5*SB_GT )/(SA_GT+SB_GT)

					##Cluster rate

					# Takes the histogram for cluster size
					hist_partition_a = input_rate.Get("NoiseCSize_H_CMS-GT-2-0_A")
					hist_partition_b = input_rate.Get("NoiseCSize_H_CMS-GT-2-0_B")

					# Takes the mean for cluster size
					cluster_partition_a = hist_partition_a.GetMean()
					cluster_partition_b = hist_partition_b.GetMean()

					# Computes the normalized cluster size
					cluster_size = (cluster_partition_a*SA_GT + cluster_partition_b*SB_GT )/(SA_GT+SB_GT)

					# Computes the cluster rate
					Cluster_rate = Rate_TOT5/cluster_size

					line_out= str(scan) +space + str(volt) + space + str(I_TOT5)+ space+ str(ADC_BOT5)+space+str(ADC_TOP5)+space+ str(Rate_TOT5) +space+ str(Cluster_rate) +space+ str(scan_list[scan]) + newline

					file_output.write(line_out)
		
				
	
	
	

	print "END SCAN #", scan
















					
            
    
