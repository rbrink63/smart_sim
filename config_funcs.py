import config_file
import scipy_curve_fit
import sys

def get_optimizer_values(metric):
    
    #run optimizer
    #the main function will call update file to overwrite config_data.py to store the values
    
    #UG is going to write code to dynamically change the func argument for curve fit
    #this will need to happen before we call do_opt()
    # for now we will just use y=mx+b as an example

    # format arguments and model
    args = config_file.user_config[metric]['x_axis'] + "," + \
            ",".join(config_file.user_config[metric]['optimizer_params'])
    mdl = config_file.user_config[metric]['Model']
    
    # insert numbers to equation
    for design_params in config_file.user_config[metric]['design_params']:
        mdl = mdl.replace(design_params, str(config_file.user_config[metric][design_params]))
    for devsim_params in config_file.user_config[metric]['devsim_params']:
        mdl = mdl.replace(devsim_params, str(config_file.user_config[metric][devsim_params]))
    
    # retrieve optimized constants
    new_opts = scipy_curve_fit.do_optimization(mdl, args, config_file.user_config[metric]['opt_x_data'], config_file.user_config[metric]['opt_y_data'])
   
    #loop through optimizer params and save new vals
    #config_file won't actually be updated until main() overwrites it

    for idx, param in enumerate(config_file.user_config[metric]['optimizer_params']):
        config_file.user_config[metric][param] = new_opts[idx]


def get_devsim_values(metric, devsim_dummy):
#find all devsim commands in the metric entry of the config file
    for param in config_file.user_config[metric]['devsim_params']:
        #run devsim
        #fake it for now
        #this updates the local copy of config_data we imported
        #the main function will overwrite config_data.py to store the values
        config_file.user_config[metric][param][1] = devsim_dummy



def update_config_file():
    #store the results in the config file
    with open('config_file.py', 'w') as f:
       f.seek(0) #go to beginning of file 
       for metric in config_file.user_config:
           f.write(f'{metric} = ' + '{\n')
           for key, value in config_file.user_config[metric].items():
               if isinstance(value, str):
                   f.write(f'\t\'{key}\' : \'{value}\',\n')
               else: 
                   f.write(f'\t\'{key}\' : {value},\n')
           f.write('}\n')
    
       f.write('user_config = {')
       for metric in config_file.user_config:
           f.write(f'\'{metric}\' : {metric},')
       f.write('}')

def save_design_value(metric, param, new_value):
    config_file.user_config[metric][param] = new_value


def main():
    #usage python3 execName config_<metric name>
    
    if len(sys.argv) != 2:
        print('use one and only one command line argument')
        sys.exit()
    if sys.argv[1] not in config_file.user_config:
        print('metric not found in config file')
        sys.exit()

    config_metric = sys.argv[1] 
    #print (config_metric)
    #get_devsim_values(config_metric, 11)
    get_optimizer_values(config_metric)
#    save_design_value(config_metric, 'c', 5)
    update_config_file()
        
main()
