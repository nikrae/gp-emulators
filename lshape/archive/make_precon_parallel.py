# AUTHOR: NK, kraemer(at)ins.uni-bonn.de

"""
run with:
script.py num_pts <path_to_precon_and_mesh_folder>, 
e.g.
python3 make_precon.py 225 /home/kraemer/Programmieren/txts/ 
or
python3 make_precon.py 225 /local/hdd/kraemer/lshape/files
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.spatial
import scipy.sparse.linalg as spla
import scipy.sparse
import scipy.linalg


import sys
sys.path.insert(0,'../modules/')

from pointsets import *
from covariances import *
from misc import gmresCounter

from joblib import Parallel, delayed
import multiprocessing
import time




#def localco(idx, tree, numPts, numNeighb, k2, distneighb, indneighb, ptSet, kernelMtrxFct, polBlockSize):
def localco(idx):
	time.sleep(0.00)
	retu = np.ones((k2, 3))
	distNeighb = distneighb[idx,:]
	indNeighb = indneighb[idx,:]
	locKernelMtrx = kernelMtrxFct(ptSet[indNeighb], ptSet[indNeighb])
	locRhs = np.zeros(len(locKernelMtrx))
	locRhs[0] = 1
#	locCoeff = locRhs
	lu, piv = scipy.linalg.lu_factor(locKernelMtrx)
	locCoeff = scipy.linalg.lu_solve((lu, piv), locRhs)
	retu[:,0] = locCoeff #val
	retu[:numNeighb, 1] = indNeighb #row
	retu[numNeighb:, 1] = numPts + np.arange(polBlockSize) #row
	retu[:,2] = idx #col
	return retu

"""
@staticmethod
def precon_parallel(ptSet, radius, kernelMtrxFct, polBlockSize):

	tree = scipy.spatial.KDTree(ptSet)
	numPts = len(ptSet)
	numNeighb = 1.0 * radius * np.log10(numPts) * np.log10(numPts)
	numNeighb = int(np.minimum(np.floor(numNeighb), numPts))
	k2 = numNeighb + polBlockSize
	preconVals = np.zeros(k2 * numPts)
	preconRowIdx = np.zeros(k2 * numPts)
	preconColIdx = np.zeros(k2 * numPts)
	distneighb, indneighb = tree.query(ptSet, k = numNeighb)


	num_cores = multiprocessing.cpu_count()
	Ret = Parallel(n_jobs=num_cores, backend = "multiprocessing")(delayed(LocalLagrange.localco)(i, tree, numPts, numNeighb, k2, distneighb, indneighb, ptSet, kernelMtrxFct, polBlockSize) for i in range(numPts))
	retu = np.vstack(Ret)
	return retu[:,0], retu[:,1], retu[:,2], k2

