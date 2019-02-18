# FILENAME: sampleEvolBasic.py
# PURPOSE: playground for basic mcmc 
# DESCRIPTION: set up a toy example for mcmc sampling and approximate with Metropolis sampler
# AUTHOR: NK

import matplotlib
import numpy as np 
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from scipy.stats import norm
np.set_printoptions(precision = 1)
#plt.rcParams.update({'font.size': 20})
#plt.rcParams.update({'legend.fontsize': 20})

np.random.seed(15051994)


def gaussDens(pt, mean = 0, variance = 1.):
	return np.exp(-(pt-mean)**2/(2*variance))/(np.sqrt(2*np.pi*variance))

propWidth = 1.
numPlots = 4
numSamp = 250
samplesSmall = np.zeros(numSamp)
currSamp = 0.5
i = 0
samplesSmall[i] = currSamp

i = i + 1



while i < numSamp:
	proposal =  currSamp + propWidth * np.random.randn()
	accProb = gaussDens(proposal)/gaussDens(currSamp)
	ratio = np.random.rand()
	if accProb < ratio:
		samplesSmall[i] = currSamp
	else:
		samplesSmall[i] = proposal
		currSamp = proposal
	i = i + 1




propWidth = 1.
numPlots = 4
numSamp = 250
samplesBig = np.zeros(numSamp)
currSamp = 12.0
i = 0
samplesBig[i] = currSamp

i = i + 1



while i < numSamp:
	proposal =  currSamp + propWidth * np.random.randn()
	accProb = gaussDens(proposal)/gaussDens(currSamp)
	ratio = np.random.rand()
	if accProb < ratio:
		samplesBig[i] = currSamp
	else:
		samplesBig[i] = proposal
		currSamp = proposal
	i = i + 1




plt.figure()
plt.plot(samplesSmall, linewidth = 3, color = "darkblue", label ="Starting at x = 0.5", alpha = 0.9)
plt.plot(samplesBig, linewidth = 3, color = "red", label ="Starting at x = 12.0", alpha = 0.9)
plt.grid()
xl = plt.xlabel("Iteration")
yl = plt.ylabel("Samples")
plt.ylim((-5,15))
plt.legend()
plt.savefig("figures/burnIn", bbox_extra_artists= (xl, ), bbox_inches ="tight")
plt.show()














# plt.plot(samples, linewidth = 2)
# plt.title("Trace of Metropolis sampling")
# plt.xlabel("sample")
# plt.ylabel("mean")
# plt.show()




