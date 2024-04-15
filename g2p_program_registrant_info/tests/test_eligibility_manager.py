from odoo.exceptions import UserError  # Import UserError for exception testing
from odoo.tests import TransactionCase


class TestDefaultEligibilityManager(TransactionCase):
    def setUp(self):
        super(TestDefaultEligibilityManager, self).setUp()

        # Create program and partner (assuming these exist)
        self.program = self.env["g2p.program"].create({"name": "Test Program"})
        self.partner = self.env["res.partner"].create({"name": "Test Partner"})

        # Create membership with draft state (new application)
        self.membership = self.env["g2p.program_membership"].create(
            {
                "program_id": self.program.id,
                "partner_id": self.partner.id,
                "state": "draft",
            }
        )

        # Create registrant info
        self.info = self.env["g2p.program.registrant_info"].create(
            {
                "program_membership_id": self.membership.id,
                "state": "active",
            }
        )

        # Create manager record
        self.manager = self.env["g2p.program_membership.manager.default"].create(
            {
                "name": "Test Manager Name",
                "program_id": self.program.id,
            }
        )

    def test_enroll_eligible_registrants(self):
        self.membership.state = "draft"
        self.manager.enroll_eligible_registrants(self.membership)
        self.assertEqual(self.membership.state, "enrolled")

        self.assertLogs(level="INFO", msg="your_expected_message")

    def test_enroll_non_eligible_registrants(self):
        # Simulate ineligibility check (replace with your actual logic)
        self.membership.state = "not_eligible"  # Set a flag or use a relevant field

        # Try enrolling (expect exception or specific behavior)
        with self.assertRaises(UserError):  # Expect UserError if enrollment fails
            self.manager.enroll_eligible_registrants(self.membership)

        # Assert expected outcome (membership not enrolled)
        self.assertNotEqual(self.membership.state, "enrolled")
