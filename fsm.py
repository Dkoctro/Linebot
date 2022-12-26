from transitions.extensions import GraphMachine
# import scrapy
from linebot.models import *
from ability import Project, fun, trivia, subject
# from fsm import TocMachine


person = Project()

class TocMachine(GraphMachine):
        def __init__(self, **machine_configs):
            self.machine = GraphMachine(model = self, **machine_configs)
        def is_going_to_name(self, event):
            text = event.message.text
            return text.lower() == "go to name"
        def is_going_to_lucky(self, event):
            text = event.message.text
            return text.lower() == "go to lucky"
        def is_going_to_relax(self, event):
            text = event.message.text
            return text.lower() in fun
        def is_going_to_trivia(self, event):
            text = event.message.text
            return text.lower() in trivia
        def is_going_to_study(self, event):
            text = event.message.text
            return text.lower() == "go to study"
        def is_going_to_subject(self, event):
            text = event.message.text
            return text.lower() in subject
