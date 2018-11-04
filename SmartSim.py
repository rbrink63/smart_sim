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
        self.currentWindow.geometry("600x300+300+0")
        self.currentWindow.geometry('{}x{}'.format(700, 500))
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
    design_buttons = []
    def __init__(self, X_dataPoints, Y_dataPoints, metricName, allParams, all_param_values):
        self.design_buttons.clear()
        #Create the current window
        self.currentWindow = tk.Toplevel(root)
        self.currentWindow.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.currentWindow.title("MainPage")
        self.currentWindow.geometry("1080x680+200+0")
        #LABEL: SmartSim title 
        self.title = tk.Label(self.currentWindow, text="SmartSim")
        self.title.place(relx=.5, rely=.05, anchor="center")
        self.title.config(font=("Courier", 24))
        #LABEL: Other options
        self.otherLbl = tk.Label(self.currentWindow, text="Other Options")
        self.otherLbl.place(relx=.02, rely=.1)
        self.otherLbl.config(font=("Courier", 12))
        #BUTTON: Overlay Button
        self.overlayBtn = tk.Button(self.currentWindow, text="Overlay Simulated Data", bg="deep sky blue")
        self.overlayBtn.place(relx=.02, rely=.14)
        #BUTTON: Redo-Config Button
        self.configBtn = tk.Button(self.currentWindow, text="Redo-Config", command=lambda: self.RedoConfig(metricName), bg="deep sky blue")
        self.configBtn.place(relx=.195, rely=.14)
        #BUTTON: Submit Button
        self.SubmitBtn = tk.Button(self.currentWindow, text="Submit", command=lambda: self.Submit(metricName,self.design_buttons), bg="deep sky blue")
        self.SubmitBtn.place(relx=.3, rely=.14)
        #LABEL: Select new metric 
        self.metricLbl = tk.Label(self.currentWindow, text="Select New Metric")
        self.metricLbl.place(relx=.02, rely=.2)
        self.metricLbl.config(font=("Courier", 12))
        #LABEL: Edit Parameter 
        self.editLbl = tk.Label(self.currentWindow, text="Edit Parameter")
        self.editLbl.place(relx=.2, rely=.2)
        self.editLbl.config(font=("Courier", 12))
        
        #Create a List that will be used to populate the combobox
        self.my_list = []

        ### COMBOBOX for Select Metric ###
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
        self.combo.place(relx=.02, rely=.24)
        
        #Called when the user makes a selection within the combobox
        def callback(eventObject):
            self.Close(self.text.get())
        self.combo.bind("<<ComboboxSelected>>", callback)

        ### COMBOBOX for Edit ###
        #Sting to store the comboBox selection
        self.text2 = tk.StringVar() 
        self.editCombo = ttk.Combobox(self.currentWindow, textvariable=self.text2)
        self.editCombo['values'] = allParams
        self.editCombo.current(1)
        self.editCombo.grid(column=0, row=1)
        self.editCombo.place(relx=.2, rely=.24)
        
        #Called when the user makes a selection within the combobox
        def editCallback(eventObject):
            self.Edit(self.text.get())
        self.editCombo.bind("<<ComboboxSelected>>", editCallback)

        #LABEL: Parameters
        self.paramLbl = tk.Label(self.currentWindow, text="Parameters")
        self.paramLbl.place(relx=.02, rely=.32)
        self.paramLbl.config(font=("Courier", 12))

		##### Design Parameters #####
        column = 0
        row = 0
        for index in range(len(allParams)):
            #LABEL: label for the current param
            floatValue = float(all_param_values[index])
            floatValue = round(floatValue, 2)
            self.Lbl = tk.Label(self.currentWindow, text=allParams[index]+": "+str(floatValue))
            self.Lbl.place(relx=.02+(column*.1), rely=.36+(row*.025))
            self.Lbl.config(font=("Courier", 9)) 
            row = row + 1
            if row == 15:
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
        canvas.get_tk_widget().place(relx=0.43, rely=0.1)
        canvas.draw()
        #GRAPH
        #plt.plot(X_dataPoints, Y_dataPoints)
        #plt.xlabel('X_Axis_Title')
        #plt.ylabel('Y_Axis_Title')
        #plt.title("Metric: "+metricName)
        #plt.grid(True)
        #plt.savefig(metricName+".png")
        #plt.show()

    def Submit(self, selection, design_buttons):
        for index in design_buttons:
            config_file.user_config["config_"+selection][index[0]]= index[1].get()
        self.currentWindow.destroy()
        loadModel(selection)
	#Called to update the paramaters from the configuration file
    def RedoConfig(self, selection):
        get_devsim_values("config_"+selection)
        get_optimizer_values("config_"+selection)
        self.currentWindow.destroy()
        loadModel(selection)
    #Called to close the current window when transitioning to a new window    
    def Close(self, selection):
        self.currentWindow.destroy()
        loadModel(selection)
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
    all_param_values = []
    allParams = []
    #query will now hold all data for the selected model
    query = config_file.user_config[selected_model]
    #get params
    design_params = query["design_params"]
    devsim_params = query["devsim_params"]
    optimizer_params = query["optimizer_params"]
    #Get the model EQ
    modelEq = query["Model"]

    #2d array to hold all types of params
    for index in range(len(design_params)):
        allParams.append(design_params[index])
    for index in range(len(devsim_params)):
        allParams.append(devsim_params[index])
    for index in range(len(optimizer_params)):
        allParams.append(optimizer_params[index])

    #start parsing the model equation and filling in actual values for the params. Replace all design parameter variables with their associated values
    for index in design_params:
        all_param_values.append(str(query[index]))
        modelEq = modelEq.replace(index, str(query[index]))

    #Replace all devsim parameter variables with their associated values
    if len(devsim_params) > 0:
        for index,val in enumerate(devsim_params):
            #If the values do not exist than retrieve them
            if query[devsim_params[index]][1] == "":
                get_devsim_values(selected_model)
                query = config_file.user_config[selected_model]
    for index in devsim_params:
        all_param_values.append(str(query[index][1]))
        modelEq = modelEq.replace(index, str(query[index][1]))

    #Replace all optimizer parameter variables with their associated values
    if len(optimizer_params) > 0:
        #If the values do not exist than retrieve them
        if query[optimizer_params[0]] == "":
            get_optimizer_values(selected_model)
            query = config_file.user_config[selected_model]
    for index in optimizer_params:
        all_param_values.append(str(query[index]))
        modelEq = modelEq.replace(index, str(query[index]))

    #generate data points
    opt_x_data = query["opt_x_data"]
    x_axis = query["x_axis"]
    Y_dataPoints = []
    for dataPoint in opt_x_data:
        currentEq = modelEq.replace(x_axis, str(dataPoint))
        Y_dataPoints.append(eval(currentEq))

    #Call the MainPage 
    MainPage(opt_x_data, Y_dataPoints, selection, allParams, all_param_values)
#end of loadModel

def main():
    app = IntroPage()
    root.mainloop()

if __name__ == '__main__':
    main()

    
