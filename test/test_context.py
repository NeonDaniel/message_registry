import unittest

from message_models.context import *
from pydantic import ValidationError


class TestContext(unittest.TestCase):
    def test_import_models(self):
        from pydantic import BaseModel
        self.assertIsInstance(UserProfile(), BaseModel)
        self.assertIsInstance(IntentContext(), BaseModel)
        self.assertIsInstance(SessionContext(), BaseModel)
        self.assertIsInstance(Session(), BaseModel)
        self.assertIsInstance(Context(), BaseModel)

    def test_context(self):
        from message_models.context import Context
        with self.assertRaises(ValidationError):
            Context.model_validate({})
        valid = Context.model_validate({"source": "test",
                                        "destination": "test"})
        self.assertIsInstance(valid, Context)
        # TODO: Test model_dump
