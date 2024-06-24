from Orange.widgets.widget import OWWidget
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.utils.signals import Output
from orangestarsim.distributions.base import DistributionWidget
import starsim as ss
import sciris as sc

sc.options(interactive=False) # Assume not running interactively

class LogNormalExplicitDistributionWidget(OWWidget, DistributionWidget):
    name = "LogNormal Explicit Distribution"
    description = "Create a lognormal explicit Distribution"
    icon = "icons/lognormal_explicit_Distribution.png"
    category = "StarSim Distributions"
    priority = 1

    mean = Setting(0.0)
    stdev = Setting(1.0)

    class Outputs:
        dist = Output("Dist", ss.Dist)

    def __init__(self):
        super(DistributionWidget, self).__init__()
        super(OWWidget, self).__init__()
        self._build_canvas()
        # prepare our options call by build list of options
        # 1st is the mean spinner with values from 0.0 to 1.0
        # 2nd is the std spinner with values from 0.0 to 1.0
        options = [
            (gui.doubleSpin, ("mean", 0.0, 1.0, 0.1), dict(label="Mean")),
            (gui.doubleSpin, ("stdev", 0.0, 1.0, 0.1), dict(label="Std Deviation")),
        ]
  

        # build our options 
        self._build_options(options)
        self.commit()

    def updateIfCommitOnChange(self):
        if self.stdev > 0:
            return super().updateIfCommitOnChange()
        else:
            print("Std must be greater than 0")

    def make_dist(self, sim=None, *args, **kwargs):
        return ss.lognormal(mean=self.mean, stdev=self.stdev, *args, **kwargs) if sim is None else ss.lognormal(mean=self.mean, stdev=self.stdev, sim=sim, *args, **kwargs)
