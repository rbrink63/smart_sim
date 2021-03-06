#this is a Python module but it is really used as a database
#it gets imported in to SmartSim.py when a user launches SmartSim
#changes to the values during runtime are saved only to the runtime environment
#so we call config_funcs.update_config_file() as needed to overwite this file
#to make the changes persistent between SmartSim runs

config_y = {
	'Metric' : 'y',
	'Model' : 'm*x + c/b',
	'x_axis' : 'x',
	'design_params' : ['m'],
	'devsim_params' : [],
	'optimizer_params' : ['b', 'c'],
	'm' : -0.5,
	'b' : 0.9999999999961197,
	'c' : 4.999999999980599,
	'opt_x_data' : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
	'opt_y_data' : [5, 4.5, 4, 3.5, 3, 2.5, 2, 1.5, 1, 0.5, 0],
}
config_x = {
	'Metric' : 'x',
	'Model' : 'm*a*d*x + c/b',
	'x_axis' : 'x',
	'design_params' : ['m', 'a', 'd', 'h', 'i'],
	'devsim_params' : ['e', 'f', 'g'],
	'optimizer_params' : ['b', 'c', 'z'],
	'm' : -0.5,
	'a' : 1,
	'd' : 1,
	'h' : 1,
	'i' : 1,
	'b' : 0.9999999999961197,
	'c' : 4.999999999980599,
	'z' : 4.999999999980599,
	'e' : ['devsim input line', 11],
	'f' : ['devsim input line', 11],
	'g' : ['devsim input line', 11],
	'opt_x_data' : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
	'opt_y_data' : [5, 4.5, 4, 3.5, 3, 2.5, 2, 1.5, 1, 0.5, 0],
}
config_Ids = {
	'Metric' : 'Ids',
	'Model' : '(u*C_ox*W * (Vgs-Vt)**2) / (2*L)',
	'x_axis' : 'Vgs',
	'design_params' : ['W', 'L'],
	'devsim_params' : ['C_ox', 'Vt'],
	'optimizer_params' : ['u'],
	'u' : 0.004377845600063896,
	'W' : 1,
	'L' : 0.5,
	'C_ox' : ['devsim input line', 11],
	'Vt' : ['devsim input line', 11],
	'opt_x_data' : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
	'opt_y_data' : [5, 4.5, 4, 3.5, 3, 2.5, 2, 1.5, 1, 0.5, 0],
}
user_config = {'config_y' : config_y,'config_Ids' : config_Ids,'config_x' : config_x}
