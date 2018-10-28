from tkinter import *
from tkinter.ttk import * 
import config_file


class IntroPage:
	def __init__(self, master):
		self.master = master
		master.geometry('{}x{}'.format(800, 650))
		#SmartSim title 
		self.title = Label(master, text="SmartSim")
		self.title.grid(column=0, row=0)
		self.title.place(relx=.5, rely=.07, anchor="center")
		self.title.config(font=("Courier", 24))

		#Welcome message
		self.welcomeLbl = Label(master, text="Welcome to the SmartSim development tool.")
		self.welcomeLbl.grid(column=0, row=0)
		self.welcomeLbl.place(relx=.5, rely=.2, anchor="center")
		self.welcomeLbl.config(font=("Courier", 14))

		#Select metric
		self.metricLbl = Label(master, text="Select Metric")
		self.metricLbl.grid(column=0, row=0)
		self.metricLbl.place(relx=.5, rely=.35, anchor="center")
		self.metricLbl.config(font=("Courier", 12))

		#Populate the combobox
		self.my_list = []

		for metric in config_file.user_config:
			self.my_list.append(config_file.user_config[metric]["Metric"])
		#Sting to store the comboBox selection
		self.text = StringVar() 
		self.combo = Combobox(master, textvariable=self.text)
		self.combo['values'] = self.my_list
		self.combo.current(1)
		self.combo.grid(column=0, row=1)
		self.combo.place(relx=.5, rely=.4, anchor="center")
		
		def callback(eventObject):
			self.Open()
			print(self.text.get())

		self.combo.bind("<<ComboboxSelected>>", callback)

		#Can be called to close the IntroPage
	def close(self):
		self.master.destroy()
		self.new_window
	#Opens the MainPage
	def Open(self):
		print("I was called")
		self.new_window = Toplevel(self.master)
		self.app = MainPage(self.new_window)

class MainPage:
	def __init__(self, master):
		print("here")
		self.master = master
		master.geometry('{}x{}'.format(800, 650))
		#Welcome message
		self.welcomeLbl = Label(master, text="Welcome to the Next page!!!!.")
		self.welcomeLbl.grid(column=0, row=0)
		self.welcomeLbl.place(relx=.5, rely=.2, anchor="center")
		self.welcomeLbl.config(font=("Courier", 14))

	def close_windows(self):
		self.master.destroy()

def main():
	root = Tk()
	app = IntroPage(root)
	root.mainloop()

if __name__ == '__main__':
	main()

	
