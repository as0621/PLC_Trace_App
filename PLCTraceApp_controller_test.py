import unittest
from PLCTraceApp_controller import Controller
from PLCTraceApp_model import Model


class MyTestCase(unittest.TestCase):
    def testProcessSource(self):
        model = Model()
        model.source_filepath = r"C:\Users\as0621\OneDrive - Dexcom\Projects\SW Projects\230721 Kevin App\source\Ax_High_1.CSV".replace('\\', '/')
        model.results_filepath = r"C:\Users\as0621\OneDrive - Dexcom\Projects\SW Projects\230721 Kevin App\Ax_High_Analysis.xlsx".replace('\\', '/')
        model.history_filepath = r"C:\Users\as0621\OneDrive - Dexcom\Projects\SW Projects\230721 Kevin App\Ax_High_Historical.csv".replace('\\', '/')
        controller = Controller(model)
        controller.process_data()


if __name__ == '__main__':
    unittest.main()
