from typing import Any
from Orange.widgets.widget import OWWidget
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.utils.signals import Input, Output
from orangewidget.utils.signals import summarize, PartialSummary
from Orange.data import Table

import starsim as ss

class RoutineVaccinationWidget(OWWidget):
    name = "Routine Vaccination"
    category = "StarSim Interventions"
    description = "Routine Vaccination"
    icon = "icons/routine_vx.png"
    priority = 1

    class Inputs:
        product = Input("Product", ss.Product)
        prob = Input("Probability of Vaccination", ss.Dist)
        eligible = Input("Eligible", Any )

    class Outputs:
        # Output will be the Starsim Network object
        vaccination = Output("Vaccination", ss.routine_vx)

    label = Setting("Routine Vaccination")
    startYear = Setting(200)
    endYear = Setting(2024)
    yearsStr = Setting([])
    ys = Setting("")
    _years = []


    commitOnChange = Setting(0)

    def __init__(self):
        super().__init__()

        self.people = None
        self.network = None
        self.disease = None

        box = gui.widgetBox(self.controlArea, "Info")
        self.info_labels = []
        self.info_labels.append(gui.label(box, self, f"Routine Vaccination"))

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
        
        # display the years in a combolist
        self.yearsList = gui.comboBox(
            self.optionsBox, self, "ys", items=[], label="Years"
        )

        # call a custom validator function
        self.yearsList.validator = self.validateYears
        self.yearsList.setDuplicatesEnabled(False)
        self.yearsList.setEditable(True)

     
        
        gui.separator(self.controlArea)
        # Add A checkbox to commit on change
        gui.checkBox(
            self.controlArea, self, "commitOnChange", "Commit on change"
        )

    def validateYears(self, text):
        # validate text matches pattern [0-9,]{4,}

        if not text:
            return text
        if not text[-1].isdigit():
            return text[:-1]
        # now remove commas and convert to int
        text = text.replace(",", "")
        try:
            int(text)
        except ValueError:
            return text[:-1]
        return text


    def convertYears(self):
        # convert the list of year string to our _years int list
        self._years = [int(year) for year in self.yearsStr]

    def checkUpdate(self):
        if self.commitOnChange:
            self.commit()

    @Inputs.prob
    def set_prob(self, prob):
        self.prob = prob
        self.commit()

    @Inputs.eligible
    def set_eligible(self, eligible):
        self.eligible = eligible
        self.commit()

    @Inputs.product
    def set_product(self, product):
        self.product = product
        self.commit()

    def commit(self):
        if self.prob is None or self.eligible is None:
            return
        
        self.convertYears()

        rv = ss.RoutineVaccination(self.prob, self.eligible, self.startYear, self.endYear, self._years)
        self.Outputs.vaccination.send(rv)


if __name__ == "__main__":
    from Orange.widgets.utils.widgetpreview import WidgetPreview
    WidgetPreview(RoutineVaccinationWidget).run()