# Model for PLCTraceApp
# Aldo Siswanto
# 2023/07/08

import tkinter as tk


class Model:
    VERSION = "0.0.1"

    def __init__(self):
        self.source_filepath = str()
        self.history_filepath = str()
        self.results_filepath = str()
