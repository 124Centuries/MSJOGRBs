## show you how to read the response matrix file
import numpy as np
from generate_matrix import read_rsp, read_rsp_WXT
import sys

file_GRM = "/home/centuries/mult_messenger/rsp_matrix/svom_grm_g01_evt_x_bn24071385_v00.rsp"
file_WXT = '/home/centuries/mult_messenger/rsp_matrix/WXT_rsp'
file_GECAM_H = '/home/centuries/mult_messenger/rsp_matrix/gbg20H.rsp'  
file_GECAM_L = '/home/centuries/mult_messenger/rsp_matrix/gbg20L.rsp' ## we use low gain as an example

## GRM part
channel, e_min, e_max, energ_lo, energ_hi, matrix = read_rsp(file_GRM)
np.savetxt('matrix_data/matrix_GRM.txt', matrix, delimiter='\t')
energy = np.column_stack((energ_lo, energ_hi))
np.savetxt('matrix_data/energy_GRM.txt', energy, delimiter='\t')
ebounds = np.column_stack((e_min, e_max))
np.savetxt('matrix_data/ebounds_GRM.txt', ebounds, delimiter='\t')
print('GRM matrix data finish')

## GECAM part, you need cut some element, we already give the value to tell you cut which part.
channel, e_min, e_max, energ_lo, energ_hi, matrix = read_rsp(file_GECAM_L)
cut_matrix = matrix[:,:448] ; cut_e_min = e_min[:448] ; cut_e_max = e_max[:448] ; cut_energ_lo = energ_lo[:448] ; cut_energ_hi = energ_hi[:448]
np.savetxt('matrix_data/matrix_GECAM.txt', cut_matrix, delimiter='\t')
energy = np.column_stack((cut_energ_lo, cut_energ_hi))
np.savetxt('matrix_data/energy_GECAM.txt', energy, delimiter='\t')
ebounds = np.column_stack((cut_e_min, cut_e_max))
np.savetxt('matrix_data/ebounds_GECAM.txt', ebounds, delimiter='\t')
print('GECAM matrix data finish')

## WXT part, read_rsp_WXT is for the file formats contain arf.fits rmf.fits and bkgspec.fits
data = read_rsp_WXT(file_WXT)
energ_lo = np.array(data['arf_energ_lo'])
energ_hi = np.array(data['arf_energ_hi'])
arf_specresp = np.array(data['arf_specresp'])
bkg_counts = np.array(data['bkg_counts'])
exposure = data['exposure']
backscal = data['backscal']
areascal = data['areascal']
rmf_matrix = np.array(data['rmf_matrix'])
e_min = np.array(data['e_min'])
e_max = np.array(data['e_max'])
matrix = np.zeros((len(energ_lo),len(e_min)))
bkg_s = (bkg_counts / exposure) / backscal # 'bkg_s' refers to the counts/s in background
## get the final WXT matrix
for i in range(len(arf_specresp)):
    matrix[i,:] = rmf_matrix[i,:] * arf_specresp[i]
np.savetxt('matrix_data/matrix_WXT.txt', matrix, delimiter='\t')
ebounds = np.column_stack((e_min, e_max))
energy = np.column_stack((energ_lo, energ_hi))
np.savetxt('matrix_data/ebounds_WXT.txt', ebounds, delimiter='\t')
np.savetxt('matrix_data/energy_WXT.txt', energy, delimiter='\t')
print('WXT matrix data finish')



