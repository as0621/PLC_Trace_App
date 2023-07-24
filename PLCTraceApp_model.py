# Model for PLCTraceApp
# Aldo Siswanto
# 2023/07/08

class Model:
    VERSION = "1.0.0"

    def __init__(self):
        self.source_filepath = str('hi')
        self.history_filepath = str()
        self.results_filepath = str()
        self.status = str()
