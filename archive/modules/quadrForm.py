# NAME: 'quadrForm.py'
#
# PURPOSE: Collect different quadrature formulas
#
# DESCRIPTION: see PURPOSE
#
# AUTHOR: NK, kraemer(at)ins.uni-bonn.de

from __future__ import division
import numpy as np 

def compQuadQMC(integrand, ptSet):
	numPts = ptSet.shape[0]
	dim = ptSet.shape[1]
	qmcSum = 0.0
	for idx in range(numPts):
		qmcSum = qmcSum + integrand(ptSet[idx,:])

#	return qmcSum/(N * 2.0**dim)
	return qmcSum/(numPts * 1.0)
