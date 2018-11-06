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

# Create a root window that will be hidden. Will act as a driver to all other windows.
root = tk.Tk()
root.withdraw()

# This class represents the introduction page that first appears when the application is launched
class IntroPage:
    def __init__(self):
        #Create the current window
        self.currentWindow = tk.Toplevel(root)
        self.currentWindow.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.currentWindow.title("IntroPage")
        self.currentWindow.geometry("500x300+400+0")

        #LABEL: SmartSim title 
        title = tk.Label(self.currentWindow, text="SmartSim")
        title.grid(column=0, row=0)
        title.place(relx=.5, rely=.07, anchor="center")
        title.config(font=("Courier", 24))

        #LABEL: Welcome message
        welcomeLbl = tk.Label(self.currentWindow, text="Welcome to the SmartSim development tool.")
        welcomeLbl.place(relx=.5, rely=.2, anchor="center")
        welcomeLbl.config(font=("Courier", 14))

        #LABEL: Select metric
        metricLbl = tk.Label(self.currentWindow, text="Select Metric")
        metricLbl.place(relx=.5, rely=.35, anchor="center")
        metricLbl.config(font=("Courier", 12))

        #Create a List that will be used to fill the comboBox
        model_list = []
        for metric in config_file.user_config:
            model_list.append(config_file.user_config[metric]["Metric"])

        #COMBOBOX: Select Model to Load
        selected_model = tk.StringVar() 
        model_combo = ttk.Combobox(self.currentWindow, textvariable=selected_model)
        model_combo['values'] = model_list
        model_combo.current(0)
        model_combo.place(relx=.5, rely=.45, anchor="center")
        
        #Called when the user makes a selection within the combobox
        def callback(eventObject):
            self.Open(selected_model.get())
        # This binds the event that occurs when a user makes a selection 
        # within the combobox to the callback function above.
        model_combo.bind("<<ComboboxSelected>>", callback)
    
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
###### End of the IntroPage Class ######

# This function is called to load model data that will be used to create a new plot
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
        
    #Call the MainPage 
    MainPage(query, selection, allParams, all_param_values)
###### END OF LOADMODEL CLASS ######

