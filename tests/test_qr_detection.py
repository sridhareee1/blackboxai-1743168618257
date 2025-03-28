import unittest
import os
import time
from qr_nlp.qr_detector import read_qr_from_image, generate_qr_code
from qr_nlp.exceptions import QRDetectionError

class TestQRDetection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a test QR code
        cls.test_text = "https://example.com"
        cls.test_qr_path = "test_qr.png"
        generate_qr_code(cls.test_text, cls.test_qr_path)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_qr_path):
            os.remove(cls.test_qr_path)

    def test_read_valid_qr(self):
        result = read_qr_from_image(self.test_qr_path)
        self.assertEqual(result, self.test_text)

    def test_read_invalid_file(self):
        with self.assertRaises(QRDetectionError):
            read_qr_from_image("nonexistent.png")

if __name__ == '__main__':
    unittest.main()