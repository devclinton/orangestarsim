from Orange.widgets.widget import OWWidget
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.utils.signals import Output
from orangestarsim.distributions.base import DistributionWidget
import starsim as ss
import sciris as sc

sc.options(interactive=False) # Assume not running interactively

class PoissonDistributionWidget(OWWidget, DistributionWidget):
    name = "Poisson Distribution"
    description = "Create a Poisson Distribution"
    icon = "../icons/poisson_distribution.svg"
    category = "StarSim Distributions"
    priority = 1

    lam = Setting(1.0)

    class Outputs:
        dist = Output("Dist", ss.Dist)

    def __init__(self):
        super(DistributionWidget, self).__init__()
        super(OWWidget, self).__init__()
        self._build_canvas()
        # prepare our options call by build list of options
        # 1st is the mean spinner with values from 0.0 to 1.0
        options = [
            (gui.doubleSpin, ("lam", 0.0, 1.0, 0.1), dict(label="Lambda")),
        ]
  

        # build our options 
        self._build_options(options)
        self.commit()

    def updateIfCommitOnChange(self):
        if self.lam > 0:
            return super().updateIfCommitOnChange()
        else:
            print("Lambda must be greater than 0")

    def make_dist(self, sim=None, *args, **kwargs):
        return ss.poisson(lam=self.lam, *args, **kwargs) if sim is None else ss.poisson(lam=self.lam, sim=sim, *args, **kwargs)