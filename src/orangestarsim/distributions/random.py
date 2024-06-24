from Orange.widgets.widget import OWWidget
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from orangestarsim.distributions.base import DistributionWidget
import starsim as ss


class RandomDistributionWidget(OWWidget, DistributionWidget):
    name = "Random Distribution"
    description = "Create a random Distribution"
    icon = "../icons/random_Distribution.png"
    category = "StarSim Distributions"
    priority = 1

    seed = Setting(3)

    def __init__(self):
        self._build_canvas()
        

        # prepare our options call by build list of options
        # 1st is the seed slider
        options = [
            (gui.hSlider, ("seed",), dict(label="Seed", minValue=0, maxValue=100, step=1))
        ]

        # build our options 
        self._build_options(options)
        self.commit()

    def make_dist(self, sim=None, *args, **kwargs):
        return ss.random(seed=self.seed, *args, **kwargs) if sim is None else ss.random(seed=self.seed, sim=sim, *args, **kwargs)
    
