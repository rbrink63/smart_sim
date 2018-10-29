import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
#import numpy as np 
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox 
import config_file
from config_funcs import get_optimizer_values

# Create a root window that will be hidden. Will act as a driver to 
# all other windows.
root = tk.Tk()
root.withdraw()

class IntroPage:
	def __init__(self):

		#Create the current window
		self.currentWindow = tk.Toplevel(root)
		self.currentWindow.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.currentWindow.title("IntroPage")
		self.currentWindow.geometry('{}x{}'.format(800, 650))
		#SmartSim title 
		self.title = tk.Label(self.currentWindow, text="SmartSim")
		self.title.grid(column=0, row=0)
		self.title.place(relx=.5, rely=.07, anchor="center")
		self.title.config(font=("Courier", 24))

		#Welcome message
		self.welcomeLbl = tk.Label(self.currentWindow, text="Welcome to the SmartSim development tool.")
		self.welcomeLbl.grid(column=0, row=0)
		self.welcomeLbl.place(relx=.5, rely=.2, anchor="center")
		self.welcomeLbl.config(font=("Courier", 14))

		#Select metric
		self.metricLbl = tk.Label(self.currentWindow, text="Select Metric")
		self.metricLbl.grid(column=0, row=0)
		self.metricLbl.place(relx=.5, rely=.35, anchor="center")
		self.metricLbl.config(font=("Courier", 12))

		#Populate the combobox
		self.my_list = []

		for metric in config_file.user_config:
			self.my_list.append(config_file.user_config[metric]["Metric"])
		#Sting to store the comboBox selection
		self.text = tk.StringVar() 
		self.combo = ttk.Combobox(self.currentWindow, textvariable=self.text)
		self.combo['values'] = self.my_list
		self.combo.current(1)
		self.combo.grid(column=0, row=1)
		self.combo.place(relx=.5, rely=.4, anchor="center")
		
		#Called when the user makes a selection within the combobox
		def callback(eventObject):
			self.Open(self.text.get())

		self.combo.bind("<<ComboboxSelected>>", callback)
	
	#Can be called to close the IntroPage
	def close(self):
		self.currentWindow.destroy()
	#Opens the MainPage
	def Open(self, selection):
		#TODO: Most of this code needs to be placed in a global function of some sort.
		selected_model = "config_"+selection
		query = config_file.user_config[selected_model]

		#get params
		design_params = query["design_params"]
		devsim_params = query["devsim_params"]
		optimizer_params = query["optimizer_params"]
		#2d array to hold all types of params
		allParams = [design_params, devsim_params, optimizer_params]

		#start parsing the model equation and filling in values
		modelEq = query["Model"]
		for index in design_params:
			modelEq = modelEq.replace(index, str(query[index]))
		for index in devsim_params:
			#here is where devsim may need to be called
			modelEq = modelEq.replace(index, str(query[index]))

		if len(optimizer_params) > 0:
			if query[optimizer_params[0]] == "":
				get_optimizer_values(selected_model)
				query = config_file.user_config[selected_model]

		for index in optimizer_params:
			#check if param values exist
			modelEq = modelEq.replace(index, str(query[index]))

		#generate data points
		opt_x_data = query["opt_x_data"]
		x_axis = query["x_axis"]
		Y_dataPoints = []
		for dataPoint in opt_x_data:
			currentEq = modelEq.replace(x_axis, str(dataPoint))
			Y_dataPoints.append(eval(currentEq))
		#Code that needs to be placed elsewhere stops here
		self.close()
		self.app = MainPage(opt_x_data, Y_dataPoints, selection, allParams)
	
	# Called when the user hits 'X'
	def on_closing(self):
		self.currentWindow.destroy
		if messagebox.askokcancel("Quit", "Do you want to quit?"):
			root.destroy()
		

