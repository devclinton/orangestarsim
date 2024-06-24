from typing import Any
from Orange.widgets.widget import OWWidget
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.utils.signals import Input, Output
from orangewidget.utils.signals import summarize, PartialSummary
from Orange.data import Table

import starsim as ss

class RoutineScreening(OWWidget):
    name = "Routine Screening"
    category = "StarSim Interventions"
    description = "Routine Screening"
    icon = "icons/routine_screening.png"
    priority = 1

    class Inputs:
        product = Input("Product", ss.Product)
        prob = Input("Probability of Screening", ss.Dist)
        eligible = Input("Eligible", Any )

    class Outputs:
        # Output will be the Starsim Network object
        screening = Output("Screening", ss.routine_screening)

    label = Setting("Routine Screening")
    startYear = Setting(200)
    endYear = Setting(2024)
    yearsStr = Setting([])
    ys = Setting("")
    _years = []


    commitOnChange = Setting(0)

    def __init__(self):
        super().__init__()

        box = gui.widgetBox(self.controlArea, "Info")
        self.info_labels = []
        self.info_labels.append(gui.label(box, self, f"Routine Screening"))

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
        # checkbox for commit on change
        gui.checkBox(
            self.optionsBox, self, "commitOnChange", "Commit on change"
        )

    def checkUpdate(self):
        if self.commitOnChange:
            self.commit()

    @Inputs.product
    def set_product(self, product):
        self.product = product
        self.commit()

    @Inputs.prob
    def set_prob(self, prob):
        self.prob = prob
        self.commit()

    @Inputs.eligible
    def set_eligible(self, eligible):
        self.eligible = eligible
        self.commit()

    def commit(self):
        if self.product is not None and self.prob is not None and self.eligible is not None:
            screening = ss.routine_screening(
                product=self.product,
                prob=self.prob,
                eligible=self.eligible,
                years=self._years,
                start_year=self.startYear,
                end_year=self.endYear
            )
            self.Outputs.screening.send(screening)
        else:
            self.Outputs.screening.send(None)
        