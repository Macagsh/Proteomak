# -*- coding: utf-8 -*-
"""
Created on Mon May 20 13:18:28 2019

Programa: Proteomak 1.0

@author: Macagsh
"""
"""This is the module docstring"""
#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""libraries"""
from tkinter import *
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, Checkbutton
import PIL
from PIL import Image, ImageDraw, ImageTk
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
from matplotlib_venn import venn2, venn3
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import iplot, init_notebook_mode
import plotly.io as pio
import os
from io import open

   
"""definitions and classes"""
def welcome():
    """ It opens a welcome image on the info button"""
    img=Image.open('img\welcome.png')
    img=ImageTk.PhotoImage(img)
    lblfoto.config(image=img).pack(fill=tk.BOTH)
    

def exitproteomak():
    """ It exits the program when exit button is pushed"""
    root.destroy()
    quit
    
def import_data():
    """ It imports data from a csv file to be use for graph generation"""
    file = filedialog.askopenfilename(parent=root, title='Please select a file')
    if len(file) > 0:
        status.set("File uploaded")
        print ("You chose %s" % file)
        global gfilename
        gfilename = file
       
def helpdata():
    """ in future will show on the screen the how to import the data info"""
    pass
def other_help():
    """ in future will show on the screen Other help info"""
    pass

class StatusBar(tk.Frame):
    """ It is a class with functions for showing the status bar"""

    def __init__(self, master):
        """ It initiates the class function and shows a label with the satus bar on the bottom"""
        tk.Frame.__init__(self, master)
        self.label = tk.Label(self, bd=1, relief="sunken", anchor="w")
        self.label.pack(fill=tk.X)

    def set(self, format, *args):
        """ It gives format to the status bar"""
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        """ It clears the status bar"""
        self.label.config(text="")
        self.label.update_idletasks()

def graficoHeat():
    """ It generates a Heatmap from the imported file and shows the image on the window"""
    global  gfilename 
    print(gfilename)
    file = pd.read_csv(gfilename, sep=";")
    print(file)
    ratio=np.array(file)
    print(ratio)
    j = 0
    z = []
    for i in ratio:
        z.append(i[1:])
    print(z[:])
    x=['sample1', 'sample2']
    y=file['Proteins']   
    data = [
        go.Heatmap(
            z=z,
            x=x,
            y=y,
            colorscale=[
                [0.0, 'rgb(255.99609375, 0.0, 0.0)'],[0.1, 'rgb(255.99609375, 0.0, 0.0)'],
                [0.5, 'rgb(0,0,0)'], 
                [1.0, 'rgb(0.0, 121.47265625, 0.0)']]
        )
    ]
    
    layout = go.Layout(
        title='Protein expression levels',
        xaxis = dict(ticks='', nticks=36),
        yaxis = dict(ticks='' )
    )
    
    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig, filename='prot_exp_heatmap')
    pio.write_image(fig, 'heatmap.png')
    
    """Shows the image of heatmap"""
    img=Image.open('heatmap.png')
    img=ImageTk.PhotoImage(img)
    lblfoto.config(image=img).pack(fill=tk.BOTH)
        
def graficoVenn():
    """ It generates a Venn diagram from the imported file and shows the image on the window"""
    """data importation"""
    global  gfilename 
    print(gfilename)
    file = pd.read_csv(gfilename, sep=";")
    print(file)
    sample1=file["sample1"]
    sample2=file["sample2"]
    sample3=file["sample3"]
    """sample correction"""
    samplecorr1 = correct_samples(sample1)
    print(samplecorr1)
    samplecorr2 = correct_samples(sample2)
    print(samplecorr2)
    samplecorr3 = correct_samples(sample3)
    print(samplecorr3)
   
    lista =[]
    if len(set(samplecorr1)) > 0: lista.append (set(samplecorr1))
    if len(set(samplecorr2)) > 0: lista.append (set(samplecorr2))
    if len(set(samplecorr3)) > 0: lista.append (set(samplecorr3))

    if len(lista) == 3 :
        v=venn3(lista)
        print("all samples")
        matplotlib.pyplot.plot()
        matplotlib.pyplot.savefig('venn_diagram.png')
    elif len(lista) == 2 :
        v=venn2(lista)
        print("2 samples")
        matplotlib.pyplot.plot()
        matplotlib.pyplot.savefig('venn_diagram.png')
    else:
        print("not possible to generate Venn diagram, add more samples")

    """ Shows the image of venn diagram"""
    img=Image.open('venn_diagram.png')
    img=ImageTk.PhotoImage(img)
    lblfoto.config(image=img).pack(fill=tk.BOTH)

def correct_samples(sample):
    """ It corrects the data from the file used for Venn Diagram. It takes out the Nan values from the panda generated to generate the Veen Diagram correctly"""
    samplecorr = []
    for valores in sample:
        if math.isnan(valores) != True:
            samplecorr.append(valores)
    return samplecorr       

"""Root configuration"""
     
root = tk.Tk()
root.title("Proteomak")
root.geometry("800x500")

"""Creates the menu"""
menubar = tk.Menu(root)

"""Creates welcome drop-down menu with the different options"""
menu_welcome = tk.Menu(menubar, tearoff=0)
menu_welcome.add_command(label="Info", command=welcome)
menu_welcome.add_separator()
menu_welcome.add_command(label="Exit", command=exitproteomak)
menubar.add_cascade(label="Welcome", menu=menu_welcome)
menu_import = tk.Menu(menubar, tearoff=0)
menu_import.add_command(label="Import data csv", command=import_data)
menubar.add_cascade(label="Import", menu=menu_import)
menu_graph = tk.Menu(menubar, tearoff=0)
menu_graph.add_command(label="Venn", command=graficoVenn)
menu_graph.add_command(label="Heat", command=graficoHeat)
menubar.add_cascade(label="Graph", menu=menu_graph)
menu_help = tk.Menu(menubar, tearoff=0)
menu_help.add_command(label="How to import data...", command=helpdata)
menu_help.add_separator()
menu_help.add_command(label="Other help", command=other_help)
menubar.add_cascade(label="Help", menu=menu_help)

"""To show the menu"""
root.config(menu=menubar)

frameC = Frame(root, width=500, height=500, relief="sunken")
img=Image.open('img\proteomak.png')
img = img.resize((800,500), Image.ANTIALIAS)
img=ImageTk.PhotoImage(img)
lblfoto = Label(frameC, image=img)
lblfoto.pack(fill=tk.BOTH, padx=10)
frameC.pack()
"""Opens welcome file"""
file = open ("welcome.txt", "r")
print(file)
content = file.read()
print(content)
text_file = Text(root)
text_file.insert('insert', content)
text_file.pack(fill='both', expand=1)
text_file.config(padx=6, pady=4, bd=0, font=("Consoles", 12))

"""Status bar"""
status = StatusBar(root)
status.set("Status Bar")
status.pack(side=tk.BOTTOM)

"""To show the windows"""
root.mainloop()




 