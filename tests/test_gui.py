import unittest
from unittest.mock import patch
from src.gui import validate_inputs
from tkinter import StringVar, Tk


class TestGUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    @patch("tkinter.messagebox.showerror")  # Mock the showerror function
    def test_validate_inputs_valid(self, mock_showerror):
        entry_vars = [
            StringVar(value="10"),  # N
            StringVar(value="5"),  # N_+
            StringVar(value="3"),  # q
            StringVar(value="0.5"),  # p
            StringVar(value="0.2"),  # f
            StringVar(value="1"),  # dx
        ]
        result = validate_inputs(entry_vars)
        self.assertTrue(result)
        mock_showerror.assert_not_called()

    @patch("tkinter.messagebox.showerror")
    def test_validate_inputs_invalid_negative_N(self, mock_showerror):
        entry_vars = [
            StringVar(value="-10"),  # N
            StringVar(value="5"),
            StringVar(value="3"),
            StringVar(value="0.5"),
            StringVar(value="0.2"),
            StringVar(value="1"),
        ]
        result = validate_inputs(entry_vars)
        self.assertFalse(result)
        mock_showerror.assert_called_once()

    @patch("tkinter.messagebox.showerror")
    def test_validate_inputs_invalid_large_p(self, mock_showerror):
        entry_vars = [
            StringVar(value="10"),  
            StringVar(value="5"),
            StringVar(value="3"),
            StringVar(value="1.5"),  # p (invalid, greater than 1)
            StringVar(value="0.2"),
            StringVar(value="1"),
        ]
        result = validate_inputs(entry_vars)
        self.assertFalse(result)
        mock_showerror.assert_called_once()

    @patch("tkinter.messagebox.showerror")
    def test_validate_inputs_invalid_negative_f(self, mock_showerror):
        entry_vars = [
            StringVar(value="10"),  # N
            StringVar(value="5"),
            StringVar(value="3"),
            StringVar(value="0.5"),
            StringVar(value="-0.1"),  # f (invalid, less than 0)
            StringVar(value="1"),
        ]
        result = validate_inputs(entry_vars)
        self.assertFalse(result)
        mock_showerror.assert_called_once()

    @patch("tkinter.messagebox.showerror")
    def test_validate_inputs_invalid_non_integer_N(self, mock_showerror):
        entry_vars = [
            StringVar(value="10.5"),  # N (invalid, not an integer)
            StringVar(value="5"),
            StringVar(value="3"),
            StringVar(value="0.5"),
            StringVar(value="0.2"),
            StringVar(value="1"),
        ]
        result = validate_inputs(entry_vars)
        self.assertFalse(result)
        mock_showerror.assert_called_once()

    @patch("tkinter.messagebox.showerror")
    def test_validate_inputs_invalid_empty_entry(self, mock_showerror):
        entry_vars = [
            StringVar(value=""),  # N (invalid, empty)
            StringVar(value="5"),
            StringVar(value="3"),
            StringVar(value="0.5"),
            StringVar(value="0.2"),
            StringVar(value="1"),
        ]
        result = validate_inputs(entry_vars)
        self.assertFalse(result)
        mock_showerror.assert_called_once()

if __name__ == "__main__":
    unittest.main()
