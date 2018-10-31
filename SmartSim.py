#SmartSim GUI

#Imports
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox 
import config_file
from config_funcs import get_optimizer_values, get_devsim_values

# Create a root window that will be hidden. Will act as a driver to 
# all other windows.
root = tk.Tk()
#root.geometry("500,100 300, 300")
root.withdraw()

class IntroPage:
    def __init__(self):
        #Create the current window
        self.currentWindow = tk.Toplevel(root)
        self.currentWindow.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.currentWindow.title("IntroPage")
        self.currentWindow.geometry('{}x{}'.format(800, 650))
        #LABEL: SmartSim title 
        self.title = tk.Label(self.currentWindow, text="SmartSim")
        self.title.grid(column=0, row=0)
        self.title.place(relx=.5, rely=.07, anchor="center")
        self.title.config(font=("Courier", 24))
        #LABEL: Welcome message
        self.welcomeLbl = tk.Label(self.currentWindow, text="Welcome to the SmartSim development tool.")
        self.welcomeLbl.grid(column=0, row=0)
        self.welcomeLbl.place(relx=.5, rely=.2, anchor="center")
        self.welcomeLbl.config(font=("Courier", 14))
        #LABEL: Select metric
        self.metricLbl = tk.Label(self.currentWindow, text="Select Metric")
        self.metricLbl.grid(column=0, row=0)
        self.metricLbl.place(relx=.5, rely=.35, anchor="center")
        self.metricLbl.config(font=("Courier", 12))

        #Create a List that will be used to fill the comboBox
        self.my_list = []
        for metric in config_file.user_config:
            print("here")
            self.my_list.append(config_file.user_config[metric]["Metric"])

        #COMBOBOX: Select Model to Load
        self.text = tk.StringVar() 
        self.combo = ttk.Combobox(self.currentWindow, textvariable=self.text)
        self.combo['values'] = self.my_list
        self.combo.current(1)
        self.combo.grid(column=0, row=1)
        self.combo.place(relx=.5, rely=.4, anchor="center")
        
        #Called when the user makes a selection within the combobox
        def callback(eventObject):
            self.Open(self.text.get())
        # This binds the event that occurs when a user makes a selection 
        # within the combobox to the callback function above.
        self.combo.bind("<<ComboboxSelected>>", callback)
    
    #Called to close the IntroPage when transitioning to a new page
    def close(self):
        self.currentWindow.destroy()
    #Initiates opening the main page which contains the plot
    def Open(self, selection):
        self.close()
        loadModel(selection)
    # Captures the event of a user hitting the red 'X' button to close a window
    def on_closing(self):
        self.currentWindow.destroy
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            #The following line will kill the entire application
            root.destroy()     

