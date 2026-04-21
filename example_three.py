## in this script, we will show you how to use filter and fit functions
##  only light curve shape fit, not the spectral fit.
import numpy as np
from read_param import read_param
from fit_lc import fred, fred_fit
from filter_lc import moving_avg_smooth, wavelet_smooth,  savgol_filter

## read parameters from 'parameters.txt'
file_param = 'parameters.txt'
parameters = read_param(file_param)
time1, time2, time_dt = parameters['time']
time_bin = parameters['time_bin']
gen1, gen2, gen_dt = parameters['energy_gen']
energy_list_GRM = parameters['energy_list_GRM'] ## 'energy_list' parameters are a little special, you can use the same process to make sure the formats are compatible.
fluence_target = parameters['fluence_target']
energy_target = parameters['energy_target']
time_target = parameters['time_target']
print('read parameters finish')

## basic data process
time = np.arange(time1, time2, time_dt)
time_timebin = np.arange(time1, time2, time_bin)
energy_gen = np.arange(gen1, gen2, gen_dt)
gen_centers = (energy_gen[1:] + energy_gen[:-1]) / 2
cleaned = energy_list_GRM.strip('[]').split()
energy_list_GRM = [int(x) for x in cleaned]

data = np.loadtxt('energy_list/GRM_rsp_rate_bin_noisy.txt')
## filter parameters
order = 2 ; window_size = 5
window_length = 15 ; polyorder = 3 
GRM_n = len(energy_list_GRM) - 1
for_, for_time = moving_avg_smooth(data[0], time_timebin, order, window_size)
m_smooth = np.zeros((GRM_n+1, len(for_time))) ## one more row for recording time, because the time array may have some change when filtering.
w_smooth = np.zeros((GRM_n+1, len(time_timebin)))
s_smooth = np.zeros((GRM_n+1, len(time_timebin)))
for j in range(GRM_n):
    m_smooth[j], m_time = moving_avg_smooth(data[j], time_timebin, order, window_size)
    w_smooth[j] = wavelet_smooth(data[j])
    s_smooth[j] = savgol_filter(data[j], window_length, polyorder)
    
m_smooth[-1] = m_time
w_smooth[-1] = time_timebin
s_smooth[-1] = time_timebin
np.savetxt('energy_list/filter_data/GRM/moving_smooth.txt', m_smooth, delimiter='\t')
np.savetxt('energy_list/filter_data/GRM/wavelet_smooth.txt', w_smooth, delimiter='\t')
np.savetxt('energy_list/filter_data/GRM/sg_smooth.txt', s_smooth, delimiter='\t')
print('all filter data finish')

## fit part
## we use wavelet_smooth data as an example
A = np.zeros(GRM_n) ; tau1 = np.zeros(GRM_n) ; tau2 = np.zeros(GRM_n) ; perr = np.zeros((GRM_n, 3))
p0 =  [2000, 0.2, 0.8]
for j in range(GRM_n):
    A[j], tau1[j], tau2[j], perr[j,:] = fred_fit(w_smooth[-1], w_smooth[j], p0)

fit_param = np.column_stack((A, tau1, tau2,))
np.savetxt('fred_fit/GRM/results.txt', fit_param, header='A  tau1  tau2', delimiter='\t')
np.savetxt('fred_fit/GRM/standard_deviation.txt', perr, header='A  tau1  tau2', delimiter='\t')
print('GRM fit finish')

