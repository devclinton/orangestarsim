from Orange.widgets.widget import OWWidget
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.utils.signals import Input, Output
from orangewidget.utils.signals import summarize, PartialSummary
from Orange.data import Table

import starsim as ss


@summarize.register(ss.People)
def summarize_corpus(people: ss.People) -> PartialSummary:
    """
    Provides automated input and output summaries for Corpus
    """
    
    summary = f"{people}"
    return PartialSummary(summary, "People")

    

class PeopleWidget(OWWidget):
    name = "People"
    category = "StarSim"
    description = "Create a population of agents"
    icon = "icons/people.svg"
    priority = 1

    class Inputs:
        age_data = Input("Age data", Table)

    class Outputs:
        # Output will be the Starsim people object
        agents = Output("Agents", ss.People)

    number_of_agents = Setting(1000)

    # Automatically commit when the number of agents changes
    commitOnChange = Setting(0)

    def __init__(self):
        super().__init__()
        self.age_data = None
        self.people = None

        box = gui.widgetBox(self.controlArea, "Info")
        self.info_labels = []
        # Add the current number of agents selected
        self.info_labels.append(gui.label(box, self, f"Number of agents: {self.number_of_agents}"))
        # Info about our demographics data loaded from file
        self.info_labels.append(gui.label(box, self, "No data loaded"))

        gui.separator(self.controlArea)

        self.optionsBox = gui.widgetBox(self.controlArea, "Options")
        # Add The number of agents as a horizontal slider with a text box to manually enter the number of agents as well
        gui.hSlider(
            self.optionsBox, self, "number_of_agents", label="Number of agents", minValue=100, maxValue=1000000, step=1, callback=self.checkUpdate
        )
        # Add our checkbox for automatically committing when the number of agents changes
        gui.checkBox(
            self.optionsBox, self, "commitOnChange", "Commit data on selection change"
        )

        self.commit()

    @Inputs.age_data
    def set_age_data(self, data):
        self.age_data = data
        self.info_label.setText(f"Loaded data with {len(data)} rows")
        self.commit()

    def commit(self):
        self.info_labels[0].setText(f"Number of agents: {self.number_of_agents}")
        people = self.create_people()
        self.Outputs.agents.send(people)

    def create_people(self):
        if self.age_data is not None:
            people = ss.People(self.number_of_agents, self.age_data)
        else:
            people = ss.People(self.number_of_agents)
        return people
    
    def checkUpdate(self):
        if self.commitOnChange:
            self.commit()
    