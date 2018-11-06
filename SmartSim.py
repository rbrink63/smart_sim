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

# This class represents the introduction page that first appears when
# the application is launched
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

### This class represents the main page of the GUI which contains the graph
class MainPage:

    def __init__(self, X_dataPoints, Y_dataPoints, metricName, allParams, all_param_values):
        
        self.allParams = allParams
        self.all_param_values = all_param_values

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
        configBtn = tk.Button(self.currentWindow, text="Redo-Config", command=lambda: self.RedoConfig(metricName), bg="deep sky blue")
        configBtn.place(relx=.195, rely=.14)
        
        #LABEL: Select new metric 
        metricLbl = tk.Label(self.currentWindow, text="Select New Metric")
        metricLbl.place(relx=.02, rely=.2)
        metricLbl.config(font=("Courier", 12))

        #LABEL: Edit Parameter 
        editLbl = tk.Label(self.currentWindow, text="Edit Parameter")
        editLbl.place(relx=.2, rely=.2)
        editLbl.config(font=("Courier", 12))
        
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
        editCombo = ttk.Combobox(self.currentWindow, textvariable=selected_parameter)
        editCombo['values'] = self.allParams
        editCombo.current(0)
        editCombo.grid(column=0, row=1)
        editCombo.place(relx=.2, rely=.24)
        
        #Called when the user makes a selection within the combobox
        def editCallback(eventObject):
            self.Edit(selected_parameter.get(), editCombo.current())
        editCombo.bind("<<ComboboxSelected>>", editCallback)

        #Call the function that displays all te parameters
        #self.Display_Parameters(self.allParams, self.all_param_values)
        self.Display_Parameters()    

        #Call the function that draws the graph
        self.DrawGraph(X_dataPoints, Y_dataPoints)

    #This function is called to display all parameters. 
    #def Display_Parameters(self, allParams, all_param_values):
    def Display_Parameters(self):
        #LABEL: Parameters
        paramLbl = tk.Label(self.currentWindow, text="Parameters")
        paramLbl.place(relx=.02, rely=.32)
        paramLbl.config(font=("Courier", 12))

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
            row = row + 1
            if row == 15:
                row = 0
                column = column + 1

    # This function is responsible for creating the smaller window that lets 
    # you edit parameters
    def Edit(self, selection, index):
        #Create the current window
        self.editWindow = tk.Toplevel(root)
        self.editWindow.title("EditPage")
        self.editWindow.geometry("600x200+65+500")
        
        #LABEL: Update Slider Label 
        updateLbl = tk.Label(self.editWindow, text="Select a min and max value for the slider.")
        updateLbl.place(relx=.025, rely=.03)
        updateLbl.config(font=("Courier", 10))

         #BUTTON: Update Button
        updateBtn = tk.Button(self.editWindow, text="Update Slider", command=lambda: UpdateSlider(minText, maxText), bg="deep sky blue")
        updateBtn.place(relx=.025, rely=.3)

        #LABEL: Min Label 
        minLbl = tk.Label(self.editWindow, text="Min:")
        minLbl.place(relx=.025, rely=.15)
        minLbl.config(font=("Courier", 10))

        #Min Textbox
        minText = tk.IntVar()
        minimum = tk.Entry(self.editWindow, textvariable=minText, width=10)
        minimum.insert(0,0)
        minimum.place(relx=0.09, rely=0.15)

        #LABEL: Max Label 
        maxLbl = tk.Label(self.editWindow, text="Max:")
        maxLbl.place(relx=.25, rely=.15)
        maxLbl.config(font=("Courier", 10))

        #TEXTBOX: Max Textbox
        maxText = tk.IntVar()
        maximum = tk.Entry(self.editWindow, textvariable=maxText, width=10)
        maximum.insert(0,100)
        maximum.place(relx=0.315, rely=0.15)

        #LABEL: Current Parameter 
        maxLbl = tk.Label(self.editWindow, text="Current Parameter: "+ selection + ", Current Value = " + self.all_param_values[index])
        maxLbl.place(relx=.5, rely=.85, anchor="center")
        maxLbl.config(font=("Courier", 10))

        #Slider TODO:command=self.updateModel()
        self.slider = tk.Scale(self.editWindow, from_=0, to=100, orient="horizontal", length=480)
        self.slider.place(relx=.5, rely=.65, anchor="center")
        
        def UpdateSlider(minimun, maximun):
            self.slider.destroy()
            self.slider = tk.Scale(self.editWindow, from_=minimun.get(), to=maximum.get(), orient="horizontal", length=480)
            self.slider.place(relx=.5, rely=.65, anchor="center")

    #This function is responsible for drawing the graph
    def DrawGraph(self, X_dataPoints, Y_dataPoints):
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

    
