import logging
from datetime import datetime, timedelta

from odoo.tests.common import TransactionCase

_logger = logging.getLogger(__name__)


class TestEntitlementRegInfo(TransactionCase):
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

        self.entitlement = self.env["g2p.entitlement"].create(
            {
                "name": "Test Entitlement",
                "partner_id": self.partner.id,
                "program_id": self.program.id,
                "cycle_id": self.cycle.id,
                "initial_amount": 100,
            }
        )

        # Create necessary records before testing, if any

    def test_latest_registrant_info(self):
        # Create a test entitlement
        entitlement = self.env["g2p.entitlement"].create(
            {
                "name": "Test Entitlement",
                "partner_id": self.partner.id,
                "program_id": self.program.id,
                "cycle_id": self.cycle.id,
                "initial_amount": 100,
            }
        )

        # Create a test registrant_info
        registrant_info = self.env["g2p.program.registrant_info"].create({"entitlement_id": entitlement.id})

        # Trigger the compute method
        entitlement._compute_latest_registrant_info()

        # Assertions or verifications go here
        self.assertEqual(entitlement.latest_registrant_info.id, registrant_info.id, "Wrong Registrant Info")
        self.assertEqual(
            entitlement.latest_registrant_info_status,
            registrant_info.state,
            "Wrong Registrant Info Status",
        )
