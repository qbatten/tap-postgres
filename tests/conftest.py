"""Test Configuration."""
import pytest

from .test_replication_key import setup_test_table, teardown_test_table

pytest_plugins = ("singer_sdk.testing.pytest_plugin",)


# @pytest.fixture(scope="module")
# def fake_data():
#     setup_test_table()
#     yield
#     teardown_test_table()
