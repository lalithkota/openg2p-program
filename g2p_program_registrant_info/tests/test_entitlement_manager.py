from datetime import datetime, timedelta

from odoo.tests.common import TransactionCase


class TestDefaultEntitlementManagerRegInfo(TransactionCase):
    def setUp(self):
        super().setUp()
        self.program = self.env["g2p.program"].create({"name": "Test Program"})
        self.partner = self.env["res.partner"].create({"name": "Test Partner"})
        self.g2p_program_membership = self.env["g2p.program_membership"].create(
            {
                "name": "Test Membership",
                "partner_id": self.partner.id,
                "program_id": self.program.id,
            }
        )
        self.cycle = self.env["g2p.cycle"].create(
            {
                "name": "Test Cycle",
                "program_id": self.program.id,
                "sequence": 1,
                "start_date": datetime.now().strftime("%Y-%m-%d"),
                "end_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
            }
        )

    def test_prepare_entitlements(self):
        EntitlementManager = self.env["g2p.program.entitlement.manager.default"]
        RegistrantInfo = self.env["g2p.program.registrant_info"]

        # Create test data
        beneficiaries = [self.partner.id]

        # Call the method to be tested
        ents = EntitlementManager.prepare_entitlements(self.cycle, beneficiaries)

        # Perform assertions
        for ent in ents:
            self.assertTrue(ent, "Entitlements should not be empty")
            # Add more assertions as needed

        # Check if assign_reg_info_to_entitlement_from_membership was called
        # with the correct arguments
        self.assertTrue(
            RegistrantInfo.assign_reg_info_to_entitlement_from_membership.called,
            "assign_reg_info_to_entitlement_from_membership should be called",
        )

    def test_approve_entitlements(self):
        EntitlementManager = self.env["g2p.program.entitlement.manager.default"]
        RegistrantInfo = self.env["g2p.program.registrant_info"]

        # Create test data
        entitlements = self.env["g2p.entitlement"].create(
            {
                "name": "Test Entitlement",
                "partner_id": self.partner.id,
                "program_id": self.program.id,
                "cycle_id": self.cycle.id,
                "initial_amount": 100,
            }
        )

        # Call the method to be tested
        state_err, message = EntitlementManager.approve_entitlements(entitlements)

        # Perform assertions
        self.assertFalse(state_err, "State error should be False")
        self.assertEqual(message, "", "Message should be empty")

        # Check if trigger_latest_status_of_entitlement was called
        # with the correct arguments
        for rec in entitlements:
            RegistrantInfo.trigger_latest_status_of_entitlement.assert_called_with(
                rec, "completed", check_states=()
            )
