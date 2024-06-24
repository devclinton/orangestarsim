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

    

class SIRWidget(OWWidget):
    name = "SIR"
    category = "StarSim"
    description = "SIR"
    icon = "../icons/sir.svg"
    priority = 1

    _network = None


    class Inputs:
        init_prev = Input("Initial Prevalence", ss.Dist)
        dur_inf = Input("Duration of Infection", ss.Dist)
        p_death = Input("Probability of Death", ss.Dist)

    class Outputs:
        # Output will be the Starsim Network object
        sir = Output("sir", ss.SIR)

    
    beta = Setting(0.1)

    commitOnChange = Setting(0)

    def __init__(self):
        super().__init__()

        self.init_prev = None
        self.dur_inf = None
        self.p_death = None

        self.sir = None

        box = gui.widgetBox(self.controlArea, "Info")
        self.info_labels = []
        self.info_labels.append(gui.label(box, self, f"beta: {self.beta}"))

        gui.separator(self.controlArea)

        self.optionsBox = gui.widgetBox(self.controlArea, "Options")
        # use spinner for beta since it is a float
        gui.doubleSpin(
            self.optionsBox, self, "beta", 0, 1, 0.01, label="Beta:", callback=self.updateIfCommit
        )
        gui.checkBox(
            self.optionsBox, self, "commitOnChange", "Commit on change"
        )
        self.commit()

    @Inputs.init_prev
    def set_init_prev(self, init_prev):
        self.init_prev = init_prev
        self.commit()

    @Inputs.dur_inf
    def set_dur_inf(self, dur_inf):
        self.dur_inf = dur_inf
        self.commit()

    @Inputs.p_death
    def set_p_death(self, p_death):
        self.p_death = p_death
        self.commit()

    def updateIfCommit(self):
        if self.commitOnChange:
            self.commit()

    def commit(self):
        pars = {
        }
        # everything is optional so only add ones with values in a for loop
        for name in ['init_prev', 'dur_inf', 'p_death']:
            if getattr(self, name) is not None:
                pars[name] = getattr(self, name)

        result = ss.SIR(pars)
        self.Outputs.sir.send(result)
    


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


    WidgetPreview(SIRWidget).run(
        set_dur_inf=ss.normal(loc=10),
    )