class MainPage:
    def __init__(self, X_dataPoints, Y_dataPoints, metricName, allParams):
        #Create the current window
        self.currentWindow = tk.Toplevel(root)
        self.currentWindow.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.currentWindow.title("MainPage")
        self.currentWindow.geometry("1000x680+200+0")
        #self.currentWindow.geometry('{}x{}'.format(1000, 650))
        #LABEL: SmartSim title 
        self.title = tk.Label(self.currentWindow, text="SmartSim")
        self.title.place(relx=.5, rely=.05, anchor="center")
        self.title.config(font=("Courier", 24))
        #LABEL: Other options
        self.otherLbl = tk.Label(self.currentWindow, text="Other Options")
        self.otherLbl.place(relx=.025, rely=.12)
        self.otherLbl.config(font=("Courier", 12))
        #BUTTON: Overlay Button
        self.overlayBtn = tk.Button(self.currentWindow, text="Overlay Simulated Data", bg="deep sky blue")
        self.overlayBtn.place(relx=.025, rely=.16)
        #LABEL: Select new metric 
        self.metricLbl = tk.Label(self.currentWindow, text="Select New Metric")
        self.metricLbl.place(relx=.025, rely=.23)
        self.metricLbl.config(font=("Courier", 12))
        
        #Create a List that will be used to populate the combobox
        self.my_list = []

        #Load all models that are currently stored in the configuration file
        for metric in config_file.user_config:
            self.my_list.append(config_file.user_config[metric]["Metric"])
        #Sting to store the comboBox selection
        self.text = tk.StringVar() 
        #COMBOBOX: Select Model to Load
        self.combo = ttk.Combobox(self.currentWindow, textvariable=self.text)
        self.combo['values'] = self.my_list
        self.combo.current(1)
        self.combo.grid(column=0, row=1)
        self.combo.place(relx=.025, rely=.27)
        
        #Called when the user makes a selection within the combobox
        def callback(eventObject):
            self.Open()
        self.combo.bind("<<ComboboxSelected>>", callback)

        #LABEL: Design Parameters
        self.paramLbl = tk.Label(self.currentWindow, text="Design Parameters")

        self.paramLbl.place(relx=.025, rely=.32)
        self.paramLbl.config(font=("Courier", 12))

        #dynamically create buttons representing the params
        design_buttons = []
        counter = 0
        column = 0
        row = 0
        for index in allParams[0]:
            #LABEL: label for the current param
            self.Lbl = tk.Label(self.currentWindow, text=allParams[0][counter]+":")
            self.Lbl.place(relx=.025+(column*.1), rely=.36+(row*.05))
            self.Lbl.config(font=("Courier", 12))            

            self.entry = tk.Entry(self.currentWindow, width=8)
            self.entry.place(relx=.051+(column*.1), rely=.36+(row*.05))
            design_buttons.append(self.entry)
            counter = counter + 1
            row = row + 1
            if row == 3:
                row = 0
                column = column + 1

        #LABEL: Devsim Parameters
        self.paramLbl = tk.Label(self.currentWindow, text="Devsim Parameters")
        self.paramLbl.place(relx=.025, rely=.52)
        self.paramLbl.config(font=("Courier", 12))

        #Dynamically create buttons representing the params
        devsim_buttons = []
        counter = 0
        column = 0
        row = 0
        for index in allParams[1]:
            #LABEL: label for the current param
            self.Lbl = tk.Label(self.currentWindow, text=allParams[1][counter]+":")
            self.Lbl.place(relx=.025+(column*.1), rely=.56+(row*.05))
            self.Lbl.config(font=("Courier", 12))            

            self.entry = tk.Entry(self.currentWindow, width=8)
            self.entry.place(relx=.051+(column*.1), rely=.56+(row*.05))
            design_buttons.append(self.entry)
            counter = counter + 1
            row = row + 1
            if row == 3:
                row = 0
                column = column + 1

        #LABEL: Optimizer Parameters
        self.paramLbl = tk.Label(self.currentWindow, text="opt Parameters")
        self.paramLbl.place(relx=.025, rely=.72)
        self.paramLbl.config(font=("Courier", 12))
        #Dynamically create buttons representing the params
        opt_buttons = []
        counter = 0
        column = 0
        row = 0
        for index in allParams[2]:
            #LABEL: label for the current param
            self.Lbl = tk.Label(self.currentWindow, text=allParams[2][counter]+":")
            self.Lbl.place(relx=.025+(column*.1), rely=.76+(row*.05))
            self.Lbl.config(font=("Courier", 12))            

            self.entry = tk.Entry(self.currentWindow, width=8)
            self.entry.place(relx=.051+(column*.1), rely=.76+(row*.05))
            design_buttons.append(self.entry)
            counter = counter + 1
            row = row + 1
            if row == 3:
                row = 0
                column = column + 1
        
        #GRAPH        
        fig = Figure(figsize=(6,6))
        plot = fig.add_subplot(111)
        plot.plot(X_dataPoints, Y_dataPoints, color='blue')
        plot.set_title ("Estimation Grid", fontsize=14)
        plot.set_ylabel("Y", fontsize=14)
        plot.grid(True)
        plot.set_xlabel("X", fontsize=14)
        canvas = FigureCanvasTkAgg(fig, master=self.currentWindow)
        canvas.get_tk_widget().place(relx=0.39, rely=0.1)
        canvas.draw()
        #GRAPH
        #plt.plot(X_dataPoints, Y_dataPoints)
        #plt.xlabel('X_Axis_Title')
        #plt.ylabel('Y_Axis_Title')
        #plt.title("Metric: "+metricName)
        #plt.grid(True)
        #plt.savefig(metricName+".png")
        #plt.show()
    #Called to close the current window when transitioning to a new window    
    def close_windows(self):
        self.self.currentWindow.destroy()
    # Captures the event of a user hitting the red 'X' button to close a window
    def on_closing(self):
        self.currentWindow.destroy
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            #This will kill the entire application
            root.destroy()

# This function is called to load model data that will be used to 
# create a new plot
def loadModel(selection):
    #Get the name of the selected model
    selected_model = "config_"+selection
    #query will now hold all data for the selected model
    query = config_file.user_config[selected_model]

    #get params
    design_params = query["design_params"]
    devsim_params = query["devsim_params"]
    optimizer_params = query["optimizer_params"]
    #2d array to hold all types of params
    allParams = [design_params, devsim_params, optimizer_params]

    #start parsing the model equation and filling in actual values for the params
    modelEq = query["Model"]
    #Replace all design parameter variables with their associated values
    for index in design_params:
        modelEq = modelEq.replace(index, str(query[index]))

    #Replace all devsim parameter variables with their associated values
    if len(devsim_params) > 0:
        for index,val in enumerate(devsim_params):
            #If the values do not exist than retrieve them
            if query[devsim_params[index]][1] == "":
                get_devsim_values(selected_model)
                query = config_file.user_config[selected_model]
    for index in devsim_params:
        modelEq = modelEq.replace(index, str(query[index][1]))

    #Replace all optimizer parameter variables with their associated values
    if len(optimizer_params) > 0:
        #If the values do not exist than retrieve them
        if query[optimizer_params[0]] == "":
            get_optimizer_values(selected_model)
            query = config_file.user_config[selected_model]
    for index in optimizer_params:
        modelEq = modelEq.replace(index, str(query[index]))

    #generate data points
    opt_x_data = query["opt_x_data"]
    x_axis = query["x_axis"]
    Y_dataPoints = []
    for dataPoint in opt_x_data:
        currentEq = modelEq.replace(x_axis, str(dataPoint))
        Y_dataPoints.append(eval(currentEq))

    #Call the MainPage 
    MainPage(opt_x_data, Y_dataPoints, selection, allParams)
#end of loadModel

def main():
    app = IntroPage()
    root.mainloop()

if __name__ == '__main__':
    main()

    
