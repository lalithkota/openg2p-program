from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestProgramFundManagement(TransactionCase):
    def setUp(self):
        super().setUp()
        self.program = self.env["g2p.program"].create(
            {
                # Set up necessary fields for program
                "name": "test program"
            }
        )
        # self.journal = self.env['account.journal'].create({
        #     'name': 'Test Journal',
        #     'type': 'sale',
        #     # Set up necessary fields for journal
        # })
        self.program_fund = self.env["g2p.program.fund"].create(
            {
                "name": "test fund",
                "program_id": self.program.id,
                # 'journal_id': self.journal.id,
                "amount": 1000,
            }
        )

    def test_unlink_fund(self):
        # Test unlink_fund method
        self.program_fund.state = "posted"
        with self.assertRaises(UserError):
            self.program_fund._unlink_fund()
        # Assert UserError is raised when trying to delete a posted fund

    def test_post_fund(self):
        # Test post_fund method when fund is in draft state
        self.program_fund.state = "draft"
        self.program_fund.name = "Draft"
        self.program_fund.post_fund()
        # Assert the state is updated to 'posted'
        self.assertEqual(self.program_fund.state, "posted")
        # Assert the name is updated if it was 'Draft' or None
        if self.program_fund.name in ("Draft", None):
            self.assertNotEqual(self.program_fund.name, "Draft")
            self.assertIsNotNone(self.program_fund.name)

        # Test post_fund method when fund is not in draft state
        self.program_fund.state = "posted"
        with self.assertRaises(UserError):
            self.program_fund.post_fund()

    def test_cancel_fund(self):
        # Test cancel_fund method
        # Test when fund is in draft state
        self.program_fund.state = "draft"
        self.program_fund.cancel_fund()
        # Assert the result is as expected

        # Test when fund is not in draft state
        self.program_fund.state = "posted"
        self.program_fund.cancel_fund()
        # Assert the result is as expected

    def test_reset_draft(self):
        # Test reset_draft method
        # Test when fund is in cancelled state
        self.program_fund.state = "cancelled"
        self.program_fund.reset_draft()
        # Assert the result is as expected

        # Test when fund is not in cancelled state
        self.program_fund.state = "posted"
        self.program_fund.reset_draft()
        # Assert the result is as expected