### This class represents the main page of the GUI which contains the graph
class MainPage:
    def __init__(self, query, metricName, allParams, all_param_values):
        self.allParams = allParams
        self.all_param_values = all_param_values
        self.metricName = metricName
        self.query = query
        self.labels = []
        
        #Create the current window
        self.currentWindow = tk.Toplevel(root)
        self.currentWindow.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.currentWindow.title("MainPage")
        self.currentWindow.geometry("1080x680+200+0")

        #LABEL: SmartSim title 
        title = tk.Label(self.currentWindow, text="SmartSim")
        title.place(relx=.5, rely=.05, anchor="center")
        title.config(font=("Courier", 24))

        #LABEL: Other options
        otherLbl = tk.Label(self.currentWindow, text="Other Options")
        otherLbl.place(relx=.02, rely=.1)
        otherLbl.config(font=("Courier", 12))

        #BUTTON: Overlay Button
        overlayBtn = tk.Button(self.currentWindow, text="Overlay Simulated Data", bg="deep sky blue")
        overlayBtn.place(relx=.02, rely=.14)

        #BUTTON: Redo-Config Button
        configBtn = tk.Button(self.currentWindow, text="Redo-Config", command=lambda: self.RedoConfig(self.metricName), bg="deep sky blue")
        configBtn.place(relx=.195, rely=.14)
        
        #LABEL: Select new metric 
        metricLbl = tk.Label(self.currentWindow, text="Select New Metric")
        metricLbl.place(relx=.02, rely=.2)
        metricLbl.config(font=("Courier", 12))

        #LABEL: Edit Parameter 
        editLbl = tk.Label(self.currentWindow, text="Edit Parameter")
        editLbl.place(relx=.2, rely=.2)
        editLbl.config(font=("Courier", 12))
        
        #LABEL: Parameters
        paramLbl = tk.Label(self.currentWindow, text="Parameters")
        paramLbl.place(relx=.02, rely=.32)
        paramLbl.config(font=("Courier", 12))
        
        #Create a List that will be used to populate the combobox
        model_list = []

        ### COMBOBOX for Select Metric ###
        #Load all models that are currently stored in the configuration file
        for model in config_file.user_config:
            model_list.append(config_file.user_config[model]["Metric"])
        
        #Sting to store the comboBox selection
        selected_model = tk.StringVar() 
        #COMBOBOX: Select Model to Load
        model_combo = ttk.Combobox(self.currentWindow, textvariable=selected_model)
        model_combo['values'] = model_list
        model_combo.current(0)
        model_combo.place(relx=.02, rely=.24)
        
        #Called when the user makes a selection within the combobox
        def callback(eventObject):
            self.Close(selected_model.get())
        model_combo.bind("<<ComboboxSelected>>", callback)

        ### COMBOBOX for Edit ###
        #Sting to store the comboBox selection
        selected_parameter = tk.StringVar() 
        self.editCombo = ttk.Combobox(self.currentWindow, textvariable=selected_parameter)
        self.editCombo['values'] = self.allParams
        self.editCombo.current(0)
        self.editCombo.grid(column=0, row=1)
        self.editCombo.place(relx=.2, rely=.24)
        
        #Called when the user makes a selection within the combobox
        def editCallback(eventObject):
            self.Edit(selected_parameter.get(), self.editCombo.current(), 1)
        self.editCombo.bind("<<ComboboxSelected>>", editCallback)

        #Call the function that displays all te parameters
        #self.Display_Parameters(self.allParams, self.all_param_values)
        self.Display_Parameters(0)    

        #Call the function that draws the graph
        self.DrawGraph(0)
        self.Edit(allParams[0], 0, 0)

    #This function is called to display all parameters. 
    #def Display_Parameters(self, allParams, all_param_values):
    def Display_Parameters(self, flag):
        # If this is not the first time the function is called than labels for the parameters already exist.
        # Delete them. TODO: or overwrite?
        if(flag == 1):
            for index in range(len(self.allParams)):
                currentLbl =self.labels[index]
                currentLbl.destroy()
            self.labels.clear()
        ##### Design Parameters #####
        column = 0
        row = 0
        for index in range(len(self.allParams)):
            #LABEL: label for the current param
            floatValue = float(self.all_param_values[index])
            floatValue = round(floatValue, 2)
            Lbl = tk.Label(self.currentWindow, text=self.allParams[index]+": "+str(floatValue))
            Lbl.place(relx=.02+(column*.1), rely=.36+(row*.025))
            Lbl.config(font=("Courier", 9))
            self.labels.append(Lbl) 
            row = row + 1
            if row == 15:
                row = 0
                column = column + 1
                
        #LABEL: Current Parameter 
        if(flag == 1):
            self.currentLbl.destroy()
        self.currentLbl = tk.Label(self.currentWindow, text="Current Parameter: "+ str(self.allParams[self.editCombo.current()]) + ", Current Value = " + str(self.all_param_values[self.editCombo.current()]))
        self.currentLbl.place(relx=.21, rely=.975, anchor="center")
        self.currentLbl.config(font=("Courier", 10))

    # This function is responsible for creating the smaller window that lets 
    # you edit parameters
    def Edit(self, selection, index, flag):
        if (flag == 1):
            # If this is not the first time the function is called than widgets already exist.
            # Delete them.
            self.manualLbl.destroy()
            self.value.destroy()
            self.updateBtn.destroy()
            self.minLbl.destroy()
            self.minimum.destroy()
            self.maxLbl.destroy()
            self.maximum.destroy()
            self.resLbl.destroy()
            self.resolution.destroy()
            self.slider.destroy()

        # Called to update the label below the slider representing the parameter currently 
        # being edited. kinda overkill TODO: maybe change this so all parameter labels are 
        # not re-written when only one needs to change
        self.Display_Parameters(1)
        #LABEL: Manual Label 
        self.manualLbl = tk.Label(self.currentWindow, text="Enter Value:")
        self.manualLbl.place(relx=.0175, rely=.825)
        self.manualLbl.config(font=("Courier", 10))
        
        #ENTRY: Value Textbox
        self.manualText = tk.StringVar()
        self.value = tk.Entry(self.currentWindow, textvariable=self.manualText, width=8)
        self.value.place(relx=0.11, rely=.823)
        
        def ManualEntry(eventObject):
            self.all_param_values[index] = float(self.manualText.get())
            config_file.user_config["config_"+self.metricName][self.allParams[index]] = self.all_param_values[index]
            self.Display_Parameters(1)
            self.DrawGraph(1)
        self.value.bind('<Return>', ManualEntry)
        
        #BUTTON: Update Button
        self.updateBtn = tk.Button(self.currentWindow, text="Update Slider", command=lambda: UpdateSlider(self.minText, self.maxText, self.resText), bg="deep sky blue", height=1, width=11, font=("Courier", 10))
        self.updateBtn.place(relx=.245, rely=.81)

        #LABEL: Min Label 
        self.minLbl = tk.Label(self.currentWindow, text="Min:")
        self.minLbl.place(relx=.0175, rely=.86)
        self.minLbl.config(font=("Courier", 10))

        #ENTRY: Min Textbox
        self.minText = tk.StringVar()
        self.minimum = tk.Entry(self.currentWindow, textvariable=self.minText, width=8)
        self.minimum.delete(0, 1)
        self.minimum.insert(0,-15.0)
        self.minimum.place(relx=0.05, rely=0.86)

        #LABEL: Max Label 
        self.maxLbl = tk.Label(self.currentWindow, text="Max:")
        self.maxLbl.place(relx=.125, rely=.86)
        self.maxLbl.config(font=("Courier", 10))

        #TEXTBOX: Max Textbox
        self.maxText = tk.StringVar()
        self.maximum = tk.Entry(self.currentWindow, textvariable=self.maxText, width=8)
        self.maximum.delete(0, 1)
        self.maximum.insert(0,15.0)
        self.maximum.place(relx=0.1575, rely=0.86)
        
        #LABEL: Resolution Label 
        self.resLbl = tk.Label(self.currentWindow, text="Resolution:")
        self.resLbl.place(relx=.2325, rely=.86)
        self.resLbl.config(font=("Courier", 10))

        #TEXTBOX: Resolution Textbox
        self.resText = tk.StringVar()
        self.resolution = tk.Entry(self.currentWindow, textvariable=self.resText, width=8)
        self.resolution.delete(0,1)
        self.resolution.insert(0,0.05)
        self.resolution.place(relx=0.32, rely=0.86)

        #Slider
        def getSliderValue(value):
            self.all_param_values[index] = float(value)
            config_file.user_config["config_"+self.metricName][self.allParams[index]] = self.all_param_values[index]
            self.Display_Parameters(1)
            self.DrawGraph(1)
            
        self.slider = tk.Scale(self.currentWindow, from_=-15.0, to=15.0, orient="horizontal", length=450, digits=4, resolution=0.05, command=getSliderValue)
        self.slider.place(relx=.21, rely=.92, anchor="center")
        
        def UpdateSlider(minimun, maximun, resolution):
            self.slider.destroy()
            self.slider = tk.Scale(self.currentWindow, from_=float(minimun.get()), to=float(maximun.get()), resolution=float(resolution.get()), digits=4, orient="horizontal", length=450, command=getSliderValue)
            self.slider.place(relx=.21, rely=.92, anchor="center")
            

    #This function is responsible for drawing the graph
    def DrawGraph(self, flag):
        modelEq = self.query["Model"]
        #generate data points
        opt_x_data = self.query["opt_x_data"]
        x_axis = self.query["x_axis"]
        Y_dataPoints = []
        counter = 0
        for index in self.allParams:
            modelEq = modelEq.replace(index, str(self.all_param_values[counter]))
            counter = counter + 1
        #generate values for y using default data.
        for dataPoint in opt_x_data:
            currentEq = modelEq.replace(x_axis, str(dataPoint))
            Y_dataPoints.append(eval(currentEq))
            
        if (flag == 0):
            #INIT Graph
            fig = Figure(figsize=(6,6), dpi=100)
            self.plot = fig.add_subplot(111)
            self.plot.plot(opt_x_data, Y_dataPoints, color='blue')
            self.plot.set_title ("Estimation Grid", fontsize=14)
            self.plot.set_ylabel("Y", fontsize=14)
            self.plot.grid(True)
            self.plot.set_xlabel("X", fontsize=14)
            self.canvas = FigureCanvasTkAgg(fig, master=self.currentWindow)
            self.canvas.get_tk_widget().place(relx=0.43, rely=0.1)
            self.canvas.draw()
        else: #TODO: lower the axis bounds if needed
            self.plot.lines.pop(0)
            self.plot.plot(opt_x_data, Y_dataPoints, color='blue')  
            self.canvas.draw()

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

def main():
    app = IntroPage()
    root.mainloop()

if __name__ == '__main__':
    main()

    
