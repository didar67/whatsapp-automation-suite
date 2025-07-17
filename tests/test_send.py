import unittest
from unittest.mock import patch, MagicMock
import send_whatsapp_msg as script 

class TestAutomation(unittest.TestCase):

    @patch("fallback_pywhatkit.send_via_pywhatkit")
    def test_fallback_send(self, mock_send):
        script.logger = MagicMock()
        mock_send.return_value = None
        mock_send("+8801XXXX", "Hello", {}, dry_run=True)
        mock_send.assert_called_once()

if __name__ == "__main__":
    unittest.main()