## this script will show you how to use the Band fit function
import numpy as np
from read_param import read_param
from fit_lc import NE_band, before_fit, Band_fit
from scipy import interpolate

file_param = 'parameters.txt'
data = np.loadtxt('energy_list_plot/GRM_rsp_rate_bin.txt')
ebounds = np.loadtxt('matrix_data/ebounds_GRM.txt')
energy = np.loadtxt('matrix_data/energy_GRM.txt')
matrix = np.loadtxt('matrix_data/matrix_GRM.txt')

parameters = read_param(file_param)
gen1, gen2, gen_dt = parameters['energy_gen']
time1, time2, time_dt = parameters['time']
time_bin = parameters['time_bin'] ; time_timebin = np.arange(time1, time2, time_bin)
energy_list = parameters['energy_list_GRM']
cleaned = energy_list.strip('[]').split()
energy_list = [int(x) for x in cleaned]

e_min , e_max = ebounds[:,0] , ebounds[:,1]
energy_centers = (energy[:,0] + energy[:,1]) / 2

data_, e_centers = before_fit(data, matrix, energy_centers, e_min, e_max, gen1, gen2)
bounds = ([0, -3, -5, 10], [1e6, 0, -1, 16000])
p0 = [10, -1, -2, 4000]
n_time = len(time_timebin)
A = np.zeros(n_time) ; alpha = np.zeros(n_time) ; beta = np.zeros(n_time) ; Ep = np.zeros(n_time)
perr = np.zeros((n_time, 4))
for i in range(len(time_timebin)):
    A[i], alpha[i], beta[i], Ep[i], perr[i,:] = Band_fit(e_centers, data_[:,i], p0, bounds)
    
results = np.column_stack((A, alpha, beta, Ep))
np.savetxt('Band_fit/GRM/results.txt', results, header='A  alpha  beta  Ep', delimiter='\t')
np.savetxt('Band_fit/GRM/standard_deviation.txt', perr, header='A  alpha  beta  Ep', delimiter='\t')

