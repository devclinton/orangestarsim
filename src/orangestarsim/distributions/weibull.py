from Orange.widgets.widget import OWWidget
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.utils.signals import Output
from orangestarsim.distributions.base import DistributionWidget
import starsim as ss
import sciris as sc

sc.options(interactive=False) # Assume not running interactively

class WeibullDistributionWidget(OWWidget, DistributionWidget):
    name = "Weibull Distribution"
    description = "Create a Weibull Distribution"
    icon = "../icons/weibull_distribution.svg"
    category = "StarSim Distributions"
    priority = 1

    c= Setting(1)
    loc = Setting(0)
    scale = Setting(1)


    class Outputs:
        dist = Output("Dist", ss.Dist)

    def __init__(self):
        super(DistributionWidget, self).__init__()
        super(OWWidget, self).__init__()
        self._build_canvas()
        # prepare our options call by build list of options
        # 1st is the shape spinner with values from 0.0 to 1.0
        # 2nd is the scale spinner with values from 0.0 to 1.0
        options = [
            (gui.spin, ("c", 0, 10000, 1), dict(label="C")),
            (gui.spin, ("loc", 0, 10000, 1), dict(label="Shape")),
            (gui.spin, ("scale", 0, 10000, 1), dict(label="Scale")),
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
        return ss.weibull(c=self.c, loc=self.loc, scale=self.scale, *args, **kwargs) if sim is None else ss.weibull(c=self.c,loc=self.loc, scale=self.scale, sim=sim, *args, **kwargs)
    

if __name__ == "__main__":
    from Orange.widgets.utils.widgetpreview import WidgetPreview
    WidgetPreview(WeibullDistributionWidget).run()