class MainPage:
	def __init__(self, X_dataPoints, Y_dataPoints, metricName, allParams):

		#Create the current window
		self.currentWindow = tk.Toplevel(root)
		self.currentWindow.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.currentWindow.title("MainPage")
		self.currentWindow.geometry('{}x{}'.format(800, 650))
		#SmartSim title 
		self.title = tk.Label(self.currentWindow, text="SmartSim")
		self.title.grid(column=0, row=0)
		self.title.place(relx=.5, rely=.07, anchor="center")
		self.title.config(font=("Courier", 24))
		#Other options
		self.otherLbl = tk.Label(self.currentWindow, text="Other Options")
		self.otherLbl.grid(column=0, row=0)
		self.otherLbl.place(relx=.2, rely=.15, anchor="e")
		self.otherLbl.config(font=("Courier", 12))
		#Overlay Button
		self.overlayBtn = tk.Button(self.currentWindow, text="Overlay Simulated Data", bg="deep sky blue")
		self.overlayBtn.grid(column=0, row=0)
		self.overlayBtn.place(relx=.25, rely=.19, anchor="e")
		#Select new metric 
		self.metricLbl = tk.Label(self.currentWindow, text="Select New Metric")
		self.metricLbl.grid(column=0, row=0)
		self.metricLbl.place(relx=.25, rely=.28, anchor="e")
		self.metricLbl.config(font=("Courier", 12))
		#metric combobox
		self.my_list = []

		for metric in config_file.user_config:
			self.my_list.append(config_file.user_config[metric]["Metric"])
		#Sting to store the comboBox selection
		self.text = tk.StringVar() 
		self.combo = ttk.Combobox(self.currentWindow, textvariable=self.text)
		self.combo['values'] = self.my_list
		self.combo.current(1)
		self.combo.grid(column=0, row=1)
		self.combo.place(relx=.25, rely=.315, anchor="e")
		
		#Called when the user makes a selection within the combobox
		def callback(eventObject):
			self.Open()

		self.combo.bind("<<ComboboxSelected>>", callback)

		#parameters
		self.paramLbl = tk.Label(self.currentWindow, text="Design Parameters")
		self.paramLbl.grid(column=0, row=0)
		self.paramLbl.place(relx=.24, rely=.4, anchor="e")
		self.paramLbl.config(font=("Courier", 12))

		#dynamically create buttons representing the params
		design_buttons = []
		counter = 0
		for index in allParams[0]:
			self.button = tk.Button(self.currentWindow, text=allParams[0][counter], bg="deep sky blue")
			self.button.grid(column=0, row=0)
			self.button.place(relx=.12+(counter*.1), rely=.45, anchor="e")
			design_buttons.append(self.button)

		#parameters
		self.paramLbl = tk.Label(self.currentWindow, text="Devsim Parameters")
		self.paramLbl.grid(column=0, row=0)
		self.paramLbl.place(relx=.24, rely=.5, anchor="e")
		self.paramLbl.config(font=("Courier", 12))

		devsim_buttons = []
		counter = 0
		for index in allParams[1]:
			self.button = tk.Button(self.currentWindow, text=allParams[1][counter], bg="deep sky blue")
			self.button.grid(column=0, row=0)
			self.button.place(relx=.12+(counter*.1), rely=.55, anchor="e")
			devsim_buttons.append(self.button)

		#parameters
		self.paramLbl = tk.Label(self.currentWindow, text="opt Parameters")
		self.paramLbl.grid(column=0, row=0)
		self.paramLbl.place(relx=.24, rely=.6, anchor="e")
		self.paramLbl.config(font=("Courier", 12))

		opt_buttons = []
		counter = 0
		for index in allParams[2]:
			self.button = tk.Button(self.currentWindow, text=allParams[2][counter], bg="deep sky blue")
			self.button.grid(column=0, row=0)
			self.button.place(relx=.12+(counter*.1), rely=.65, anchor="e")
			opt_buttons.append(self.button)

		#GRAPH
		plt.plot(X_dataPoints, Y_dataPoints)
		plt.xlabel('X_Axis_Title')
		plt.ylabel('Y_Axis_Title')
		plt.title("Metric: "+metricName)
		plt.grid(True)
		plt.savefig(metricName+".png")
		plt.show()
		
	def close_windows(self):
		self.self.currentWindow.destroy()
	# Called when the user hits 'X'
	def on_closing(self):
		self.currentWindow.destroy
		if messagebox.askokcancel("Quit", "Do you want to quit?"):
			root.destroy()

def main():
	app = IntroPage()
	root.mainloop()

if __name__ == '__main__':
	main()

	
