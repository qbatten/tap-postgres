"""Test Configuration."""
import pytest

from .test_replication_key import setup_test_table, teardown_test_table

pytest_plugins = ("singer_sdk.testing.pytest_plugin",)

SQLALCHEMY_URL = "postgresql://postgres:postgres@localhost:5432/postgres"


@pytest.fixture(scope="session", autouse=True)
def fake_data():
    setup_test_table(table_name="test_full_table", sqlalchemy_url=SQLALCHEMY_URL)
    setup_test_table(table_name="test_replication_key", sqlalchemy_url=SQLALCHEMY_URL)
    yield
    teardown_test_table(table_name="test_full_table", sqlalchemy_url=SQLALCHEMY_URL)
    teardown_test_table(
        table_name="test_replication_key", sqlalchemy_url=SQLALCHEMY_URL
    )
