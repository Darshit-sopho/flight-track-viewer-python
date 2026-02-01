import sys
import os
import unittest
from unittest.mock import MagicMock, patch
import pandas as pd  # Added pandas to create real dataframes for testing

# --- PATH SETUP ---
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, '..', 'src')
sys.path.insert(0, src_path)
# ------------------

from PyQt6.QtWidgets import QApplication, QFileDialog

# Ensure one QApplication exists
app = QApplication.instance() or QApplication(sys.argv)

from ftv.ui import FlightTrackViewerUI

class TestFlightTrackViewerUI(unittest.TestCase):

    def setUp(self):
        """Runs before every test."""
        self.window = FlightTrackViewerUI()
        # FIX FOR ERROR #2: The window must be shown for isVisible() checks to work
        self.window.show() 

    def tearDown(self):
        """Runs after every test."""
        self.window.close()

    def test_initial_state(self):
        """Test the UI starts in the correct default state."""
        self.assertEqual(self.window.windowTitle(), "Flight Track Viewer")
        self.assertFalse(self.window.process_btn.isEnabled())
        self.assertIn("No file selected", self.window.file_path_label.text())

    @patch.object(QFileDialog, 'getOpenFileName')
    def test_browse_file_selection(self, mock_dialog):
        """Test that the Browse button updates the UI correctly."""
        mock_dialog.return_value = ('/path/to/test_flight.csv', 'CSV Files (*.csv)')
        
        self.window.browse_file()
        
        self.assertEqual(self.window.csv_file, '/path/to/test_flight.csv')
        self.assertIn("test_flight.csv", self.window.file_path_label.text())
        self.assertTrue(self.window.process_btn.isEnabled())

    @patch('ftv.ui.FlightProcessingThread')
    def test_process_button_triggers_thread(self, mock_thread_class):
        """Test that clicking 'Process' starts the background thread."""
        self.window.csv_file = "/path/to/fake.csv"
        self.window.process_btn.setEnabled(True)
        
        # Mock the thread instance
        mock_thread_instance = MagicMock()
        mock_thread_class.return_value = mock_thread_instance
        
        self.window.process_flight()
        
        self.assertFalse(self.window.process_btn.isEnabled())
        # This should now pass because we called self.window.show() in setUp
        self.assertTrue(self.window.progress_bar.isVisible())
        mock_thread_instance.start.assert_called_once()

    def test_display_results_no_crash(self):
        """Test that display_results handles data gracefully."""
        dummy_result = {
            'data': {}, 
            'outputs': {'video': 'test.mp4'}
        }
        
        # FIX FOR ERROR #1: Use a real DataFrame instead of a Mock
        # This prevents crashes when the UI code calls .max() or .mean()
        real_df = pd.DataFrame({
            'Latitude': [10.0, 11.0],
            'Longitude': [20.0, 21.0],
            'Altitude': [1000, 2000],
            'Speed': [150, 160],
            'Callsign': ['TEST1234', 'TEST1234']
        })

        with patch('pandas.read_csv') as mock_read_csv:
            mock_read_csv.return_value = real_df
            
            try:
                self.window.display_results(dummy_result)
            except Exception as e:
                self.fail(f"display_results crashed with error: {e}")
            
            # Verify the UI updated successfully
            info_text = self.window.info_text.toPlainText()
            self.assertIn("Flight Data Summary", info_text)
            self.assertIn("TEST1234", info_text)

if __name__ == '__main__':
    unittest.main()