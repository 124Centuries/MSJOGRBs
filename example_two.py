## show you how to use function all_rsp
import numpy as np
from read_param import read_param
from all_rsp import all_rsp
from generate_lc import generate_lc
import sys

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
energy_gen = np.arange(gen1, gen2, gen_dt)
gen_centers = (energy_gen[1:] + energy_gen[:-1]) / 2
cleaned = energy_list_GRM.strip('[]').split()
energy_list_GRM = [int(x) for x in cleaned]

## get the matrix data
matrix_GRM = np.loadtxt('matrix_data/matrix_GRM.txt')
ebounds_GRM = np.loadtxt('matrix_data/ebounds_GRM.txt')
energy_GRM = np.loadtxt('matrix_data/energy_GRM.txt')
e_min = ebounds_GRM[:,0] ; e_max = ebounds_GRM[:,1]
energ_lo = energy_GRM[:,0] ; energ_hi = energy_GRM[:,1]
print('GRM matrix data finish')

## get profile and spectrum
profile = np.loadtxt('profile/profile_test.txt')
spectrum = np.loadtxt('spectrum/spectrum_test.txt')
print('get profile and spectrum')
## generate fine_counts
counts_list, fine_counts, flux, fluence, factor = generate_lc(time, energy_gen, energy_list_GRM, fluence_target, energy_target, time_target, profile, spectrum)
print('fine_counts finish')
## get data without noise, channel means deposited channel or recording channel
noisy = False
counts_channel, counts_list, counts_channel_bin, counts_list_bin = all_rsp(fine_counts, time, energy_gen, energ_lo, energ_hi, e_min, e_max, energy_list_GRM, matrix_GRM, noisy, time_bin)
np.savetxt('energy_list/GRM_rsp_rate_bin.txt', counts_list_bin, delimiter='\t')
np.savetxt('energy_list_plot/GRM_rsp_rate_bin.txt', counts_channel_bin, delimiter='\t')
np.savetxt('energy_list_plot/GRM_rsp_rate.txt', counts_channel, delimiter='\t')
print('GRM no noise part finish')
## get data with adding noise
noisy = True
counts_channel, counts_list, counts_channel_bin, counts_list_bin = all_rsp(fine_counts, time, energy_gen, energ_lo, energ_hi, e_min, e_max, energy_list_GRM, matrix_GRM, noisy, time_bin)
np.savetxt('energy_list/GRM_rsp_rate_bin_noisy.txt', counts_list_bin, delimiter='\t')
np.savetxt('energy_list_plot/GRM_rsp_rate_bin_noisy.txt', counts_channel_bin, delimiter='\t')
np.savetxt('energy_list_plot/GRM_rsp_rate_noisy.txt', counts_channel, delimiter='\t')
print('GRM noise part finish')
