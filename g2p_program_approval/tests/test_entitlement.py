from datetime import datetime, timedelta

from odoo.exceptions import UserError
from odoo.tests import common

from odoo.addons.g2p_programs.models import constants


class TestG2PApprovalEntitlement(common.TransactionCase):
    def setUp(self):
        super(TestG2PApprovalEntitlement, self).setUp()
        self.entitlement_model = self.env["g2p.entitlement"]
        self.program_model = self.env["g2p.program"]
        self.partner_model = self.env["res.partner"]
        self.cycle_model = self.env["g2p.cycle"]

    def test_compute_show_approve_button_with_false_ent_manager(self):
        # Create a sample program
        program = self.program_model.create({"name": "Test Program"})

        # Create a sample partner
        partner = self.partner_model.create({"name": "Test Partner"})

        # Create a sample cycle with a program and start_date
        cycle = self.cycle_model.create(
            {
                "name": "Test Cycle",
                "program_id": program.id,
                "start_date": datetime.now(),
                "end_date": datetime.now() + timedelta(days=30),
            }
        )

        # Create a sample entitlement with a partner, cycle, and program
        entitlement = self.entitlement_model.create(
            {
                "name": "Test Entitlement",
                "program_id": program.id,
                "partner_id": partner.id,
                "initial_amount": 100,
                "cycle_id": cycle.id,
            }
        )

        # Mock the get_manager method to return a manager
        def mock_get_manager(manager_type):
            return self.env["res.users"].create({"name": "Entitlement Manager"})

        program.get_manager = mock_get_manager

        # Set up the manager to not show the approve button
        program.get_manager(constants.MANAGER_ENTITLEMENT).show_approve_entitlements = lambda x: False

        # Trigger the computation of show_approve_button
        entitlement._compute_show_approve_button()

        # Assert that show_approve_button is False
        self.assertFalse(entitlement.show_approve_button)

    def test_compute_show_approve_button_without_ent_manager(self):
        # Create a sample partner
        partner = self.partner_model.create({"name": "Test Partner"})

        # Create a sample program
        program = self.program_model.create({"name": "Test Program"})

        # Create a sample cycle with a program and start_date
        cycle = self.cycle_model.create(
            {
                "name": "Test Cycle",
                "program_id": program.id,
                "start_date": datetime.now(),
                "end_date": datetime.now() + timedelta(days=30),
            }
        )

        # Create a sample entitlement with a partner and cycle
        entitlement = self.entitlement_model.create(
            {
                "name": "Test Entitlement",
                "partner_id": partner.id,
                "initial_amount": 100,
                "cycle_id": cycle.id,
            }
        )

        # Trigger the computation of show_approve_button
        with self.assertRaises(UserError):
            entitlement._compute_show_approve_button()
