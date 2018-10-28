import matplotlib.pyplot as plt
#import numpy as np 
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox 
import config_file

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
			self.Open()
			print(self.text.get())

		self.combo.bind("<<ComboboxSelected>>", callback)
	
	#Can be called to close the IntroPage
	def close(self):
		self.currentWindow.destroy()
	#Opens the MainPage
	def Open(self):
		self.app = MainPage()
		self.close()
	# Called when the user hits 'X'
	def on_closing(self):
		self.currentWindow.destroy
		if messagebox.askokcancel("Quit", "Do you want to quit?"):
			root.destroy()
		

class MainPage:
	def __init__(self):

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
			print(self.text.get())

		self.combo.bind("<<ComboboxSelected>>", callback)

		#parameters
		self.paramLbl = tk.Label(self.currentWindow, text="Parameters Shown Below")
		self.paramLbl.grid(column=0, row=0)
		self.paramLbl.place(relx=.3, rely=.4, anchor="e")
		self.paramLbl.config(font=("Courier", 12))


		#GRAPH

		plt.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])
		plt.xlabel('time (s)')
		plt.ylabel('voltage (mV)')
		plt.title('About as simple as it gets, folks')
		plt.grid(True)
		plt.savefig("test.png")
		plt.show()
		self.canvas = FigureCanvasTkAgg(self.f, self.currentWindow)
		self.canvas.show()
		
	def close_windows(self):
		self.self.currentWindow.destroy()
	# Called when the user hits 'X'
	def on_closing(self):
		self.currentWindow.destroy
		#if messagebox.askokcancel("Quit", "Do you want to quit?"):
		root.destroy()

def main():
	app = IntroPage()
	root.mainloop()

if __name__ == '__main__':
	main()

	
