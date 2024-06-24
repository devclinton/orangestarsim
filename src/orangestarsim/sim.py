
from Orange.widgets.widget import OWWidget
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.utils.signals import Input, Output
from orangewidget.utils.signals import summarize, PartialSummary
from Orange.data import Table

import starsim as ss




class SimWidget(OWWidget):
    name = "Sim"
    category = "StarSim"
    description = "Sim"
    icon = "icons/simulation.svg"
    priority = 1


    class Inputs:
        people = Input("People", ss.People)
        networks = Input("Networks", ss.Network, multiple=True)
        diseases = Input("SIR",ss.Disease, multiple=True)

    class Outputs:
        # Output will be the Starsim Network object
        sim = Output("sim", ss.Sim)

    
    label = Setting("Sim")

    commitOnChange = Setting(0)

    # cache of the sim
    _sim = None

    
    def __init__(self):
        super().__init__()

        self.people = None
        self.networks = dict()
        self.diseases = dict()

        self.sim = None

        box = gui.widgetBox(self.controlArea, "Info")
        self.info_labels = []
        self.info_labels.append(gui.label(box, self, f"Sim"))
        
        gui.separator(self.controlArea)

        self.optionsBox = gui.widgetBox(self.controlArea, "Options")
        # Now a textbox to edit the label
        gui.lineEdit(
            self.optionsBox, self, "label", "Label:", orientation=0
        )

        gui.separator(self.controlArea)
        # Add A checkbox to commit on change
        gui.checkBox(
            self.controlArea, self, "commitOnChange", "Commit on change"
        )

        self.commit()

    def commit(self):
        # Ensure we have at least people, network, and disease
        if self.people is None or len(self.networks) == 0 or len(self.diseases) == 0:
            return

        networks = list(self.networks.values())
        diseases = list(self.diseases.values())
        _sim = ss.Sim(
            people=self.people,
            networks=networks,
            diseases=diseases,
        )
        self.Outputs.sim.send(_sim)

    @Inputs.people
    def set_people(self, people):
        self.people = people
        self.commit()

    @Inputs.networks
    def set_networks(self, networks, id):
        self.networks[id] = networks
        self.commit()

    @Inputs.diseases
    def set_diseases(self, disease, id):
        self.diseases[id] = disease
        self.commit()

    def updateIfCommit(self):
        if self.commitOnChange:
            self.commit()



if __name__ == "__main__":
    from Orange.widgets.utils.widgetpreview import WidgetPreview
    ppl = ss.People(100)
    network_pars = {
        'n_contacts': ss.poisson(4), # Contacts Poisson distributed with a mean of 4
    }
    networks = ss.RandomNet(pars=network_pars)

    sir_pars = {
        'dur_inf': ss.normal(loc=10),  # Override the default distribution
    }
    sir = ss.SIR(sir_pars)


    WidgetPreview(SimWidget).run(
        set_people=ppl,
        set_networks=[(idx, network) for idx, network in enumerate([networks])],
        set_diseases=[(idx, disease) for idx, disease in enumerate([sir])]
    )