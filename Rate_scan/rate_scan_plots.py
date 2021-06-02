# -*- coding: utf-8 -*-					#per poter usare caratteri speciali come _

#script per plottare ratio rate re2 e re4


#librerie pyROOT per disegnare grafici

#librerie pyROOT per disegnare grafici
import ROOT
from ROOT import gROOT
from ROOT import TCanvas, TGraph, gPad, TF1, TF2 , kRed, TMultiGraph, TLegend, gStyle, TPaveStats, TStyle, TText, TList, TLatex, TMath, TFormula, TGraphErrors, TTree, TDatime, TMath
from array import array

#librerie python
import math										#importa la libreria matematica
import string										#importa la libreria stringhe
from datetime import datetime								#importa la libreria tempo
import time

spazio= " "
newline=" \n"




input_file="extract_current.csv"		#file dati input BARC-8 OFF REFERENCE, csv formattato tabulazione (un file per ogni rivelatore)


# _V3 con colonna per IC
#ADDED BINOS

################################################################################################à
#		TTree

#legge dati da file, e li mette nei rami (tipo /F di default, delimitatore tabulazione '\t')

def callTree():

	tree1= TTree ("tree1","tree1")			#tree per leggere dati BARC-8 OFF reference
	tree1.ReadFile(input_file,"#ID-Scan/C:HV/F:Curr_total/F:Curr_BOT/F:Curr_TOP:Rate/F:Cluster_rate/F:ABS/F",'\t') 

	return tree1

def voltage_clusterRate_single_plot(abs, marker_style, color_style):
	
	# Read the tree
	tree = callTree()

	volt, cluster_rate = array('d'), array('d')
	qtd = 0
	for i in tree:
		if (round(i.ABS, 2) == abs):
			volt.append(tree.HV)
			cluster_rate.append(tree.Cluster_rate)
			qtd = qtd + 1
	
	graph = TGraph(qtd,cluster_rate,volt)			

	graph.SetMarkerStyle(marker_style)
	graph.SetMarkerSize(1.6)
	graph.SetMarkerColor(color_style)
	graph.SetLineColor(color_style)

	## Legend
	""" leg = ROOT.TLegend(0.7939799,0.7095622,0.9946488,0.7601751)
	leg.SetBorderSize(0)
	leg.SetFillStyle(0)
	leg.SetTextSize(0.03)
	
	legend=str(abs) """
		
	return graph


def current_clusterRate_single_plot(abs):
	
	# Read the tree
	tree = callTree()

	current, cluster_rate = array('d'), array('d')
	qtd = 0
	for i in tree:
		if (round(i.ABS, 2) == abs):
			current.append(tree.Curr_total)
			cluster_rate.append(tree.Cluster_rate)
			qtd = qtd + 1
	
	graph = TGraph(qtd,cluster_rate,current)			

	graph.SetMarkerStyle(8)
	graph.SetMarkerSize(1.6)
	graph.SetMarkerColor(2)
	graph.SetLineColor(2)

	## Legend
	leg = ROOT.TLegend(0.7939799,0.7095622,0.9946488,0.7601751)
	leg.SetBorderSize(0)
	leg.SetFillStyle(0)
	
	lengend_GT="CMS-GT-2-0"
	
	leg.AddEntry(graph, lengend_GT, "lp")
	
	leg.Draw()
	
	return graph

