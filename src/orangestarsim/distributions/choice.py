# from Orange.widgets.widget import OWWidget
# from Orange.widgets import gui
# from Orange.widgets.settings import Setting
# from Orange.widgets.utils.signals import Output
# from orangestarsim.distributions.base import DistributionWidget
# import starsim as ss
# import sciris as sc

# sc.options(interactive=False) # Assume not running interactively

# class ChoiceDistributionWidget(OWWidget, DistributionWidget):
#     name = "Choice Distribution"
#     description = "Create a Choice Distribution"
#     icon = "icons/choice_Distribution.png"
#     category = "StarSim Distributions"
#     priority = 1

#     choices = Setting(["a", "b", "c"])

#     class Outputs:
#         dist = Output("Dist", ss.Dist)

#     def __init__(self):
#         super(DistributionWidget, self).__init__()
#         super(OWWidget, self).__init__()
#         self._build_canvas()
#         # prepare our options call by build list of options
#         # 1st is the choices text with values from a to c
#         options = [
#             (gui.lineEdit, ("choices", "a, b, c"), dict(label="Choices")),
#         ]
  

#         # build our options 
#         self._build_options(options)
#         self.commit()

#     def updateIfCommitOnChange(self):
#         return super().updateIfCommitOnChange()

#     def make_dist(self, sim=None, *args, **kwargs):
#         return ss.choice(choices=self.choices, *args, **kwargs) if sim is None else ss.choice(choices=self.choices, sim=sim, *args, **kwargs)