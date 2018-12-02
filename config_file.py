config_y = {
	'Metric' : 'y',
	'Model' : 'm*x + c/b',
	'x_axis' : 'x',
	'design_params' : ['m'],
	'devsim_params' : [],
	'optimizer_params' : ['b', 'c'],
	'm' : 0.6,
	'b' : 0.9930198013210478,
	'c' : 1.886764068047961,
	'opt_x_data' : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
	'opt_y_data' : [5, 4.5, 4, 3.5, 3, 2.5, 2, 1.5, 1, 0.5, 0],
	'models_path' : '/tools/stabflow/mainline-s8/s8/t/s8/s8p-10r/models',
	'corners' : 'tt.cor',
	'secondary_corners' : 'ttcell.cor,trtc.cor',
	'headers' : ['Paramname', 'Model', 'N/P', 'Type', 'Sweeps', 'Graph', 'W', 'L', 'M', 'Temperature', 'Vd', 'Vg', 'Vs', 'Vb', 'Simulator', 'MF', 'NF', 'Vcc', 'Vdlin', 'CC'],
}
config_Ids = {
	'Metric' : 'Ids',
	'Model' : '(u*C_ox*W * (Vgs-Vt)**2) / (2*L)',
	'x_axis' : 'Vgs',
	'design_params' : ['W', 'L'],
	'devsim_params' : ['C_ox', 'Vt'],
	'optimizer_params' : ['u'],
	'u' : -1.12,
	'W' : 0.9,
	'L' : 1.95,
	'C_ox' : 13.01,
	'Vt' : 10.52,
	'opt_x_data' : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
	'opt_y_data' : [5, 4.5, 4, 3.5, 3, 2.5, 2, 1.5, 1, 0.5, 0],
	'models_path' : '/tools/stabflow/mainline-s8/s8/t/s8/s8p-10r/models',
	'corners' : 'tt.cor',
	'secondary_corners' : 'ttcell.cor,trtc.cor',
	'headers' : ['Paramname', 'Model', 'N/P', 'Type', 'Sweeps', 'Graph', 'W', 'L', 'M', 'Temperature', 'Vd', 'Vg', 'Vs', 'Vb', 'Simulator', 'MF', 'NF', 'Vcc', 'Vdlin', 'CC'],
}
config_z = {
	'Metric' : 'z',
	'Model' : 'm*a*d*x + c/b',
	'x_axis' : 'x',
	'design_params' : ['m', 'a', 'd', 'h', 'i'],
	'devsim_params' : ['e', 'f', 'g'],
	'optimizer_params' : ['b', 'c'],
	'm' : 3.11,
	'a' : 3.1,
	'd' : 1,
	'h' : 1,
	'i' : 1,
	'b' : 7.326565173857639,
	'c' : -334.8606552381626,
	'e' : [['1', 'nhv', 'nmos', 'id', '', '', '7', '0.5', '1', '30', '0.1', '5', '', '0', 'eldo', '1', '1', '5', '0.1', '1.00E-08'], 0.0004221],
	'f' : [['1', 'nhv', 'nmos', 'id', '', '', '7', '0.5', '1', '30', '0.1', '5', '', '0', 'eldo', '1', '1', '5', '0.1', '1.00E-08'], 0.0004221],
	'g' : [['1', 'nhv', 'nmos', 'id', '', '', '7', '0.5', '1', '30', '0.1', '5', '', '0', 'eldo', '1', '1', '5', '0.1', '1.00E-08'], 0.0004221],
	'opt_x_data' : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
	'opt_y_data' : [5, 4.5, 4, 3.5, 3, 2.5, 2, 1.5, 1, 0.5, 0],
	'models_path' : '/tools/stabflow/mainline-s8/s8/t/s8/s8p-10r/models',
	'corners' : 'tt.cor',
	'secondary_corners' : 'ttcell.cor,trtc.cor',
	'headers' : ['Paramname', 'Model', 'N/P', 'Type', 'Sweeps', 'Graph', 'W', 'L', 'M', 'Temperature', 'Vd', 'Vg', 'Vs', 'Vb', 'Simulator', 'MF', 'NF', 'Vcc', 'Vdlin', 'CC'],
}
user_config = {'config_y' : config_y,'config_Ids' : config_Ids,'config_z' : config_z,}