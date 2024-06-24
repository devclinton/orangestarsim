from Orange.widgets.widget import OWWidget
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.utils.signals import Input, Output
from orangewidget.utils.signals import summarize, PartialSummary
from Orange.data import Table

import starsim as ss



class BirthsWidget(OWWidget):
    name = "Births"
    category = "StarSim Demographics"
    description = "Births"
    icon = "icons/births.png"
    priority = 1


    class Outputs:
        # Output will be the Starsim Network object
        births = Output("Births", ss.Births)

    
    birth_rate = Setting(30)
    rel_birth = Setting(1)
    units = Setting(1e-3)

    commitOnChange = Setting(0)

    def __init__(self):
        super().__init__()

        self.births = None

        box = gui.widgetBox(self.controlArea, "Info")
        self.info_labels = []
        self.info_labels.append(gui.label(box, self, f"birth_rate: {self.birth_rate}"))

        gui.separator(self.controlArea)

        # Options sections
        self.optionsBox = gui.widgetBox(self.controlArea, "Options")

        # now a spinner for the birth rate
        gui.spin(
            self.optionsBox, self, "birth_rate", 0, 1000, 1, label="Birth Rate", callback=self.checkUpdate
        )
        # now a spinner for rel_birth
        gui.spin(
            self.optionsBox, self, "rel_birth", 0, 1000, 1, label="Relative Birth Rate", callback=self.checkUpdate
        )
        # now a dropdown for units and ensure we set value as float
        gui.comboBox(
            self.optionsBox, self, "units", items=["1e-3", "1e-6", "1e-9"], label="Units", orientation=0, callback=self.checkUpdate
        )

    def commit(self):
        self.births = ss.Births(self.birth_rate, self.rel_birth, float(self.units))
        self.Outputs.births.send(self.births)
    
    def checkUpdate(self):
        if self.commitOnChange:
            self.commit()