"""



















if __name__ == '__main__':

	save_txt = False

	loc_radius = 30
	dim = 2

	# 21, 65, 225, 833, 3201, ...
	num_pts = int(sys.argv[1])
	path_to_mesh = sys.argv[2] + "mesh/lmesh_N%u.txt"%num_pts
	path_to_precon = sys.argv[2]

	ptset = np.loadtxt(path_to_mesh)


	cov_fct = TPS.fast_mtrx
	polblocksize = 1 + dim


	ptSet = ptset 
	radius = loc_radius 
	kernelMtrxFct = cov_fct 
	polBlockSize = polblocksize
	tree = scipy.spatial.KDTree(ptSet)
	numPts = len(ptSet)
	numNeighb = 1.0 * radius * np.log10(numPts) * np.log10(numPts)
	numNeighb = int(np.minimum(np.floor(numNeighb), numPts))
	k2 = numNeighb + polBlockSize
	preconVals = np.zeros(k2 * numPts)
	preconRowIdx = np.zeros(k2 * numPts)
	preconColIdx = np.zeros(k2 * numPts)
	distneighb, indneighb = tree.query(ptSet, k = numNeighb)


	num_cores = multiprocessing.cpu_count()
	num_cores = 8
	pool = multiprocessing.Pool(num_cores)
	Ret = pool.map(localco, range(numPts))
	pool.close()


#	Ret = Parallel(n_jobs=num_cores, backend = "multiprocessing")(delayed(localco)(i) for i in range(numPts))
#	Ret = Parallel(n_jobs=num_cores, backend = "threading", verbose = 50)(delayed(localco)(i, tree, numPts, numNeighb, k2, distneighb, indneighb, ptSet, kernelMtrxFct, polBlockSize) for i in range(numPts))
	retu = np.vstack(Ret)#
	precon_vals = retu[:,0]
	precon_rowidx = retu[:,1]
	precon_colidx = retu[:,2]
	num_neighb = k2
	print("Number of cores:", num_cores)
	print('\nInitialising\n\tN = %d\n\tn = %d'%(num_pts, num_neighb))


	sys.exit()


	precon = scipy.sparse.coo_matrix((precon_vals, (precon_rowidx, precon_colidx)), shape=(num_pts + polblocksize, num_pts + polblocksize))




	#print(np.linalg.norm(precon_rowidx - precon_rowidx_par))
	#print(np.linalg.norm(precon_colidx - precon_colidx_par))
	#print(np.where(precon_vals != precon_vals_par))
	#print(np.where(precon_rowidx != precon_rowidx_par))
	#print(np.where(precon_colidx != precon_colidx_par))
	print('\nInitialising\n\tN = %d\n\tn = %d'%(num_pts, num_neighb))
	print('Memory footprint of ptset:\n\t %.1f MB'%(ptset.nbytes/(1024**2)))
	print('Memory footprint  of sparse matrix:\n\t %.1f MB'%(sys.getsizeof(precon.data)/(1024**2)))
	print('Memory footprint of full matrix:\n\t %.1f MB'%((precon.toarray()).nbytes/(1024**2)))






	if save_txt == True:
		print('Saving')
		path_to_precon_val = path_to_precon + "precon/precon_val_N%d_n%d.txt"%(num_pts, num_neighb)
		path_to_precon_row = path_to_precon + "precon/precon_row_N%d_n%d.txt"%(num_pts, num_neighb)
		path_to_precon_col = path_to_precon + "precon/precon_col_N%d_n%d.txt"%(num_pts, num_neighb)

	#	np.savetxt("precon_txt_tps_square/ptSet_Halton_N%d_n%d.txt"%(num_pts, num_neighb), ptset, fmt='%.17e')
		np.savetxt(path_to_precon_val, precon_vals, fmt='%.17e')
		np.savetxt(path_to_precon_row, precon_rowidx, fmt='%d')
		np.savetxt(path_to_precon_col, precon_colidx, fmt='%d')
		print('\tcomplete')
	print()

	if num_pts>15000:
		sys.exit()

	P = precon.toarray()
	P[num_pts:(num_pts+3), num_pts:(num_pts+3)] = np.eye(3)
	covmat = TPS.fast_mtrx(ptset, ptset)
	cond_covmat = covmat.dot(P)
	#cond_covmat = cond_covmat[:num_pts, :num_pts]


	#print("PTSET", ptset)
	#print("COVMAT", covmat)
	#print("PRECON", P)



	print('Computing GMRES')
	count = gmresCounter()






	rhs = np.random.rand(len(cond_covmat))
	rhs[len(rhs)-polblocksize::] = 0
	x0 = 0 * rhs

	x, info = spla.gmres(cond_covmat, rhs, callback = count)

	#cond_covmat = cond_covmat[0:num_pts, 0:num_pts]
	#print('Condition number of covariance matrix:\n\tc(M)\t= %.1f' % np.linalg.cond(covmat))

	#print('Condition number of preconditioned matrix:\n\tc(MP)\t= %.1f' % np.linalg.cond(cond_covmat))

	print('\t%u iterations' % count.numIter)
	print()