def plot_voltage_clusterRate(nabs, abslist):

	## Graph cosmetics

	# Canvas section
	canvas = TCanvas("canvas","canvas", 600, 600)
	gPad.SetGrid()

	canvas.SetTopMargin(.08)
	canvas.SetRightMargin(0.05)
	canvas.SetBottomMargin(0.13)
	canvas.SetLeftMargin(0.16)

	canvas.SetBorderSize(2)
	canvas.SetFrameFillStyle(0)
	canvas.SetFrameBorderMode(0)
	canvas.SetFrameFillStyle(0)
	canvas.SetFrameBorderMode(0)
	
    # Creates the multigraph
	gr1= TMultiGraph()					
	gr1.Draw( 'AP' )
	
	marker_style = [20, 21, 22, 23, 29, 31, 33, 34, 39, 41, 43]
	color_style = [2, 3, 4, 5, 6, 7, 8, 46, 49, 30, 40, 25, 18]

	leg = ROOT.TLegend(0.3, 0.7, 0.5, 0.8)
	leg.SetBorderSize(0)
	leg.SetFillStyle(0)
	leg.SetTextSize(0.03)

	for i in range(nabs):
		
		print abslist[i]
		single_graph = voltage_clusterRate_single_plot(abslist[i], marker_style[i], color_style[i])
		leg.AddEntry(single_graph, str(abslist[i]), "lp")
		gr1.Add(single_graph)


	xTitle = "Cluster Rate [Hz/cm^{2}]"
	yTitle = "HV_{eff} [V]"

	gr1.GetXaxis().SetTitle(xTitle) 
	gr1.GetYaxis().SetTitle(yTitle)				
	gr1.GetXaxis().SetTitleFont(43)
	gr1.GetYaxis().SetTitleFont(43)	
	gr1.GetXaxis().SetTitleSize(25) 
	gr1.GetYaxis().SetTitleSize(25)						
	gr1.GetXaxis().SetTitleOffset(1) 
	gr1.GetYaxis().SetTitleOffset(1.8)						
						
	gr1.GetXaxis().SetLabelFont(43)
	gr1.GetYaxis().SetLabelFont(43)
	gr1.GetXaxis().SetLabelSize(18)
	gr1.GetYaxis().SetLabelSize(18)						
	gr1.GetXaxis().SetLabelOffset(0.005)
	gr1.GetYaxis().SetLabelOffset(.015)	

	## Disable stats
	ROOT.gROOT.SetBatch()
	ROOT.gStyle.SetOptStat(0)
	ROOT.gStyle.SetOptTitle(0)
		
	## Top text right
	right = ROOT.TLatex()
	right.SetNDC()
	right.SetTextFont(43)
	right.SetTextSize(20)
	right.SetTextAlign(31)
	right.DrawLatex(.95,.93, "GIF++")
	
	## CMS preliminary
	right.SetTextSize(30)
	right.SetTextAlign(13)
	right.DrawLatex(.15,.97,"#bf{CMS} #scale[0.7]{#it{Preliminary}}")

	leg.Draw()
	
	canvas.Update()
	
	canvas.SaveAs("VoltageClusterRate.png")	


def plot_current_clusterRate(nabs, abslist):

	## Graph cosmetics

	# Canvas section
	canvas = TCanvas("canvas","canvas", 600, 600)
	gPad.SetGrid()

	canvas.SetTopMargin(.08)
	canvas.SetRightMargin(0.05)
	canvas.SetBottomMargin(0.13)
	canvas.SetLeftMargin(0.16)

	canvas.SetBorderSize(2)
	canvas.SetFrameFillStyle(0)
	canvas.SetFrameBorderMode(0)
	canvas.SetFrameFillStyle(0)
	canvas.SetFrameBorderMode(0)
	
    # Creates the multigraph
	gr1= TMultiGraph()					
	gr1.Draw( 'AP' )
	
	for i in range(nabs):
		
		print abslist[i]
		single_graph = current_clusterRate_single_plot(abslist[i])
		gr1.Add(single_graph)


	xTitle = "Cluster Rate [Hz/cm^{2}]"
	yTitle = "Current $[\\mu A]$"

	gr1.GetXaxis().SetTitle(xTitle) 
	gr1.GetYaxis().SetTitle(yTitle)				
	gr1.GetXaxis().SetTitleFont(43)
	gr1.GetYaxis().SetTitleFont(43)	
	gr1.GetXaxis().SetTitleSize(25) 
	gr1.GetYaxis().SetTitleSize(25)						
	gr1.GetXaxis().SetTitleOffset(1) 
	gr1.GetYaxis().SetTitleOffset(1.8)						
						
	gr1.GetXaxis().SetLabelFont(43)
	gr1.GetYaxis().SetLabelFont(43)
	gr1.GetXaxis().SetLabelSize(18)
	gr1.GetYaxis().SetLabelSize(18)						
	gr1.GetXaxis().SetLabelOffset(0.005)
	gr1.GetYaxis().SetLabelOffset(.015)	

	## Disable stats
	ROOT.gROOT.SetBatch()
	ROOT.gStyle.SetOptStat(0)
	ROOT.gStyle.SetOptTitle(0)
		
	## Top text right
	right = ROOT.TLatex()
	right.SetNDC()
	right.SetTextFont(43)
	right.SetTextSize(20)
	right.SetTextAlign(31)
	right.DrawLatex(.95,.93, "GIF++")
	
	## CMS preliminary
	right.SetTextSize(30)
	right.SetTextAlign(13)
	right.DrawLatex(.15,.97,"#bf{CMS} #scale[0.7]{#it{Preliminary}}")
	
	canvas.Update()
	
	canvas.SaveAs("CurrentClusteRate.png")

