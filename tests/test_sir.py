from Orange.widgets.tests.base import WidgetTest
from orangestarsim.diseases.sir import SIRWidget
import starsim as ss

class TestSIRWidget(WidgetTest):

    def setUp(self):
        self.widget = self.create_widget(SIRWidget)

    def test_init_simple(self):
        widget = self.widget
        self.assertEqual(widget.beta, 0.1)
        self.assertIsNone(widget.init_prev)
        self.assertIsNone(widget.dur_inf)
        self.assertIsNone(widget.p_death)

    def test_update_beta(self):
        widget = self.widget
        widget.beta = 0.2
        self.assertEqual(widget.beta, 0.2)
    
    # test our input signal for initial prevalence
    def test_input_init_prev(self):
        widget = self.widget
        self.send_signal(widget.Inputs.init_prev, ss.bernoulli(p=0.05))
        self.assertEqual(widget.init_prev.pars.p, 0.05)