from Orange.widgets.tests.base import WidgetTest

from orangestarsim.network import RandomNetworkWidget

class TestRandomNetworkWidget(WidgetTest):

    def setUp(self):
        self.widget = self.create_widget(RandomNetworkWidget)

    def test_init_simple(self):
        widget = self.widget
        self.assertEqual(widget.n_contacts, 10)
        self.assertEqual(widget.dur, 0)
        self.assertIsNone(widget.contact_dist)