abslist=[6.9, 10, 15, 22, 69]
nabs=len(abslist)
plot_voltage_clusterRate(nabs, abslist)
#plot_current_clusterRate(nabs, abslist)
			
	
#####################################################################################################################
########  CMS-GT  =+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def callPlot(plt_type):

	tree1 = callTree()

	canvas = TCanvas("canvas","canvas", 600, 600)
	gPad.SetGrid()

	canvas.SetTopMargin(.08)
	canvas.SetRightMargin(0.05)
	canvas.SetBottomMargin(0.13)
	canvas.SetLeftMargin(0.16)

	canvas.SetBorderSize(2)
	canvas.SetFrameFillStyle(0)
	canvas.SetFrameBorderMode(0)
	canvas.SetFrameFillStyle(0)
	canvas.SetFrameBorderMode(0)
	

	gr1= TMultiGraph()					
	gr1.Draw( 'AP' )


	treedraw = "ABS:Cluster_rate:Curr_total"
	N=tree1.Draw(treedraw,"","goff")

	if plt_type == "cluster_rate":
		
		
		x=tree1.GetV2()				
		y=tree1.GetV3()

		xTitle = "Cluster Rate [Hz/cm^{2}]"
		yTitle = "Current uA"

		name_plot= "IxCluster_Rate_GT.png"

	if plt_type == "current":
		# Cluster rate and total current
		
		x=tree1.GetV1()				
		y=tree1.GetV2()

		xTitle = "ABS factor"
		yTitle = "Cluster Rate [Hz/cm^{2}]"
		name_plot= "Cluster_Ratexfactor_GT.png"
	


	gr_irr = TGraph(N,x,y)			

	gr_irr.SetMarkerStyle(8)
	gr_irr.SetMarkerSize(1.6)
	gr_irr.SetMarkerColor(2)
	gr_irr.SetLineColor(2)
	gr_irr.Draw( 'AP' )

	gr1.Add(gr_irr)	

	gr1.Draw("AP")
	
	gr1.GetXaxis().SetTitle(xTitle) 
	gr1.GetYaxis().SetTitle(yTitle)				
	gr1.GetXaxis().SetTitleFont(43)
	gr1.GetYaxis().SetTitleFont(43)	
	gr1.GetXaxis().SetTitleSize(25) 
	gr1.GetYaxis().SetTitleSize(25)						
	gr1.GetXaxis().SetTitleOffset(1) 
	gr1.GetYaxis().SetTitleOffset(1.8)						
						
	gr1.GetXaxis().SetLabelFont(43)
	gr1.GetYaxis().SetLabelFont(43)
	gr1.GetXaxis().SetLabelSize(18)
	gr1.GetYaxis().SetLabelSize(18)						
	gr1.GetXaxis().SetLabelOffset(0.005)
	gr1.GetYaxis().SetLabelOffset(.015)						
		
	## Disable stats
	ROOT.gROOT.SetBatch()
	ROOT.gStyle.SetOptStat(0)
	ROOT.gStyle.SetOptTitle(0)
	
	## Legend
	leg = ROOT.TLegend(0.7939799,0.7095622,0.9946488,0.7601751)
	leg.SetBorderSize(0)
	leg.SetFillStyle(0)
	
	lengend_GT="CMS-GT-2-0"
	
	leg.AddEntry(gr_irr, lengend_GT, "lp")
	
	leg.Draw()
	
	## Top text right
	right = ROOT.TLatex()
	right.SetNDC()
	right.SetTextFont(43)
	right.SetTextSize(20)
	right.SetTextAlign(31)
	right.DrawLatex(.95,.93, "GIF++")
	
	## CMS preliminary
	right.SetTextSize(30)
	right.SetTextAlign(13)
	right.DrawLatex(.15,.97,"#bf{CMS} #scale[0.7]{#it{Preliminary}}")
	
	canvas.Update()
	
	canvas.SaveAs(name_plot)					
	
	
	
# Call the function to plot	
#callPlot("cluster_rate")
#callPlot("current")
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	