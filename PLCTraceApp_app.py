# App for PLCTraceApp
# Aldo Siswanto
# 23/07/21

from PLCTraceApp_view import View
from PLCTraceApp_model import Model
from PLCTraceApp_controller import Controller


class App:
    # Constants
    VERSION = "1.0.0"

    def __init__(self):
        self.model = self.initialize_model()
        self.controller = self.initialize_controller()
        self.view = self.initialize_view()

        # self.initialize_controller()

    def initialize_model(self):
        return Model()

    def initialize_controller(self):
        return Controller(self.model)

    def initialize_view(self):
        return View(self.model, self.controller)
