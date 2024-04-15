from odoo.tests.common import TransactionCase


class TestBaseManager(TransactionCase):
    def setUp(self):
        super().setUp()
        self.base_manager = self.env["base.programs.manager"].create({})

    def test_get_eval_context(self):
        # Call the _get_eval_context method
        eval_context = self.base_manager._get_eval_context()

        # Ensure that the evaluation context contains the required keys
        self.assertIn("datetime", eval_context)
        self.assertIn("dateutil", eval_context)
        self.assertIn("time", eval_context)
        self.assertIn("uid", eval_context)
        self.assertIn("user", eval_context)

        # Ensure that the values of the keys are the expected types
        self.assertTrue(callable(eval_context["datetime"]))
        self.assertTrue(callable(eval_context["dateutil"]))
        self.assertTrue(callable(eval_context["time"]))
        self.assertEqual(eval_context["uid"], self.env.uid)
        self.assertEqual(eval_context["user"], self.env.user)

    def test_safe_eval(self):
        # Test a simple evaluation
        result = self.base_manager._safe_eval("2 + 2")
        self.assertEqual(result, 4)

        # Test evaluation with local variables
        locals_dict = {"a": 3, "b": 5}
        result = self.base_manager._safe_eval("a * b", locals_dict)
        self.assertEqual(result, 15)

        # Test evaluation with context variables
        result = self.base_manager._safe_eval("uid", {})
        self.assertEqual(result, self.env.uid)

        # Test evaluation with invalid expression
        with self.assertRaises(Exception):
            self.base_manager._safe_eval("1 / 0")
