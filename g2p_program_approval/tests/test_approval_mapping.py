from werkzeug.exceptions import Forbidden

from odoo.tests.common import TransactionCase


class TestProgramApprovalMapping(TransactionCase):
    def setUp(self):
        super().setUp()
        # Create necessary records (approval groups, mappings with different states)
        group_manager = self.env["res.groups"].create({"name": "Program Manager"})
        group_reviewer = self.env["res.groups"].create({"name": "Program Reviewer"})
        self.mapping1 = self.env["g2p.program.approval.mapping"].create(
            {
                "state": "draft",
                "group_id": group_manager.id,
                "entitlement_manager_ref": "manager1",
            }
        )
        self.mapping2 = self.env["g2p.program.approval.mapping"].create(
            {
                "state": "review",
                "group_id": group_reviewer.id,
                "entitlement_manager_ref": "reviewer1",
            }
        )

    def test_create(self):
        # Test sequence assignment during creation
        new_mapping = self.env["g2p.program.approval.mapping"].create(
            {
                "state": "draft",
                "group_id": self.env.ref("g2p_program_approval.group_manager").id,
                "entitlement_manager_ref": "manager2",
            }
        )
        self.assertGreater(new_mapping.sequence, 0)  # Ensure sequence is assigned

    def test_get_next_mapping_empty(self):
        # Test with no mappings
        success, res = self.mapping1.get_next_mapping("draft")
        self.assertTrue(success)
        self.assertIsNone(res)

    def test_get_next_mapping_current_state(self):
        # Test getting next mapping for current state
        success, res = self.mapping1.get_next_mapping("draft")
        self.assertTrue(success)
        self.assertEqual(res, self.mapping2)

    def test_get_next_mapping_no_state(self):
        # Test with no state provided
        success, res = self.mapping1.get_next_mapping()
        self.assertTrue(success)
        self.assertEqual(res, self.mapping1)

    def test_get_next_mapping_forbidden(self):
        # Test with incorrect user group
        with self.assertRaises(Forbidden):
            self.env.user.groups_id = self.env.ref(
                "g2p_program_approval.group_reviewer"
            )  # Simulate wrong group
            self.mapping1.get_next_mapping("draft")

    def test_get_next_mapping_no_raise_error(self):
        # Test without raising error for incorrect user
        success, res = self.mapping1.get_next_mapping("draft", raise_incorrect_user_error=False)
        self.assertTrue(success)
        self.assertEqual(res, self.mapping2)

    def test_get_next_mapping_multiple_mappings(self):
        # Test with multiple mappings and different states
        success, res = self.mapping2.get_next_mapping("review")
        self.assertTrue(success)
        self.assertEqual(res, self.mapping3)

    def test_get_next_mapping_no_matching_state(self):
        # Test with a state that doesn't exist
        success, res = self.mapping1.get_next_mapping("non-existent")
        self.assertTrue(success)  # Function should still return success
        self.assertIsNone(res)  # But result should be None
