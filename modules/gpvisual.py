"""
NAME: gpvisual.py

PURPOSE: Visualisation class for GP
"""

from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np

from pointsets import Mesh1d
from gaussianprocesses import GaussianProcess#, ConditionedGaussianProcess


class GPVisual():

    def __init__(self, GaussProc, ctheme = "darkred", num_pts = 200, 
                 xlim = [0,1], title = "", naked = False):
        plt.style.use("ggplot")
        plt.rcParams["figure.figsize"] = [10,5]
        plt.rcParams["lines.linewidth"] = 3
        plt.rcParams["lines.markersize"] = 8
        plt.rcParams["grid.linewidth"] = 1
        plt.rcParams["font.size"] = 16
        plt.rcParams['xtick.major.width']= 0
        plt.rcParams['ytick.major.width']= 0
        if naked == True:
            plt.rcParams["axes.facecolor"] = "white"
        fig = plt.figure()
        ax = plt.axes()
        plt.title(title, color = "black", alpha = 0.6)
        plt.xlim(xlim)
        plt.grid(True)
        self.fig = fig
        self.ax = ax
        self.gp = GaussProc
        self.num_pts = num_pts
        self.mesh = Mesh1d(self.num_pts)
        self.mean_vec = self.gp.mean_fct.assemble_mean_vec(self.mesh.points)
        self.color = ctheme

    def addplot_mean(self):
        self.ax.plot(self.mesh.points, self.mean_vec, color = self.color, 
                     label = "Mean function")


    def addplot_deviation(self, num_dev = 2):
        cov_mtrx = self.gp.cov_fct.assemble_cov_mtrx(self.mesh.points, self.mesh.points)
        pos_dev = self.mean_vec.T + 2*num_dev*np.sqrt(np.abs(np.diag(cov_mtrx)))
        neg_dev = self.mean_vec.T - 2*num_dev*np.sqrt(np.abs(np.diag(cov_mtrx)))
        self.ax.fill_between(self.mesh.points[:,0], neg_dev[0,:], pos_dev[0,:], 
                             facecolor = self.color, linewidth = 1, linestyle = "-", 
                             alpha = 0.3, label = "Confidence interval")

    def addplot_samples(self, num_samp = 5):
        for i in range(num_samp):
            samp = self.gp.sample(self.mesh)
            self.ax.plot(self.mesh.points, samp, '--')

    def addplot_observations(self):
        if self.gp.data is None:
            print("This GP does not have data, hence no observations")
        else:
            locations = self.gp.data.locations.points
            observations = self.gp.data.observations
            self.ax.plot(locations, observations, 'o', color = "white")
            if self.gp.data.variance == 0:
                self.ax.plot(locations, observations, 'o', color = self.color,
                             markerfacecolor = "white", markeredgecolor = self.color, 
                             markeredgewidth = 2, label = "Observations")
            else:
                self.ax.errorbar(locations, observations, 
                             yerr = np.sqrt(self.gp.data.variance), color = self.color, 
                             fmt='o', markerfacecolor = "white", 
                             markeredgecolor = self.color, markeredgewidth = 2, 
                             capsize = 3, label = "Observations")


    def addanimation_samples(self):

        def init():
            line.set_data([], [])
            return line,

        def animate(i):
            samp = self.gp.sample(self.mesh)
            line.set_data(self.mesh.points, samp)
            line.set_linewidth(3)
            line.set_color(0.3*np.random.rand(3,))
            return line,

        line, = self.ax.plot([], [])
        self.anim = animation.FuncAnimation(self.fig, animate, init_func=init,
                                       frames=25, interval=500, blit=True)



class NakedGPVisual(GPVisual):
    def __init__(self, GaussProc, num_pts = 200, xlim = [0,1], title = ""):
        GPVisual.__init__(self, GaussProc, num_pts = 200, xlim = [0,1], 
                          title = "", naked = True)
        plt.grid(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)
        plt.tick_params(top=False, bottom=False, left=False, right=False, 
                        labelleft=False, labelbottom=False)

