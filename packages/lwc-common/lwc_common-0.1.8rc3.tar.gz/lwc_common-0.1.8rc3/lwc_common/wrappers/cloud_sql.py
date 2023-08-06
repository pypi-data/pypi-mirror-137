import json
import typing as t
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


class CloudSQLWrapper:
    engine: Engine = None
    declarative_base: DeclarativeMeta = None

    def __init__(
        self,
        db_host: str,
        db_port: t.Union[str, int],
        db_name: str,
        db_username: str,
        db_password: str
    ):
        self.DB_HOST = db_host
        self.DB_PORT = db_port
        self.DB_NAME = db_name
        self.DB_USERNAME = db_username
        self.DB_PASSWORD = db_password
        self.engine = self._create_engine()
        self.declarative_base = declarative_base()

    def _create_engine(self) -> Engine:
        engine = create_engine(
            "postgresql+pg8000://{}:{}@{}:{}/{}".format(
                self.DB_USERNAME, self.DB_PASSWORD, self.DB_HOST,
                str(self.DB_PORT), self.DB_NAME
            ))
        return engine

    def get_declarative_base(self):
        return self.declarative_base

    def get_query_property(self):
        session = scoped_session(sessionmaker(bind=self.engine))
        return session.query_property()

    @staticmethod
    def update_lists(partition: str, profile_url: str, success: bool, master_filepath: str):
        # TODO: use db here
        MASTER_LIST = master_filepath
        with open(MASTER_LIST) as file:
            master = json.loads(file.read() or "{}")
        monitor = master.get(partition, {})
        successes = set(monitor.get("success", []))
        failures = set(monitor.get("failure", []))
        new = set(monitor.get("new", []))
        new = new - {profile_url}
        if success:
            failures = failures - {profile_url}
            successes.add(profile_url)
        else:
            failures.add(profile_url)

        # write new data
        master[partition] = {
            "new": list(new),
            "success": list(successes),
            "failure": list(failures)
        }
        with open(MASTER_LIST, "w") as file:
            json.dump(master, file, indent=4)
