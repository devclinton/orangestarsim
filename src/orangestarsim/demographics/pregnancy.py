from Orange.widgets.widget import OWWidget
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.utils.signals import Input, Output
from orangewidget.utils.signals import summarize, PartialSummary
from Orange.data import Table

import starsim as ss

class PregnancyWidget(OWWidget):
    name = "Pregnancy"
    category = "StarSim Demographics"
    description = "Pregnancy"
    icon = "icons/pregnancy.png"
    priority = 1

    _network = None
    class Inputs:
        dur_preg = Input("Duration of Pregnancy", ss.Dist)
        dur_postpartum = Input("Duration of Postpartum", ss.Dist)
        maternal_death_prob = Input("Maternal Death Probability", ss.Dist)
        sex_ratio = Input("Sex Ratio", ss.Dist)
    


    class Outputs:
        # Output will be the Starsim Network object
        pregancy = Output("Pregnancy", ss.Pregnancy)

    
    # TODO fert rate from file or from int here
    rel_fertility = Setting(1)
    min_age = Setting(15)
    max_age = Setting(50)
    units = Setting(1e-3)

    commitOnChange = Setting(0)

    def __init__(self):
        super().__init__()

        self.preg = None

        box = gui.widgetBox(self.controlArea, "Info")
        self.info_labels = []
        self.info_labels.append(gui.label(box, self, f"min_age: {self.min_age}"))
        self.info_labels.append(gui.label(box, self, f"max_age: {self.max_age}"))
        self.info_labels.append(gui.label(box, self, f"units: {self.units}"))

        gui.separator(self.controlArea)

        # Options sections
        self.optionsBox = gui.widgetBox(self.controlArea, "Options")
        # rel_fertility
        gui.spin(
            self.optionsBox, self, "rel_fertility", 0, 1000, 1, label="Relative Fertility", callback=self.checkUpdate
        )
        # min_age
        gui.spin(
            self.optionsBox, self, "min_age", 0, 100, 1, label="Min Age", callback=self.checkUpdate
        )
        # max_age
        gui.spin(
            self.optionsBox, self, "max_age", 0, 100, 1, label="Max Age", callback=self.checkUpdate
        )
        # now a dropdown for units and ensure we set value as float
        gui.comboBox(
            self.optionsBox, self, "units", items=["1e-3", "1e-6", "1e-9"], label="Units", orientation=0, callback=self.checkUpdate
        )

    def commit(self):
        preg = ss.Pregnancy(self.rel_fertility, self.min_age, self.max_age, float(self.units))
        self.Outputs.pregancy.send(preg)

    def checkUpdate(self):
        if self.commitOnChange:
            self.commit()

    @Inputs.dur_preg
    def set_dur_preg(self, dur_preg):
        self.dur_preg = dur_preg
        self.commit()

    @Inputs.dur_postpartum
    def set_dur_postpartum(self, dur_postpartum):
        self.dur_postpartum = dur_postpartum
        self.commit()

    @Inputs.maternal_death_prob
    def set_maternal_death_prob(self, maternal_death_prob):
        self.maternal_death_prob = maternal_death_prob
        self.commit()

    @Inputs.sex_ratio
    def set_sex_ratio(self, sex_ratio):
        self.sex_ratio = sex_ratio