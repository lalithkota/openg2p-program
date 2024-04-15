from odoo.tests.common import TransactionCase


class G2PCycleManagerTest(TransactionCase):
    def setUp(self):
        super(G2PCycleManagerTest, self).setUp()
        self.program = self.env["g2p.program"].create({"name": "Test Program"})
        self.cycle_manager = self.env["g2p.cycle.manager.default"].create(
            {
                "program_id": self.program.id,
                "auto_approve_entitlements": False,
                "cycle_duration": 1,
            }
        )

    def test_selection_manager_ref_id(self):
        selection = self.cycle_manager._selection_manager_ref_id()
        self.assertIn(("g2p.cycle.manager.default", "Default"), selection)
