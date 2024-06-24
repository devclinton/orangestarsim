from Orange.widgets.widget import OWWidget
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.utils.signals import Output
from orangestarsim.distributions.base import DistributionWidget
import starsim as ss
import sciris as sc

sc.options(interactive=False) # Assume not running interactively

class ExponentialDistributionWidget(OWWidget, DistributionWidget):
    name = "Exponential Distribution"
    description = "Create an exponential Distribution"
    icon = "icons/exponential_Distribution.png"
    category = "StarSim Distributions"
    priority = 1

    scale = Setting(1.0)

    class Outputs:
        dist = Output("Dist", ss.Dist)

    def __init__(self):
        super(DistributionWidget, self).__init__()
        super(OWWidget, self).__init__()
        self._build_canvas()
        # prepare our options call by build list of options
        # 1st is the mean spinner with values from 0.0 to 1.0
        options = [
            (gui.doubleSpin, ("scale", 0.0, 1.0, 0.1), dict(label="Scale")),
        ]
  

        # build our options 
        self._build_options(options)
        self.commit()

    def updateIfCommitOnChange(self):
        if self.scale > 0:
            return super().updateIfCommitOnChange()
        else:
            print("Scale must be greater than 0")

    def make_dist(self, sim=None, *args, **kwargs):
        return ss.exponential(scale=self.scale, *args, **kwargs) if sim is None else ss.exponential(scale=self.scale, sim=sim, *args, **kwargs)