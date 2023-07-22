# View for CSV manipulation
# Aldo Siswanto
# 23/07/21

# Import Classes
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import threading


class View:
    # Constants
    VERSION = "0.0.1"
    APP_TITLE = "PLC Trace App"
    APP_SIZE = "800x400"

    def __init__(self, model):
        root = tk.Tk()
        root.title(View.APP_TITLE)
        root.geometry(View.APP_SIZE)

        MainFrame(root, model).pack(side='top')
        root.mainloop()


class StringVarModel(tk.StringVar):
    def __init__(self, model_var, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model_var = model_var

    def set(self, value: str) -> None:
        self.model_var = value
        super().set(value)

    def get(self) -> str:
        super().set(self.model_var)
        return super().get()


class MainFrame(tk.Frame):
    def __init__(self, parent, model):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.model = model

        self.source_file_frame = SourceFileFrame(self)
        self.analysis_file_frame = HistoryFileFrame(self)
        self.results_file_frame = ResultsFileFrame(self)
        self.execute_frame = ExecuteFrame(self)

        self.source_file_frame.pack(side='top')
        ttk.Separator(self, orient='horizontal').pack(side='top')

        self.analysis_file_frame.pack(side='top')
        ttk.Separator(self, orient='horizontal').pack(side='top')

        self.results_file_frame.pack(side='top')
        ttk.Separator(self, orient='horizontal').pack(side='top')

        self.execute_frame.pack(side='top')


class FileFrame(tk.Frame):
    def __init__(self, parent, config, model_filepath):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.config = config

        self.filepath_var = tk.StringVar(model_filepath)

        self.title = self.create_title()
        self.label = self.create_label()
        self.filepath_button = self.create_filepath_button()

        self.filepath_button.pack(side='left')
        self.title.pack(side='left')
        self.label.pack(side='left')

    def create_title(self):
        return ttk.Label(self, text=f'{self.config} filepath:')

    def create_label(self):
        return ttk.Label(self, textvariable=self.filepath_var)

    def create_filepath_button(self):
        return ttk.Button(self, text='Select filepath...', command=self.open_directory_selector)

    def open_directory_selector(self):
        filepath = filedialog.askdirectory()
        self.filepath_var.set(filepath)


class SourceFileFrame(FileFrame):
    def __init__(self, parent):
        super().__init__(parent, "SOURCE", parent.model.source_filepath)


class HistoryFileFrame(FileFrame):
    def __init__(self, parent):
        super().__init__(parent, "HISTORY", parent.model.history_filepath)


class ResultsFileFrame(FileFrame):
    def __init__(self, parent):
        super().__init__(parent, "RESULTS", parent.model.results_filepath)


class ExecuteFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.execute_button = self.create_execute_button()

        self.execute_button.pack(side='top')

    def create_execute_button(self):
        return ttk.Button(self, text='Execute')
