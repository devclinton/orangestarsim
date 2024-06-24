from typing import Any
from Orange.widgets.widget import OWWidget
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.utils.signals import Input, Output
from orangewidget.utils.signals import summarize, PartialSummary
from Orange.data import Table

import starsim as ss

class FixedTreatmentWidget(OWWidget):
    name = "Fixed Treatment"
    category = "StarSim Interventions"
    description = "Fixed Treatment"
    icon = "icons/fixed_treatment.png"
    priority = 1

    class Inputs:
        product = Input("Product", ss.Product)
        prob = Input("Probability of Treatment", ss.Dist)
        eligible = Input("Eligible", Any )

    class Outputs:
        # Output will be the Starsim Network object
        treatment = Output("Treatment", ss.treat_num)

    label = Setting("Fixed Treatment")
    startYear = Setting(200)
    endYear = Setting(2024)
    yearsStr = Setting([])
    ys = Setting("")
    _years = []

    max_capacity = Setting(1000)


    commitOnChange = Setting(0)

    def __init__(self):
        super().__init__()

        self.people = None
        self.network = None
        self.disease = None

        box = gui.widgetBox(self.controlArea, "Info")
        self.info_labels = []
        self.info_labels.append(gui.label(box, self, f"Fixed Treatment"))

        gui.separator(self.controlArea)

        self.optionsBox = gui.widgetBox(self.controlArea, "Options")
        # Now a textbox to edit the label
        gui.lineEdit(
            self.optionsBox, self, "label", "Label:", orientation=0
        )
        # present the startYear and endYear as selections from 1900 to 2100
        gui.spin(
            self.optionsBox, self, "startYear", 1900, 2100, 1, label="Start Year", callback=self.checkUpdate
        )
        gui.spin(
            self.optionsBox, self, "endYear", 1900, 2100, 1, label="End Year", callback=self.checkUpdate
        )
        # add the max capacity
        gui.spin(
            self.optionsBox, self, "max_capacity", 0, 100000, 1, label="Max Capacity", callback=self.checkUpdate
        )
        gui.separator(self.optionsBox)
        gui.checkBox(
            self.optionsBox, self, "commitOnChange", "Commit on change", callback=self.checkUpdate
        )

        self.checkUpdate()

    @Inputs.product
    def set_product(self, product):
        self.product = product
        self.checkUpdate()

    @Inputs.prob
    def set_prob(self, prob):
        self.prob = prob
        self.checkUpdate()

    @Inputs.eligible
    def set_eligible(self, eligible):
        self.eligible = eligible
        self.checkUpdate()

    def checkUpdate(self):
        if self.commitOnChange:
            self.commit()

    def commit(self):
        if self.product is not None and self.prob is not None and self.eligible is not None:
            treatment = ss.treat_num(
                product=self.product,
                prob=self.prob,
                eligible=self.eligible,
                years=self._years,
                max_capacity=self.max_capacity
            )
            self.treatment = treatment
            self.Outputs.treatment.send(treatment)