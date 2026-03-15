import importlib.util
import json
import os
import sys
import unittest
from unittest import mock


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.aws import bedrock_client as bedrock_wrapper
from app.aws import dynamodb_client as dynamodb_wrapper
from app.aws import session as aws_session


class _FakeBody:
    def __init__(self, payload: dict):
        self.payload = json.dumps(payload).encode("utf-8")

    def read(self):
        return self.payload


class FallbackWrapperTests(unittest.TestCase):
    def setUp(self):
        dynamodb_wrapper._LOCAL_DB[dynamodb_wrapper._table_name("AnalysisResults")] = []
        dynamodb_wrapper._LOCAL_DB[dynamodb_wrapper._table_name("Appeals")] = []
        dynamodb_wrapper._LOCAL_DB[dynamodb_wrapper._table_name("Translations")] = []

    def test_embedding_uses_real_bedrock_when_available(self):
        fake_client = mock.Mock()
        fake_client.invoke_model.return_value = {"body": _FakeBody({"embedding": [0.1, 0.2, 0.3]})}

        with mock.patch.object(aws_session.Config, "MOCK_MODE", False), \
             mock.patch.object(aws_session, "RUNTIME_MOCK_MODE", False), \
             mock.patch.dict(aws_session.SERVICE_STATUS, {"bedrock": True}, clear=False), \
             mock.patch.object(bedrock_wrapper, "bedrock_client", fake_client), \
             mock.patch.object(bedrock_wrapper, "get_cached_embedding", return_value=None), \
             mock.patch.object(bedrock_wrapper, "set_cached_embedding") as cache_set:
            embedding = bedrock_wrapper.get_embedding("hello world")

        self.assertEqual(embedding, [0.1, 0.2, 0.3])
        cache_set.assert_called_once()

    def test_embedding_falls_back_when_bedrock_raises(self):
        fake_client = mock.Mock()
        fake_client.invoke_model.side_effect = RuntimeError("bedrock down")

        with mock.patch.object(aws_session.Config, "MOCK_MODE", False), \
             mock.patch.object(aws_session, "RUNTIME_MOCK_MODE", False), \
             mock.patch.dict(aws_session.SERVICE_STATUS, {"bedrock": True}, clear=False), \
             mock.patch.object(bedrock_wrapper, "bedrock_client", fake_client), \
             mock.patch.object(bedrock_wrapper, "get_cached_embedding", return_value=None), \
             mock.patch.object(bedrock_wrapper, "mock_generate_embedding", return_value=[9.9, 8.8]):
            embedding = bedrock_wrapper.get_embedding("fallback")

        self.assertEqual(embedding, [9.9, 8.8])

    def test_registry_lookup_falls_back_without_dynamodb(self):
        with mock.patch.object(aws_session.Config, "MOCK_MODE", False), \
             mock.patch.object(aws_session, "RUNTIME_MOCK_MODE", True), \
             mock.patch.dict(aws_session.SERVICE_STATUS, {"dynamodb": False}, clear=False):
            results = dynamodb_wrapper.query_registry(entity_name="Official Agency", domain="example.gov")

        self.assertTrue(results)
        self.assertIn("entity_name", results[0])


class FallbackApiTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        dynamodb_wrapper._LOCAL_DB[dynamodb_wrapper._table_name("AnalysisResults")] = []

    def test_analyze_route_returns_success_in_mock_mode(self):
        with mock.patch.object(aws_session.Config, "MOCK_MODE", True), \
             mock.patch.object(aws_session, "RUNTIME_MOCK_MODE", True):
            response = self.client.post(
                "/analyze",
                json={
                    "communication_text": "Official notification for citizens.",
                    "channel_type": "email",
                    "metadata": {"domain": "example.gov", "entity_name": "Official Agency"},
                },
            )

        payload = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("analysis_id", payload)
        self.assertIn("authenticity_score", payload)

    def test_health_route_degrades_instead_of_crashing_without_aws(self):
        with mock.patch.object(aws_session.Config, "MOCK_MODE", False), \
             mock.patch.object(aws_session, "RUNTIME_MOCK_MODE", True), \
             mock.patch.dict(aws_session.SERVICE_STATUS, {
                 "bedrock": False,
                 "dynamodb": False,
                 "dynamodb_client": False,
                 "s3": False,
                 "comprehend": False,
                 "sqs": False,
             }, clear=False), \
             mock.patch("app.routes.health.s3_client", None), \
             mock.patch("app.routes.health.sqs_client", None):
            response = self.client.get("/health")

        payload = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload["status"], "degraded")
        self.assertTrue(payload["mock_mode"])
        self.assertIn("services", payload)


if __name__ == "__main__":
    unittest.main()
