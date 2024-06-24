from Orange.widgets.widget import OWWidget
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.utils.signals import Input, Output
from orangewidget.utils.signals import summarize, PartialSummary
from Orange.data import Table

import starsim as ss



class DeathsWidget(OWWidget):
    name = "Deaths"
    category = "StarSim Demographics"
    description = "Deaths"
    icon = "icons/deaths.png"
    priority = 1

    class Outputs:
        # Output will be the Starsim Network object
        deaths = Output("Deaths", ss.Deaths)

    rel_death = Setting(1)
    death_rate = Setting(20)
    units = Setting(1e-3)

    commitOnChange = Setting(0)

    def __init__(self):

        super().__init__()

        self.deaths = None

        box = gui.widgetBox(self.controlArea, "Info")
        self.info_labels = []
        self.info_labels.append(gui.label(box, self, f"death_rate: {self.death_rate}"))

        gui.separator(self.controlArea)

        # Options sections
        self.optionsBox = gui.widgetBox(self.controlArea, "Options")

        # now a spinner for the death rate
        gui.spin(
            self.optionsBox, self, "death_rate", 0, 1000, 1, label="Death Rate", callback=self.checkUpdate
        )
        # now a spinner for rel_death
        gui.spin(
            self.optionsBox, self, "rel_death", 0, 1000, 1, label="Relative Death Rate", callback=self.checkUpdate
        )
        # now a dropdown for units and ensure we set value as float
        gui.comboBox(
            self.optionsBox, self, "units", items=["1e-3", "1e-6", "1e-9"], label="Units", orientation=0, callback=self.checkUpdate
        )

    def commit(self):
        self.deaths = ss.Deaths(self.death_rate, self.rel_death, float(self.units))
        self.Outputs.deaths.send(self.deaths)
    
    def checkUpdate(self):
        self.commit()