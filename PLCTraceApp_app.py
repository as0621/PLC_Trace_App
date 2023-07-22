# App for PLCTraceApp
# Aldo Siswanto
# 23/07/21

from PLCTraceApp_view import View
from PLCTraceApp_model import Model


class App:
    # Constants
    VERSION = "0.0.1"

    def __init__(self):
        self.model = self.initialize_model()
        self.controller = None
        self.view = self.initialize_view()

        # self.initialize_controller()

    def initialize_model(self):
        return Model()

    def initialize_view(self):
        return View(self.model)
