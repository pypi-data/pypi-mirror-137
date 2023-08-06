import unittest
from io import StringIO
import sys
from sarcasticGD import sarcastic_gd

class TestStdOutMethods(unittest.TestCase):
    def test_sarcasm(self):
        """
        Tests whether the decarator introduces sufficient sarcasm
        """
        @sarcastic_gd.sarcastic_gd
        def train():
            # Dummy SGD training function
            print("hello")
            pass

        captured_output = StringIO()
        sys.stdout = captured_output
        train()
        sys.stdout = sys.__stdout__
        self.assertTrue(len(captured_output.getvalue()) > 0)

if __name__ == "__main__":
    unittest.main()


