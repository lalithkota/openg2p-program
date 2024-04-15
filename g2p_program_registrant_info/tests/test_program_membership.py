from odoo.tests.common import TransactionCase


class TestG2PProgramMembership(TransactionCase):
    def setUp(self):
        super().setUp()
        self.program = self.env["g2p.program"].create({"name": "Test Program"})
        self.partner = self.env["res.partner"].create({"name": "Test Partner"})
        self.membership = self.env["g2p.program_membership"].create(
            {"partner_id": self.partner.id, "program_id": self.program.id}
        )

    def test_compute_latest_registrant_info(self):
        reg_info_1 = self.env["g2p.program.registrant_info"].create(
            {"registrant_id": self.partner.id, "program_id": self.program.id}
        )
        reg_info_2 = self.env["g2p.program.registrant_info"].create(
            {"registrant_id": self.partner.id, "program_id": self.program.id}
        )
        self.assertEqual(self.membership.latest_registrant_info, reg_info_2)

    def test_onchange_program_registrant_info(self):
        reg_info_1 = self.env["g2p.program.registrant_info"].create(
            {"registrant_id": self.partner.id, "program_id": self.program.id}
        )
        reg_info_2 = self.env["g2p.program.registrant_info"].create(
            {"registrant_id": self.partner.id, "program_id": self.program.id}
        )
        self.assertEqual(reg_info_1.program_membership_id, self.membership.id)
        self.assertEqual(reg_info_2.program_membership_id, self.membership.id)

    def test_create_program_registrant_info(self):
        action = self.membership.create_program_registrant_info()
        self.assertEqual(action["name"], "Create Application")
        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["res_model"], "g2p.program.registrantinfo.wizard")
        self.assertEqual(action["view_mode"], "form")
        self.assertEqual(action["target"], "new")
