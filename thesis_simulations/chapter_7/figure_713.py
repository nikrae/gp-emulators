# AUTHOR: NK, kraemer(at)ins.uni-bonn.de

import numpy as np
import matplotlib.pyplot as plt
import scipy.spatial
import scipy.sparse.linalg as spla
import scipy.sparse
import scipy.linalg


import sys
sys.path.insert(0,'../../modules/')

from pointsets import *
from misc import *
from covariances import *

save_txt = False

num_pts = 256
loc_radius = 7.0

ptset = FibonacciSphere.construct(num_pts, rand_shift = False)
cov_fct = TPSSphere.fast_mtrx
polblocksize = 4

precon_vals, precon_rowidx, precon_colidx, num_neighb = LocalLagrange.precon(ptset, loc_radius, cov_fct, polblocksize)

precon = scipy.sparse.coo_matrix((precon_vals, (precon_rowidx, precon_colidx)), shape=(num_pts + polblocksize, num_pts + polblocksize))

print('\nN = %d, n = %d\n'%(num_pts, num_neighb))
print('Memory footprint of ptset:\n\t %.1f MB'%(ptset.nbytes/(1024**2)))
print('Memory footprint  of sparse matrix:\n\t %.1f MB'%(sys.getsizeof(precon.data)/(1024**2)))
print('Memory footprint of full matrix:\n\t %.1f MB'%((precon.toarray()).nbytes/(1024**2)))






if save_txt == True:
	np.savetxt("precon_txt_tps_sphere/ptSet_Halton_N%d_n%d.txt"%(num_pts, num_neighb), ptset, fmt='%.17e')
	np.savetxt("precon_txt_tps_sphere/preconVals_N%d_n%d.txt"%(num_pts, num_neighb), precon_vals, fmt='%.17e')
	np.savetxt("precon_txt_tps_sphere/preconRowIdx_N%d_n%d.txt"%(num_pts, num_neighb), precon_rowidx, fmt='%d')
	np.savetxt("precon_txt_tps_sphere/preconColIdx_N%d_n%d.txt"%(num_pts, num_neighb), precon_colidx, fmt='%d')
	print('\n\nSaving complete\n')
print()


covmat = TPSSphere.fast_mtrx(ptset, ptset)
cond_covmat = covmat.dot(precon.toarray())
cond_covmat = cond_covmat[0:num_pts, 0:num_pts]
print('Condition number of covariance matrix:\n\tc(M)\t= %.1f' % np.linalg.cond(covmat))

print('Condition number of preconditioned matrix:\n\tc(MP)\t= %.1f' % np.linalg.cond(cond_covmat))
