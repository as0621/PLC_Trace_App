# Controller for PLCTraceApp
# Aldo Siswanto
# 2023/07/08

import pandas as pd
from win32com import client
import os


class Controller:
    VERSION = "0.0.1"
    SOURCE_COLUMNS = ['Header',
                      'Date',
                      'Time',
                      'Sensor1',
                      'Timer1',
                      'Sensor2',
                      'Timer2',
                      'Sensor3',
                      'Timer3',
                      'Sensor4',
                      'Timer4']
    SOURCE_SENSOR_COL_NAMES = ['Sensor1', 'Sensor2', 'Sensor3', 'Sensor4']
    SOURCE_TIMER_COL_NAMES = ['Timer1', 'Timer2', 'Timer3', 'Timer4']
    SOURCE_DATA_COLUMNS_INDEX = 3
    SOURCE_SKIPROW = 13
    SOURCE_BINS = [10, 20, 30, 40, 50, 100, 200, 300, 400, 500, 1000, 2000, 3000, 4000, 6000, 8000, float('inf')]
    RESULTS_SHEETNAME = 'Summary'

    def __init__(self, model):
        self.model = model
        self.source_filepath = model.source_filepath
        self.history_filepath = model.history_filepath
        self.results_filepath = model.results_filepath

    def process_data(self):
        history_df = self.history_load()

        if not history_df['Files'].str.contains(self.source_filepath):
            new_df = self.process_sourcepath()
            self.process_resultspath(new_df)
            self.history_update(history_df, self.source_filepath)
        else:
            raise Exception("File has been previously processed")

    def history_load(self):
        return pd.read_csv(self.history_filepath)
    def history_update(self, history_df, new_filepath):
        head, tail = os.path.split(new_filepath)

        history_df.loc[len(history_df.index)] = tail
        history_df.to_csv(self.history_filepath, index=False)

    def process_resultspath(self, new_df):
        appended_df = self.results_append_df(self.results_filepath, new_df)
        self.results_write_excel(self.results_filepath, Controller.RESULTS_SHEETNAME, appended_df)

    def results_append_df(self, results_filepath, new_df):
        old_df = pd.read_excel(results_filepath, sheet_name=Controller.RESULTS_SHEETNAME, index_col=0)

        # Improvement: new method of matching indexes
        old_df.index = new_df.index

        old_df = old_df.add(new_df)

        return old_df

    def results_write_excel(self, filename, sheetname, df):
        df.to_clipboard(index=True, header=True)

        excel_app = client.gencache.EnsureDispatch("Excel.Application")  # Initialize instance
        # excel_app = client.Dispatch("Excel.Application")
        # excel_app.Visible = False
        wb = excel_app.Workbooks.Open(
            r'C:\Users\as0621\OneDrive - Dexcom\Projects\SW Projects\230721 Kevin App\Ax_High_Analysis.xlsx')  # Load your (formatted) template workbook
        ws = wb.Worksheets(sheetname)  # First worksheet becomes active - you could also refer to a sheet by name
        ws.Application.Goto(ws.Range("A1"),
                            True)  # Only select a single cell using Excel nomenclature, otherwise this breaks
        ws.PasteSpecial(Format='Unicode Text')  # Paste as text
        wb.Save()  # Save our work
        excel_app.Quit()  # End the Excel instance

    def process_sourcepath(self):
        df_summary = pd.DataFrame()

        temp_df = self.sourcepath_load(self.source_filepath)

        for col_name in Controller.SOURCE_COLUMNS[Controller.SOURCE_DATA_COLUMNS_INDEX:]:
            df_summary = self.sourcepath_add_col(temp_df, col_name, df_summary)

        self.sourcepath_add_totals(df_summary)

        return df_summary

    def sourcepath_load(self, filepath):
        temp_df = pd.read_csv(filepath, skiprows=Controller.SOURCE_SKIPROW)
        temp_df.columns = Controller.SOURCE_COLUMNS
        return temp_df

    def sourcepath_add_col(self, source_df, col_name, output_df):
        # checking if row changes from the previous row
        temp_df = source_df[col_name].ne(source_df[col_name].shift()).cumsum()

        # take portions of when the original bit turns 1 only
        temp_df = temp_df[source_df[col_name].eq(1)]

        # groupby
        temp_df = temp_df.groupby(temp_df).count()
        temp_df = temp_df[temp_df > 1].reset_index(drop=True)

        # Binning
        bins = pd.cut(x=temp_df, bins=Controller.SOURCE_BINS)
        temp_df = pd.concat([temp_df, bins], axis=1)
        temp_df.columns = [col_name, 'bins']

        # Summary
        temp_df = temp_df.groupby('bins').count()

        # Concat to mastertable
        output_df = pd.concat([output_df, temp_df], axis=1)

        return output_df

    def sourcepath_add_totals(self, df):
        df['Sensor_Total'] = df[Controller.SOURCE_SENSOR_COL_NAMES].sum(axis=1)
        df['Timer_Total'] = df[Controller.SOURCE_TIMER_COL_NAMES].sum(axis=1)
