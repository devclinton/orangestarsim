from Orange.widgets.widget import OWWidget
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.utils.signals import Output
from orangestarsim.distributions.base import DistributionWidget
import starsim as ss
import sciris as sc

sc.options(interactive=False) # Assume not running interactively

class UniformDistributionWidget(OWWidget, DistributionWidget):
    name = "Uniform Distribution"
    description = "Create a uniform Distribution"
    icon = "../icons/uniform_distribution.svg"
    category = "StarSim Distributions"
    priority = 1

    low = Setting(0.0)
    high = Setting(1.0)

    class Outputs:
        dist = Output("Dist", ss.Dist)

    def __init__(self):
        super(DistributionWidget, self).__init__()
        super(OWWidget, self).__init__()
        self._build_canvas()
        # prepare our options call by build list of options
        # 1st is the low spinner with values from 0.0 to 1.0
        # 2nd is the high spinner with values from 0.0 to 1.0
        options = [
            (gui.doubleSpin, ("low", 0.0, 1.0, 0.1), dict(label="Low")),
            (gui.doubleSpin, ("high", 0.0, 1.0, 0.1), dict(label="High")),
        ]
  

        # build our options 
        self._build_options(options)
        self.commit()

    def updateIfCommitOnChange(self):
        if self.low < self.high:
            return super().updateIfCommitOnChange()
        else:
            print("Low must be less than high")

    def make_dist(self, sim=None, *args, **kwargs):
        return ss.uniform(low=self.low, high=self.high, *args, **kwargs) if sim is None else ss.uniform(low=self.low, high=self.high, sim=sim, *args, **kwargs)



if __name__ == "__main__":
    from Orange.widgets.utils.widgetpreview import WidgetPreview
    WidgetPreview(UniformDistributionWidget).run()