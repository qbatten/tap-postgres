import pendulum
import pytest
from singer_sdk.testing import get_tap_test_class, suites
from singer_sdk.testing.suites import TestSuite
from singer_sdk.testing.templates import StreamTestTemplate

from tap_postgres.tap import TapPostgres

from .test_replication_key import TABLE_NAME, setup_test_table, teardown_test_table

SAMPLE_CONFIG = {
    "sqlalchemy_url": "postgresql://postgres:postgres@localhost:5432/postgres",
    "start_date": pendulum.datetime(2022, 11, 1).to_iso8601_string(),
}

TapPostgresFullTable = get_tap_test_class(
    tap_class=TapPostgres,
    config=SAMPLE_CONFIG,
    catalog="tests/resources/test-full-table.json",
)


class TapPostgresFixtures:
    """Base Fixtures Class."""

    @pytest.fixture(scope="class")
    def resource(self, fake_data):
        yield


class TestTapPostgresFullTable(TapPostgresFixtures, TapPostgresFullTable):
    """Standard Tests."""


# Incremental Tests
STATE_BOOKMARK = "2022-11-15T00:00:00+00:00"  # half way through sample data
INCREMENTAL_START = pendulum.parse(STATE_BOOKMARK)

STATE = {
    "bookmarks": {
        "public-test_replication_key": {
            "replication_key": "updated_at",
            "replication_key_value": STATE_BOOKMARK,
        }
    }
}
SAMPLE_CONFIG.pop("start_date")


class StreamReplicationKeyTest(StreamTestTemplate):
    name = "replication_key"

    def test(self):
        if self.stream.name == "public-test_replication_key":
            # test that data starts from bookmark
            first_record_updated_at = pendulum.parse(
                self.stream_records[0]["updated_at"]
            )
            starting_bookmark = INCREMENTAL_START
            assert first_record_updated_at >= starting_bookmark
            # test that final STATE message writes correct bookmark
            new_bookmark = self.runner.state_messages[-1]["value"]["bookmarks"][
                "public-test_replication_key"
            ]["replication_key_value"]
            last_record_updated_at = self.stream_records[-1]["updated_at"]
            new_bookmark_dt = pendulum.parse(new_bookmark)
            assert new_bookmark == last_record_updated_at
            assert new_bookmark_dt <= pendulum.parse(
                "2022-11-30T00:00:00+00:00"
            )  # last possible record in fake data


custom_suite = TestSuite(kind="tap_stream", tests=[StreamReplicationKeyTest])


TapPostgresIncremental = get_tap_test_class(
    tap_class=TapPostgres,
    config=SAMPLE_CONFIG,
    catalog="tests/resources/test-incremental.json",
    custom_suites=[custom_suite],
    state=STATE,
)


class TestTapPostgresIncremental(TapPostgresFixtures, TapPostgresIncremental):
    """Incremental Test."""
