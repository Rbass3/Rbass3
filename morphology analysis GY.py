#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 13:06:57 2022

@author: robertbass
"""

#this script uses pandas and tkinter to automate the analysis of a large number of data frames generated from microscope image analysis. 
#it creates a simple user interface to make the program user-friendly for a lab-mate of mine who does know how to program.

#a program we use in my lab to analyze microscopy images produces a large number of excel spreadsheets, one for each image. 
#this program opens each of those excel spreadsheets, extracts out the data from them, places them in a data frame, and saves that as its own CSV file.
#this alleviates the need for hours of copy-pasting.

import os
import pandas as pd
import ntpath
import tkinter as tk
from PIL import ImageTk, Image
import statistics
import openpyxl

from io import BytesIO
import base64
from pic2str import fatmouse


# pip install pathlib2



#IF YOU GET "file is not a zip file" THEN MAKE SURE ALL EXCEL FILES ARE CLOSED
#AND THERE ARE NO CORRUPT EXCEL FILES IN THE FOLDER

# this one contains soma size info
def get_cell_info(excel_file):
    try:
        excel_file2 = pd.ExcelFile(excel_file, engine = "openpyxl")
        individual_totals = pd.read_excel(
            excel_file2, "Individual Totals-Dendrite",
            engine = "openpyxl"
            )
        neuron_summary = pd.read_excel(
            excel_file2, "Neuron Summary",
            engine = "openpyxl"
            )
    except:
        return
    
    individual_arbors = individual_totals.iloc[0:,1]
    total_arbor_length = sum(individual_totals.iloc[0:,1])
    average_arbor_length = statistics.mean(individual_totals.iloc[0:,1])
    arbor_number = len(individual_totals.iloc[0:,1])
    cell_area = neuron_summary.iloc[2, 15]
    soma_size = neuron_summary.iloc[0, 13]
    cell_info = [individual_arbors, total_arbor_length, average_arbor_length,
                  arbor_number, cell_area, soma_size]
    return cell_info
    

# test = get_cell_info("/Users/robertbass/Dropbox (UFL)/Xu Lab 20230110/Data/5xFAD astrocyte tracing/6 month 5xCre/excel sheets/P post cell 1.xlsx")
# print(test)

#extrapolated cell density from stereo investigator
def get_density(excel_file):
    try:
        excel_file2 = pd.ExcelFile(excel_file, engine = "openpyxl")
        summary_page = pd.read_excel(
            excel_file2, "Summary",
            engine = "openpyxl"
            )
    except:
        return 
    
    #Estimated Population using Mean Section Thickness with Counts"
    number_of_cells = summary_page.iloc[0, 9]
    counting_frame = summary_page.iloc[0, 16]
    hippo_area = summary_page.iloc[0, 17]
    thickness = summary_page.iloc[0, 7]
    try:
        density2D = number_of_cells/hippo_area
    except:
        density2D = "divide by 0"
        
    try:
        density3D = number_of_cells/(hippo_area*thickness)
    except:
        density3D = "divide by 0"    

    info = [number_of_cells, counting_frame, hippo_area,
            thickness, density2D, density3D]
    return info;

#real cell density
def get_real_density(excel_file):
    try:
        excel_file2 = pd.ExcelFile(excel_file, engine = "openpyxl")
        contour_details = pd.read_excel(
            excel_file2, "Contour Details",
            engine = "openpyxl"
            )
        marker_summary = pd.read_excel(
            excel_file2, "Marker Summary",
            engine = "openpyxl"
            )
    except:
        return 
    
    number_of_cells = marker_summary.iloc[0, 2]
    area = contour_details.iloc[0, 3]
    density_ = number_of_cells/area
   

    info = [number_of_cells, area, density_, density_ * 10**3]
    return info;

# get_real_density("/Users/robertbass/Dropbox (UFL)/Xu Lab 20230110/Data/5xFAD astrocyte tracing/6 month 5xCre/excel sheets/F ant hippo.xlsx")


def deblind(file_):
    string_list = file_.split()
    fbfb = ["B", "C", "G", "I"]
    x5x = ["D","F","J","K"]
    gfap = ["A","H","L","P"]
    x5xCre = ["E","M","N","O"]
    if string_list[0] in fbfb: group = "fB/fB"
    elif string_list[0] in x5x:  group = "5xFAD fB/fB"
    elif string_list[0] in gfap:  group = "GFAP-CreER fB/fB"
    elif string_list[0] in x5xCre:  group = "5xFAD GFAP-CreER fB/fB"
    else: group = "none"
    return group


#column B2 in excel is [0,1]
#column B3 in excel is [0,2]

#form the data from excel docs into lists and save as an excel sheet
# def make_data_list(filepath__ = input("data folder:")):
def make_data_list(filepath_):
    #trims off quotes and the final slash:
    # filepath_ = filepath_[1:-2]
    os.chdir(str(filepath_))
    filelist = os.listdir(filepath_)
    filelist.sort()
    IAlist = pd.DataFrame({
        "File Name":[],
        "Group":[],
        "Individual Arbors":[]})
    TALlist = pd.DataFrame({
        "File Name":[],
        "Group":[],
        "Total Arbor Length":[]})
    AALlist = pd.DataFrame({
        "File Name":[],
        "Group":[],
        "Average Arbor Length":[]})
    ANlist = pd.DataFrame({
        "File Name":[],
        "Group":[],
        "Arbor Number":[]})
    CAlist = pd.DataFrame({
        "File Name":[],
        "Group":[],
        "Cell Area":[]})
    SSlist = pd.DataFrame({
        "File Name":[],
        "Group":[],
        "Soma Size":[]})
    
    
    for file_ in filelist:
        if file_ != ".DS_Store" and str(file_)[-5:] == ".xlsx":
            excel_file2 = pd.ExcelFile(file_, engine = "openpyxl")
            try:
                pd.read_excel(
                    excel_file2, "Individual Totals-Dendrite",
                    engine = "openpyxl")
            except:
                continue
            
            
            cell_info = get_cell_info(str(file_))
            
            count = 0
            for item in cell_info[0]:
                IAlist.loc[len(IAlist.index)] = [file_[0:-5],
                                                 deblind(file_),
                                                 cell_info[0][count]]
                count += 1
            # total arbor length
            TALlist.loc[len(TALlist.index)] = [file_[0:-5],
                                               deblind(file_),
                                               cell_info[1]]
            #average arbor length
            AALlist.loc[len(AALlist.index)] = [file_[0:-5],
                                               deblind(file_),
                                               cell_info[2]] 
            # arbor number
            ANlist.loc[len(ANlist.index)] = [file_[0:-5], deblind(file_), cell_info[3]]
            # cell area
            CAlist.loc[len(CAlist.index)] = [file_[0:-5], deblind(file_), cell_info[4]]
            #soma size
            SSlist.loc[len(SSlist.index)] = [file_[0:-5], deblind(file_), cell_info[5]]


    #Cell density list        
    CDlist = pd.DataFrame({
        "File Name":[],
        "Group":[],
        "Number Of Cells":[],
        "Counting Frame Area":[],
        "Sampling Grid Area":[],
        "Thickness":[],
        "Density 2D":[],
        "Density 3D":[]})
    
    #cell density extrapolation from stereo investigator files
    for file_ in filelist:
        if file_ != ".DS_Store" and str(file_)[-5:] == ".xlsx":
            excel_file2 = pd.ExcelFile(file_, engine = "openpyxl")
            try:
                pd.read_excel(
                    excel_file2, "Summary",
                    engine = "openpyxl")
            except:
                continue
            info = get_density(str(file_))
        
        #number_of_cells, counting_frame, hippo_area, thickness, density2D, density3D]
            CDlist.loc[len(CDlist.index)] = [file_[0:-5],
                                             deblind(file_),
                                             info[0],
                                             info[1],
                                             info[2],
                                             info[3], 
                                             info[4],
                                             info[5]]
            
    #Real Cell density list        
    RealCDlist = pd.DataFrame({
        "File Name":[],
        "Group":[],
        "Number Of Cells":[],
        "Area (um^2)":[],
        "Cells/um^2":[],
        "Cells/um^2*10^3":[]})
    

    for file_ in filelist:
        if file_ != ".DS_Store" and str(file_)[-5:] == ".xlsx":
            excel_file2 = pd.ExcelFile(file_, engine = "openpyxl")
            try:
                pd.read_excel(
                    excel_file2, "Contour Summary",
                    engine = "openpyxl")
            except:
                continue
            real_density_info = get_real_density(str(file_))
        
            RealCDlist.loc[len(RealCDlist.index)] = [file_[0:-5],
                                                 deblind(file_),
                                                 real_density_info[0],
                                                 real_density_info[1],
                                                 real_density_info[2],
                                                 real_density_info[3]]
                                             
            
            
    # all_data = [IAlist, TALlist]
    all_data = [["Individual Arbor Length", IAlist],
                ["Total Arbor Length", TALlist],
                ["Average Arbor Length", AALlist],
                ["Arbor Number", ANlist],
                ["Cell Area", CAlist],
                ["Soma Size", SSlist],
                ["Cell Density", CDlist],
                ["Cortical Cell Density", RealCDlist]]
    for item in all_data: item[1].sort_values(by=['Group', "File Name"], inplace = True)
    return all_data



def save_files(all_data, filepath_):
    #create empty excel file_ 
    newname = str(ntpath.basename(filepath_)) + " analysis.xlsx" 
    writer = pd.ExcelWriter(newname, engine = 'xlsxwriter')
    
    #fill excel object with my info
    count = 0
    for file_ in all_data:
        all_data[count][1].to_excel(writer, sheet_name = all_data[count][0], index = False)
        all_data[count][1].to_csv(ntpath.basename(filepath_) + " " + all_data[count][0] + ".csv")
        count += 1
    writer.save()
    # writer.close()
    
    os.system("open -a 'Microsoft Excel.app' '%s'" % newname)
    
    
def run_all(filepath_):
    data = make_data_list(filepath_)
    save_files(data, filepath_)
    
    
# run_all("/Users/robertbass/Dropbox (UFL)/Xu Lab 20230110/Data/5xFAD astrocyte tracing/6 month 5xCre/excel sheets")

# data = make_data_list("/Users/robertbass/Dropbox (UFL)/Xu Lab 20230110/Data/5xFAD astrocyte tracing/6 month 5xCre/excel sheets")

    
    # windows:
    # os.system("start EXCEL.EXE " + newname)
    
    # newname = Path.Path(newname).resolve()
    # os.system('start excel.exe "{newname}"')
    
    # print(IAlist.head())       
    # print(TALlist.head())
    # print(ANlist.head())
    # print(CAlist.head())    


WIDTH = 600
HEIGHT = 300

# fullwd = os.path.realpath(__file__)
# wd = fullwd[:-38] + "/" 
# fullwd = os.getcwd()
# wd = fullwd[:-25] 

# path = wd + "fatmouse.png"
#this line trims off the file name "morphology analysis countour details"
#this can be written much better

window = tk.Tk() #this line starts the window loop

canvas = tk.Canvas(window, height = HEIGHT, width = WIDTH)
canvas.pack()

frame = tk.Frame(window)
frame.place(relx=0.05, rely = 0.125, relwidth = 0.9, relheight = 0.75)

window.title("Hi Guey Ying")

label = tk.Label(frame, text="Astrocyte Morphology Analysis")
label.place(anchor = 'n',
            relx = 0.4, rely = 0.27, relwidth = 0.4, relheight = 0.1)

# label = tk.Label(frame, text="(Don't forget to close excel files)")
# label.place(anchor = 'n',
#             relx = 0.4, rely = 0.37, relwidth = 0.55, relheight = 0.1)

#this works
# path = "fatmouse.png"



  # Load byte data
byte_data = base64.b64decode(fatmouse)
image_data = BytesIO(byte_data)
mouse = Image.open(image_data)
mouse2 = mouse.resize((100, 100))
mouse3 = ImageTk.PhotoImage(mouse2, master = frame)
mouselabel = tk.Label(window, image = mouse3)
mouselabel.place(anchor = 'n',
                  relx = 0.77, rely = 0.2, relwidth = 0.4, relheight = 0.3)

#this works
# mouse = Image.open(path)
# mouse2 = mouse.resize((100, 100))
# mouse3 = ImageTk.PhotoImage(mouse2, master = frame)
# mouselabel = tk.Label(window, image = mouse3)
# mouselabel.place(anchor = 'n',
#                   relx = 0.77, rely = 0.2, relwidth = 0.4, relheight = 0.3)

button = tk.Button(frame, text="Analyze",
                    command = lambda:  run_all(entry.get()))
button.place(relx = 0.7, rely = 0.6, relwidth = 0.2, relheight = 0.2)

entry = tk.Entry(frame)
entry.place(anchor = 'n', relx = 0.4, rely = 0.6, relwidth = 0.6, relheight=0.2)

window.mainloop()

