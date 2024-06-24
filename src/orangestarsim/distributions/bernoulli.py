from Orange.widgets.widget import OWWidget
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.utils.signals import Output
from orangestarsim.distributions.base import DistributionWidget
import starsim as ss
import sciris as sc

sc.options(interactive=False) # Assume not running interactively

class BernouliDistributionWidget(OWWidget, DistributionWidget):
    name = "Bernouli Distribution"
    description = "Create a Bernouli Distribution"
    icon = "../icons/bernoulli_distribution.svg"
    category = "StarSim Distributions"
    priority = 1

    p = Setting(0.5)

    class Outputs:
        dist = Output("Dist", ss.Dist)

    def __init__(self):
        super(DistributionWidget, self).__init__()
        super(OWWidget, self).__init__()
        self._build_canvas()
        # prepare our options call by build list of options
        # 1st is the p spinner with values from 0.0 to 1.0
        options = [
            (gui.doubleSpin, ("p", 0.0, 1.0, 0.1), dict(label="p")),
        ]
  

        # build our options 
        self._build_options(options)
        self.commit()

    def updateIfCommitOnChange(self):
        if self.p > 0:
            return super().updateIfCommitOnChange()
        else:
            print("p must be greater than 0")

    def make_dist(self, sim=None, *args, **kwargs):
        return ss.bernoulli(p=self.p, *args, **kwargs) if sim is None else ss.bernoulli(p=self.p, sim=sim, *args, **kwargs)
    

if __name__ == "__main__":
    from Orange.widgets.utils.widgetpreview import WidgetPreview
    WidgetPreview(BernouliDistributionWidget).run()