import unittest

from detector import detect_pii, mask_pii


class TestPIIDetector(unittest.TestCase):

    def test_email_detection(self):
        text = "Email: priya@example.com"
        findings = detect_pii(text)

        self.assertTrue(
            any(item["type"] == "Email Address" for item in findings)
        )

    def test_phone_detection(self):
        text = "Phone: 9123456789"
        findings = detect_pii(text)

        self.assertTrue(
            any(item["type"] == "Phone Number" for item in findings)
        )

    def test_pin_detection(self):
        text = "PIN: 700002"
        findings = detect_pii(text)

        self.assertTrue(
            any(item["type"] == "Indian PIN Code" for item in findings)
        )

    def test_aadhaar_like_detection(self):
        text = "ID: 1234 5678 9012"
        findings = detect_pii(text)

        self.assertTrue(
            any(item["type"] == "Aadhaar-like Number" for item in findings)
        )

    def test_pan_like_detection(self):
        text = "PAN: ABCDE1234F"
        findings = detect_pii(text)

        self.assertTrue(
            any(item["type"] == "PAN-like Number" for item in findings)
        )

    def test_dob_detection(self):
        text = "DOB: 15/08/2005"
        findings = detect_pii(text)

        self.assertTrue(
            any(item["type"] == "Date of Birth" for item in findings)
        )

    def test_card_like_detection(self):
        text = "Card: 4532015112830366"
        findings = detect_pii(text)

        self.assertTrue(
            any(
                item["type"] == "Credit/Debit Card-like Number"
                for item in findings
            )
        )

    def test_email_masking(self):
        result = mask_pii("priya@example.com", "Email Address")
        self.assertEqual(result, "pr****@example.com")

    def test_phone_masking(self):
        result = mask_pii("9123456789", "Phone Number")
        self.assertEqual(result, "91XXXXXX89")

    def test_ordinary_number_not_pin(self):
        text = "Order reference: 845621"
        findings = detect_pii(text)

        self.assertFalse(
            any(item["type"] == "Indian PIN Code" for item in findings)
        )

    def test_invoice_number_not_phone(self):
        text = "Invoice number: 9123456789"
        findings = detect_pii(text)

        self.assertFalse(
            any(item["type"] == "Phone Number" for item in findings)
        )
    def test_customer_id_not_phone(self):
        text = "Customer ID: 9123456789"
        findings = detect_pii(text)

        self.assertFalse(
            any(item["type"] == "Phone Number" for item in findings)
        )

    def test_tracking_number_not_phone(self):
        text = "Tracking number: 9123456789"
        findings = detect_pii(text)

        self.assertFalse(
            any(item["type"] == "Phone Number" for item in findings)
        )
if __name__ == "__main__":
    unittest.main()