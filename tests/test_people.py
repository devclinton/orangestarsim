from unittest import TestCase

from Orange.widgets.tests.base import WidgetTest
from orangestarsim.people import PeopleWidget

class TestPeopleWidget(WidgetTest):
    def setUp(self):
        super().setUp()
        self.widget = self.create_widget(PeopleWidget)

    def test_init_simple(self):
        widget = self.widget
        self.assertEqual(widget.number_of_agents, 1000)
        self.assertIsNone(widget.age_data)

    def test_update_number_of_agents(self):
        widget = self.widget
        widget.number_of_agents = 500
        self.assertEqual(widget.number_of_agents, 500)
    
    # test our input signal for age data
    # def test_input_age_data(self):
    #     widget = self.widget
    #     self.send_signal(widget.Inputs.age_data, self.data)
    #     self.assertEqual(widget.age_data, self.data)