import sys
import csv
import numpy as np
from scipy.optimize import curve_fit

def do_optimization(model, args, csv_file):
   
    func = eval("lambda {}:{}".format(args,model))

    res = []
    with open(csv_file, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        x = []
        y = []
        for idx, row in enumerate(reader):
            if idx == 0:
                continue
            else:
                x.append(float(row[0]))
                y.append(float(row[1]))
        res.append(x)
        res.append(y)

    xdata = np.array(res[0])
    ydata = np.array(res[1])
    popt, pcov = curve_fit(func, xdata, ydata)

    return popt
