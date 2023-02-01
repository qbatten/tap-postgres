import pendulum

from singer_sdk.testing import get_tap_test_class

from tap_postgres.tap import TapPostgres

SAMPLE_CONFIG = {
    "start_date": pendulum.datetime(2022,11,1).to_iso8601_string(),
    "sqlalchemy_url": "postgresql://postgres:postgres@localhost:5432/postgres",
}

TestTapPostgres = get_tap_test_class(
    tap_class=TapPostgres,
    config=SAMPLE_CONFIG,
)
