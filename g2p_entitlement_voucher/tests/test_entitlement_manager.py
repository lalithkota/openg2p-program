from datetime import datetime, timedelta
from unittest.mock import patch

from odoo import _
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestG2PVoucherEntitlementManager(TransactionCase):
    def setUp(self):
        super().setUp()
        self.program = self.env["g2p.program"].create({"name": "Test Program"})
        self.partner = self.env["res.partner"].create({"name": "Test Partner"})
        self.cycle = self.env["g2p.cycle"].create(
            {
                "name": "Test Cycle",
                "program_id": self.program.id,
                "start_date": datetime.now(),
                "end_date": datetime.now() + timedelta(days=30),
            }
        )
        self.entitlement = self.env["g2p.entitlement"].create(
            {
                "program_id": self.program.id,
                "partner_id": self.partner.id,
                "cycle_id": self.cycle.id,
                "state": "approved",
                "initial_amount": 100,
            }
        )
        self.storage_backend = self.env["storage.backend"].create(
            {
                "name": "Test Document Store",
            }
        )
        self.manager = self.env["g2p.program.entitlement.manager.voucher"].create(
            {
                "name": "Test voucher manager",
                "program_id": self.program.id,
                "voucher_document_store": self.storage_backend.id,
                "auto_generate_voucher_on_approval": True,
            }
        )

    def test_selection_manager_ref_id(self):
        # Ensure that the new manager is added to the selection
        entitlement_manager = self.env["g2p.program.entitlement.manager"]
        selection = entitlement_manager._selection_manager_ref_id()

        # Check if the new manager ("g2p.program.entitlement.manager.voucher", "Voucher") is present
        self.assertIn(("g2p.program.entitlement.manager.voucher", "Voucher"), selection)

    def test_open_voucher_config_form(self):
        # Create a test record for G2PVoucherEntitlementManager
        manager = self.manager

        # Set voucher_file_config
        payment_file_config = self.env["g2p.payment.file.config"].create({})
        manager.voucher_file_config = payment_file_config

        # Call the open_voucher_config_form method
        action = manager.open_voucher_config_form()

        # Assert that the action returned is as expected
        self.assertTrue(action.get("res_model") == "g2p.payment.file.config")
        self.assertTrue(action.get("view_mode") == "form")
        self.assertTrue(action.get("target") == "new")

    def test_generate_vouchers(self):
        # Create a test record for G2PVoucherEntitlementManager
        manager = self.manager

        # Set voucher_file_config
        payment_file_config = self.env["g2p.payment.file.config"].create({})
        manager.voucher_file_config = payment_file_config

        # Call the generate_vouchers method
        err_count, message, sticky, vouchers = manager.generate_vouchers()

        # Assert that the result is as expected
        self.assertEqual(err_count, 0)
        self.assertTrue(isinstance(message, str))
        self.assertFalse(sticky)

    def test_generate_vouchers_async(self):
        # Create a test record for G2PVoucherEntitlementManager
        manager = self.manager

        # Create a test record for cycle
        cycle = self.cycle

        # Create a test record for entitlements
        entitlements = self.entitlement

        # Call the generate_vouchers_async method
        manager._generate_vouchers_async(cycle, entitlements, len(entitlements))

        # Assert that the cycle has been updated
        self.assertTrue(cycle.locked)
        self.assertEqual(cycle.locked_reason, _("Generate vouchers for entitlements in cycle."))

    def test_get_encryption_provider(self):
        # Test case where encryption_provider_id is set
        provider = self.env["g2p.encryption.provider"].create(
            {
                "name": "Test Encryption Provider",
            }
        )
        self.manager.encryption_provider_id = provider
        prov = self.manager.get_encryption_provider()
        self.assertEqual(prov, provider)

        # Test case where encryption_provider_id is not set
        self.manager.encryption_provider_id = False
        prov = self.manager.get_encryption_provider()
        self.assertTrue(prov)

    def test_approve_entitlements_with_auto_generate_voucher(self):
        # Create test entitlements in the 'pending validation' state
        entitlements = self.env["g2p.entitlement"].create(
            {
                "program_id": self.program.id,
                "partner_id": self.partner.id,
                "cycle_id": self.cycle.id,
                "state": "pending_validation",
                "initial_amount": 100,  # Adjust the initial_amount as needed
            }
        )

        # Ensure that the program has sufficient funds available
        self.env[
            "g2p.program.fund"
        ].amount = 200  # Set the available funds to an amount that covers the entitlements

        # Set auto_generate_voucher_on_approval to True
        self.manager.auto_generate_voucher_on_approval = True

        # Mock the generate_vouchers method to avoid actual voucher generation
        with patch(
            "odoo.addons.g2p_entitlement_voucher.models.entitlement_manager.G2PVoucherEntitlementManager.generate_vouchers"
        ) as mock_generate_vouchers:
            # Mock the return value of generate_vouchers
            mock_generate_vouchers.return_value = (0, "Test message", False, [])

            # Call the approve_entitlements method
            result = self.manager.approve_entitlements(entitlements)

            # Assert that the result is as expected
            self.assertIsNone(result, "Approval result should be None")

            # Assert that generate_vouchers was called
            mock_generate_vouchers.assert_called_once_with(entitlements)
