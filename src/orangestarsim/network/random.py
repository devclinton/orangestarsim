from Orange.widgets.widget import OWWidget
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.utils.signals import Input, Output
from orangewidget.utils.signals import summarize, PartialSummary
from Orange.data import Table

import starsim as ss


@summarize.register(ss.Network)
def summarize_corpus(network: ss.Network) -> PartialSummary:
    """
    Provides automated input and output summaries for Corpus
    """
    
    summary = f"{network}"
    return PartialSummary(summary, "Network")

    

# class StarSimNetworkWidgetBase(OWWidget):
#     name = "Network"
#     category = "StarSim"
#     description = "Network"
#     icon = "icons/people.png"
#     priority = 1

#     _network = None

#     class Outputs:
#         # Output will be the Starsim Network object
#         network = Output("Network", ss.Network)

#     label = Setting("Network")



class RandomNetworkWidget(OWWidget):
    name = "Random Network"
    description = "Create a random network"
    icon = "../icons/random_network.svg"
    category = "StarSim"
    priority = 1

    def __init__(self):
        super().__init__()

    class Outputs:
        network = Output("Network", ss.RandomNet)
    
    n_contacts = Setting(10)
    dur = Setting(0)

    commitOnChange = Setting(0)

    def __init__(self):
        super().__init__()

        self.contact_dist = None
        self.prenatal = None
        self.postnal = None

        box = gui.widgetBox(self.controlArea, "Info")
        self.info_labels = []
        # Add the current number of agents selected
        self.info_labels.append(gui.label(box, self, f"Number of contacts: {self.n_contacts}"))
        # Info about our demographics data loaded from file
        self.info_labels.append(gui.label(box, self, "No data loaded"))

        gui.separator(self.controlArea)

        self.optionsBox = gui.widgetBox(self.controlArea, "Options")
        # Add The number of agents as a horizontal slider with a text box to manually enter the number of agents as well
        gui.hSlider(
            self.optionsBox, self, "n_contacts", label="Number of contacts", minValue=1, maxValue=100, step=1, callback=self.checkUpdate
        )
        gui.hSlider(
            self.optionsBox, self, "dur", label="Duration", minValue=0, maxValue=100, step=1, callback=self.checkUpdate
        )
        self.commit()

    def checkUpdate(self):
        if self.commitOnChange:
            self.commit()

    def commit(self):
        # build our parameters dict so the last step will build the the RandomNet object
        pars = {
            "n_contacts": self.n_contacts,
            "dur": self.dur
        }
        self.network = ss.RandomNet(pars)
        self.Outputs.network.send(self.network)



if __name__ == "__main__":
    from Orange.widgets.utils.widgetpreview import WidgetPreview
    WidgetPreview(RandomNetworkWidget).run(
    )