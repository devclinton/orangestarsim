from Orange.widgets.tests.base import WidgetTest

from orangestarsim.results import ResultsWidget

import starsim as ss

class TestResultsWidget(WidgetTest):

    def setUp(self):
        self.widget = self.create_widget(ResultsWidget)


    def test_init_simple(self):
        widget = self.widget
        self.assertEqual(widget.commitOnChange, 0)
        self.assertIsNone(widget._results)
        self.assertIsNone(widget.sim)

    # input signals from the simulation
    def test_input_sim(self):
        widget = self.widget
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
        
        self.send_signal(widget.Inputs.sim, tsim)
        self.assertIsNotNone(widget.sim)