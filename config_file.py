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
config_Ids = {
	'Metric' : 'Ids',
	'Model' : '(u*C_ox*W * (Vgs-Vt)**2) / (2*L)',
	'x_axis' : 'Vgs',
	'design_params' : ['W', 'L'],
	'devsim_params' : ['C_ox', 'Vt'],
	'optimizer_params' : ['u'],
	'u' : 1.0,
	'W' : 1,
	'L' : 0.5,
	'C_ox' : ['devsim input line', ''],
	'Vt' : ['devsim input line', 4.5],
	'opt_x_data' : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
	'opt_y_data' : [5, 4.5, 4, 3.5, 3, 2.5, 2, 1.5, 1, 0.5, 0],
}
user_config = {'config_y' : config_y,'config_Ids' : config_Ids,}
