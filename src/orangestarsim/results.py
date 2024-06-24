
from Orange.widgets.widget import OWWidget
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.utils.signals import Input, Output
from orangewidget.utils.signals import summarize, PartialSummary
from Orange.data import Domain, DiscreteVariable, ContinuousVariable, Table, StringVariable, TimeVariable
import numpy as np

import starsim as ss




class ResultsWidget(OWWidget):
    name = "Results"
    category = "StarSim"
    description = "Results"
    icon = "icons/results.svg"
    priority = 1


    class Inputs:
        sim = Input("Sim", ss.Sim)

    class Outputs:
        # Output will be the Starsim Network object
        results = Output("Results", ss.Results)
        result_table = Output("Results Table", Table)

    
    label = Setting("Results")

    commitOnChange = Setting(0)


    # Cache of results
    _results  = None

    
    def __init__(self):
        super().__init__()

        self.sim = None

        box = gui.widgetBox(self.controlArea, "Info")
        self.info_labels = []
        self.info_labels.append(gui.label(box, self, f"Results"))
        
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

        self.commitOnChange = 1
        self.commit()

    @Inputs.sim
    def set_sim(self, sim):
        self.sim = sim
        self._results = None
        self.commit()

    def commit(self):
        if self.sim is not None:
            # TODO check if sim has already ran
            if self._results is None:
                self.sim.run()
                self._results = self.sim.results
            result_table = self.convert_results_to_table(self.sim, self._results)
            self.Outputs.result_table.send(result_table)
            self.Outputs.results.send(self._results)
        else:
            self.Outputs.results.send(None)
            self.Outputs.result_table.send(None)


    @classmethod
    def convert_results_to_table(cls, sim, results):
        # convert the starsim np Results arrays to an Orange Table
        # define our domain here
        domain_vars = [
            # Add Time first from the yearvec
            ContinuousVariable.make("year")
        ]
        values = [
            sim.yearvec
        ]
        for disease in results.keys():
            # check to see if the item itself is a subresult
            if isinstance(results[disease], ss.Results):
                for key in results[disease].dict_keys():
                    # TODO Handle bool fields as Discrete Variables
                    # Add the counter vars as discreet variables
                    if key.startswith("n_"):
                        domain_vars.append(ContinuousVariable.make(f"{disease}.{key}"))
                    # Add the rest as continuous variables
                    else:
                        domain_vars.append(ContinuousVariable.make(f"{disease}.{key}" ))
                    values.append(results[disease][key])
            else:
                domain_vars.append(ContinuousVariable.make(f"{disease}"))
                values.append(results[disease])
        domain = Domain(domain_vars)
        # now combine the values into a table
        table = Table.from_numpy(domain, np.vstack(values).T)
        return table

    def updateIfChange(self):
        if self.commitOnChange:
            self.commit()


if __name__ == "__main__":
    from Orange.widgets.utils.widgetpreview import WidgetPreview
    # setup sim to test widget with initial signals
    ppl = ss.People(100)
    network_pars = {
        'n_contacts': ss.poisson(4), # Contacts Poisson distributed with a mean of 4
    }
    networks = ss.RandomNet(pars=network_pars)

    sir_pars = {
        'dur_inf': ss.normal(loc=10),  # Override the default distribution
    }
    sir = ss.SIR(sir_pars)

    # Change pars after creating the SIR instance
    sir.pars.beta = {'random': 0.1}

    # You can also change the parameters of the default lognormal distribution directly
    sir.pars.dur_inf.set(loc=5)

    # Or use a function, here a lambda that makes the mean for each agent equal to their age divided by 10
    sir.pars.dur_inf.set(loc = lambda self, sim, uids: sim.people.age[uids] / 10)

    tsim = ss.Sim(people=ppl, diseases=sir, networks=networks)
    WidgetPreview(ResultsWidget).run(
        set_sim=tsim
    )