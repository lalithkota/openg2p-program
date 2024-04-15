import random
from datetime import datetime

from odoo.tests.common import TransactionCase


class TestG2PProgramRegistrantInfo(TransactionCase):
    def setUp(self):
        super().setUp()
        self.program = self.env["g2p.program"].create({"name": "Test Program"})
        self.partner = self.env["res.partner"].create({"name": "Test Partner"})

    def test_compute_sl_no(self):
        reg_info = self.env["g2p.program.registrant_info"].create(
            {"registrant_id": self.partner.id, "program_id": self.program.id}
        )
        self.assertEqual(reg_info.sl_no, 1)

    def test_compute_application_id(self):
        reg_info = self.env["g2p.program.registrant_info"].create(
            {"registrant_id": self.partner.id, "program_id": self.program.id}
        )
        d = datetime.today().strftime("%d")
        m = datetime.today().strftime("%m")
        y = datetime.today().strftime("%y")
        random_number = str(random.randint(1, 100000))
        expected_application_id = d + m + y + random_number.zfill(5)
        self.assertEqual(reg_info.application_id, expected_application_id)

    def test_open_registrant_form(self):
        reg_info = self.env["g2p.program.registrant_info"].create(
            {"registrant_id": self.partner.id, "program_id": self.program.id}
        )
        action = reg_info.open_registrant_form()
        self.assertEqual(action["name"], "Program Registrant Info")
        self.assertEqual(action["view_mode"], "form")
        self.assertEqual(action["res_model"], "g2p.program.registrant_info")
        self.assertEqual(action["res_id"], reg_info.id)
        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["target"], "new")
        self.assertEqual(
            action["view_id"],
            self.env.ref("g2p_program_registrant_info.view_program_registrant_info_form").id,
        )

    def test_trigger_latest_status_of_entitlement(self):
        # Write test cases for trigger_latest_status_of_entitlement method
        pass

    def test_trigger_latest_status_membership(self):
        # Write test cases for trigger_latest_status_membership method
        pass

    def test_assign_reg_info_to_entitlement_from_membership(self):
        # Write test cases for assign_reg_info_to_entitlement_from_membership method
        pass

    def test_reject_entitlement_for_membership(self):
        # Write test cases for reject_entitlement_for_membership method
        pass

    def test_open_new_tab(self):
        # Write test cases for open_new_tab method
        pass
