import pendulum
import pytest
from singer_sdk.testing import get_tap_test_class, suites
from singer_sdk.testing.suites import TestSuite
from singer_sdk.testing.templates import StreamTestTemplate

from tap_postgres.tap import TapPostgres

TapPostgresTests = get_tap_test_class(
    tap_class=TapPostgres,
    config="tests/resources/test-config.json",
    catalog="tests/resources/test-catalog-full-table.json",
)


class TestTapPostgres(TapPostgresTests):
    """Standard Tap Tests."""

    @pytest.fixture
    def resource(self, fake_data):
        yield


class StreamReplicationKeyTest(StreamTestTemplate):
    name = "replication_key"

    def test(self):
        if self.stream.replication_key:
            # test that data starts from bookmark
            bookmark_value = self.stream.stream_state.get("replication_key_value")
            starting_bookmark_dt = pendulum.parse(bookmark_value)
            first_record_updated_at_dt = pendulum.parse(
                self.stream_records[0]["updated_at"]
            )
            assert first_record_updated_at_dt >= starting_bookmark_dt

            # test that final STATE message writes correct bookmark
            new_bookmark = self.runner.state_messages[-1]["value"]["bookmarks"][
                "public-test_replication_key"
            ]["replication_key_value"]
            new_bookmark_dt = pendulum.parse(new_bookmark)
            last_record_updated_at = self.stream_records[-1]["updated_at"]
            assert new_bookmark == last_record_updated_at
            assert new_bookmark_dt <= pendulum.parse(
                "2022-11-30T00:00:00+00:00"
            )  # last possible record updated_at in fake data


custom_suite = TestSuite(kind="tap_stream", tests=[StreamReplicationKeyTest])


TapPostgresIncremental = get_tap_test_class(
    tap_class=TapPostgres,
    config="tests/resources/test-config.json",
    catalog="tests/resources/test-catalog-incremental.json",
    state="tests/resources/test-state-incremental.json",
    custom_suites=[custom_suite],
)


class TestTapPostgresIncremental(TapPostgresIncremental):
    """Incremental Test."""

    @pytest.fixture
    def resource(self, fake_data):
        yield
