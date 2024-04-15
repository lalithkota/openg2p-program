from datetime import datetime, timedelta

from odoo.exceptions import UserError
from odoo.tests import TransactionCase


class TestEntitlementManagerApproval(TransactionCase):
    def setUp(self):
        super().setUp()
        self.entitlement_manager = self.env["g2p.program.entitlement.manager.default"]
        self.program = self.env["g2p.program"].create({"name": "Test Program"})
        self.partner = self.env["res.partner"].create({"name": "Test Partner"})
        self.cycle = self.env["g2p.cycle"].create(
            {
                "name": "Test Cycle",
                "program_id": self.program.id,
                "sequence": 1,
                "start_date": datetime.now().strftime("%Y-%m-%d"),
                "end_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
            }
        )
        self.manager = self.entitlement_manager.create(
            {
                "program_id": self.program.id,
                "name": "Test Manager",
            }
        )

    def test_approve_entitlements_with_forbidden(self):
        # Create a test entitlement
        entitlement = self.env["g2p.entitlement"].create(
            {
                "name": "Test Entitlement",
                "program_id": self.program.id,
                "partner_id": self.partner.id,
                "initial_amount": 100,
                "cycle_id": self.cycle.id,
                "state": "draft",
            }
        )

        # Mock the approval_mapping_ids to raise Forbidden exception
        self.manager.approval_mapping_ids = []

        # Call the approve_entitlements method
        with self.assertRaises(UserError):
            self.manager.approve_entitlements(entitlement)

    def test_approve_entitlements_with_undefined(self):
        # Create a test entitlement
        entitlement = self.env["g2p.entitlement"].create(
            {
                "name": "Test Entitlement",
                "program_id": self.program.id,
                "partner_id": self.partner.id,
                "initial_amount": 100,
                "cycle_id": self.cycle.id,
                "state": "draft",
            }
        )

        # Mock the approval_mapping_ids to return a predefined mapping with undefined state
        self.manager.approval_mapping_ids = [(0, 0, {"state": "undefined"})]

        # Call the approve_entitlements method
        err_count, message = self.manager.approve_entitlements(entitlement)

        # Assert that the result is as expected
        self.assertEqual(err_count, 1)
        self.assertTrue(isinstance(message, str))

    def test_show_approve_entitlements(self):
        # Create a test entitlement
        entitlement = self.env["g2p.entitlement"].create(
            {
                "name": "Test Entitlement",
                "program_id": self.program.id,
                "partner_id": self.partner.id,
                "initial_amount": 100,
                "cycle_id": self.cycle.id,
                "state": "draft",
            }
        )

        # Mock the approval_mapping_ids to return a predefined mapping
        self.manager.approval_mapping_ids = [(0, 0, {"state": "approved"})]

        # Call the show_approve_entitlements method
        show_ent = self.manager.show_approve_entitlements(entitlement)

        # Assert that the result is as expected
        self.assertTrue(show_ent)
