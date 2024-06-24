from Orange.widgets.widget import OWWidget
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.utils.signals import Output
from orangestarsim.distributions.base import DistributionWidget
import starsim as ss
import sciris as sc

sc.options(interactive=False) # Assume not running interactively

class ConstantDistributionWidget(OWWidget, DistributionWidget):
    name = "Constant Distribution"
    description = "Create a constant Distribution"
    icon = "icons/constant_distribution.svg"
    category = "StarSim Distributions"
    priority = 1

    value = Setting(0.0)

    class Outputs:
        dist = Output("Dist", ss.Dist)

    def __init__(self):
        super(DistributionWidget, self).__init__()
        super(OWWidget, self).__init__()
        self._build_canvas()
        # prepare our options call by build list of options
        # 1st is the value spinner with values from 0.0 to 1.0
        options = [
            (gui.doubleSpin, ("value", 0.0, 1.0, 0.1), dict(label="Value")),
        ]
  

        # build our options 
        self._build_options(options)
        self.commit()

    def updateIfCommitOnChange(self):
        return super().updateIfCommitOnChange()

    def make_dist(self, sim=None, *args, **kwargs):
        return ss.constant(v=self.value, *args, **kwargs) if sim is None else ss.constant(v=self.value, sim=sim, *args, **kwargs)