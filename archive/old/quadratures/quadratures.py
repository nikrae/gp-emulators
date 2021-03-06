# The pointset is based on a randomly shifted lattice rule
# with product weight $\gamma_j = 1/j^2$,
# based on the generating vector from Frances Kuo's website
# http://web.maths.unsw.edu.au/∼fkuo/
# as “lattice-39102-1024-1048576.3600”.



from __future__ import division	#division of integers into decimal
import numpy as np 

# Computes the lattice points for qmc integration
def get_latticepoints_unitsquare(N, dim):

	# load generating vector
	genvecold = np.loadtxt('/Users/nicholaskramer/Documents/GitHub/gp-emulators/quadratures/vec.txt')
	genvecnew = genvecold[0:dim, 1]

	# generate lattice points and random shift
	pts = np.zeros((N, dim))

	shift = np.random.rand(dim)
	for i in range(N):
		pts[i,:] = (genvecnew * i / N  + shift)% 1

	return pts

# computes the QMC integral of FCT 
# at points PTS in the interval [-1,1]^dim; 
# if FCT needs parameters do it via functools -> partial
def qmc_integral(FCT, PTS):
	N = PTS.shape[0]
	dim = PTS.shape[1]
	summ = 0
	for i in range(N):
		summ = summ + FCT(PTS[i,:])

	summ = summ/(2**dim)
	return summ/N



