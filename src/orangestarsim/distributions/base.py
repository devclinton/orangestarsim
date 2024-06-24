from abc import ABC, abstractmethod
import sciris as sc
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.utils.signals import Input, Output
from orangewidget.utils.signals import summarize, PartialSummary
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import starsim as ss



# define an abstract base distribution widget that will be used by all distribution widgets
# amd has the following properties:
# - a commitOnChange setting
# - a commit method that sends the distribution object to the output
# - a figure attribute that is a FigureCanvasQTAgg object
# - a plot function that updates the figure with the distribution
class DistributionWidget:
    category = "StarSim Distributions"
    commitOnChange = Setting(0)
    canvas = None
    Outputs = None


    def _build_canvas(self):
        self.canvas = FigureCanvas()
        self.controlArea.layout().addWidget(self.canvas)

    def _build_options(self, options=None):
        if options is None:
            options = []

        box = gui.widgetBox(self.controlArea, "Options")
        for option in options:
            if len(option) < 2:
                extra_args = {}
            else:
                extra_args = option[2]
            if "callback" not in extra_args:
                extra_args["callback"] = self.updateIfCommitOnChange
            option[0](box, self, *option[1], **option[2])

        # add our checkbox to commit on change
        gui.checkBox(
            box, self, "commitOnChange", "Commit on change"
        )
        

    def commit(self):
        self.Outputs.dist.send(self.make_dist())
        self.plot()


    @abstractmethod
    def make_dist(self, sim=None, *args, **kwargs):
        pass

    def plot(self):
        # clear existing plot
        if self.canvas:
            self.canvas.figure.clf()
            self.canvas.draw()


        # render our plot
        # build sim so we can make dist
        sim = ss.Sim(people=ss.People(1000), networks=[ss.RandomNet()], diseases=[ss.SIR()])
        sim.initialize()
        dist = self.make_dist(sim=sim, name=self.name)
        dist.initialize()

        # update our plot
        self.plot_hist(dist)
        # add the plot using FigureCanvasQTAgg
        if self.canvas:
            self.canvas.figure = plt.gcf()
            self.canvas.draw()

    @staticmethod
    def plot_hist(dist, n=1000, bins=None, fig_kw=None, hist_kw=None):
        """ Plot the current state of the RNG as a histogram """
        plt.figure(**sc.mergedicts(fig_kw))
        rvs = dist.rvs(n)
        dist.reset(-1) # As if nothing ever happened
        # if rvs is numpy bool, then we plot a bar chart
        plt.title(str(dist))
        if rvs.dtype == bool:
            bins = [0, 1] if bins is None else bins
            plt.bar([0, 1], [len(rvs) - rvs.sum(), rvs.sum()], **sc.mergedicts(hist_kw))
            # add our labels
            plt.xticks([0, 1], ['False', 'True'])
            
        else:
            plt.hist(rvs, bins=bins, **sc.mergedicts(hist_kw))
        
            plt.xlabel('Value')
            plt.ylabel(f'Count ({n} total)')
        return rvs
        

    def updateIfCommitOnChange(self):
        if self.commitOnChange:
            self.commit()
