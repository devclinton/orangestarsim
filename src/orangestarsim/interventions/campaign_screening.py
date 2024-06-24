from typing import Any
from Orange.widgets.widget import OWWidget
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.utils.signals import Input, Output
from orangewidget.utils.signals import summarize, PartialSummary
from Orange.data import Table

import starsim as ss

class CampaignScreeningWidget(OWWidget):
    name = "Campaign Screening"
    category = "StarSim Interventions"
    description = "Campaign Screening"
    icon = "icons/campaign_screening.png"
    priority = 1

    class Inputs:
        product = Input("Product", ss.Product)
        prob = Input("Probability of Vaccination", ss.Dist)
        eligible = Input("Eligible", Any )

    class Outputs:
        # Output will be the Starsim Network object
        screening = Output("Screening", ss.campaign_screening)

    label = Setting("Campaign Screening")
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
        self.info_labels.append(gui.label(box, self, f"Campaign Screening"))

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
    def setProduct(self, product):
        self.product = product
        if self.product is not None:
            self.checkUpdate()
            self.commit()

    @Inputs.prob
    def setProb(self, prob):
        self.prob = prob
        self.commit()
    
    @Inputs.eligible
    def setEligible(self, eligible):
        self.eligible = eligible
        self.commit()

    def commit(self):
        if self.product is not None and self.prob is not None and self.eligible is not None:
            screening = ss.campaign_screening(
                product=self.product,
                prob=self.prob,
                eligible=self.eligible,
                years=self._years,
            )
            self.Outputs.screening.send(screening)
        else:
            self.Outputs.screening.send(None)
