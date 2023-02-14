"""Tests standard tap features using the built-in SDK tests library."""
import datetime

import pendulum
import sqlalchemy
from faker import Faker
from sqlalchemy import Column, DateTime, Integer, MetaData, String, Table


def setup_test_table(table_name, sqlalchemy_url):
    """setup any state specific to the execution of the given module."""
    engine = sqlalchemy.create_engine(sqlalchemy_url)
    fake = Faker()

    date1 = datetime.date(2022, 11, 1)
    date2 = datetime.date(2022, 11, 30)
    metadata_obj = MetaData()
    test_replication_key_table = Table(
        table_name,
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("updated_at", DateTime(), nullable=False),
        Column("name", String()),
    )
    with engine.connect() as conn:
        metadata_obj.create_all(conn)
        conn.execute(f"TRUNCATE TABLE {table_name}")
        for _ in range(1000):
            insert = test_replication_key_table.insert().values(
                updated_at=fake.date_between(date1, date2), name=fake.name()
            )
            conn.execute(insert)


def teardown_test_table(table_name, sqlalchemy_url):
    engine = sqlalchemy.create_engine(sqlalchemy_url)
    with engine.connect() as conn:
        conn.execute(f"DROP TABLE {table_name}")
