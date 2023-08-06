import typing as t
from sqlalchemy import create_engine
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


class CloudSQLWrapper:
    engine: Engine = None
    declarative_base: DeclarativeMeta = None
    ProfileURLClass = None
    JobTitleClass = None
    LocationClass = None

    def __init__(
        self,
        db_host: str,
        db_port: t.Union[str, int],
        db_name: str,
        db_username: str,
        db_password: str,
        urls_table_name: str = "",
        job_titles_table_name: str = "",
        locations_table_name: str = ""
    ):
        self.DB_HOST = db_host
        self.DB_PORT = db_port
        self.DB_NAME = db_name
        self.DB_USERNAME = db_username
        self.DB_PASSWORD = db_password

        self.URLS_TABLE_NAME = urls_table_name
        self.JOB_TITLES_TABLE_NAME = job_titles_table_name
        self.LOCATIONS_TABLE_NAME = locations_table_name
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

    def update_master_list(
        self,
        profile_url: str,
        job_title: str,
        location: str,
        pdf_hash: str = None,
        pdf_bytesize: str = None,
        pdf_stage: bool = None,
        json_stage: bool = None,
        processor_stage: bool = None,
        success: bool = None,
        create_if_absent: bool = False
    ):
        attrs = {
            "pdf_hash": pdf_hash,
            "pdf_bytesize": pdf_bytesize,
            "pdf_stage": pdf_stage,
            "json_stage": json_stage,
            "processor_stage": processor_stage,
            "success": success
        }
        if not any(attrs.values()):
            raise Exception(
                f"You must supply one of {list(attrs.keys())}"
            )
        if not self.ProfileURLClass:
            raise Exception("To use this feature, call `create_models`"
                            " and `create_tables_in_db` first")

        _query = self.ProfileURLClass.query\
            .filter_by(linkedin_url=profile_url)\
            .filter_by(job_title=job_title)\
            .filter_by(location=location)
        url_obj = _query.first()

        if (not url_obj) and create_if_absent:
            url_obj = self.ProfileURLClass(
                linkedin_url=profile_url, job_title=job_title,
                location=location
            )
        elif not url_obj:
            raise Exception(
                f"Profile URL {profile_url} does not exist in "
                f"LWC Table. Call again with `create_if_absent=True` "
                f"to add")

        for attr, value in attrs.items():
            if value is not None:
                setattr(url_obj, attr, value)
        session = self.ProfileURLClass.query.session
        session.add(url_obj)
        session.commit()
        session.close()

    def create_models(self):
        reqd = (self.URLS_TABLE_NAME, self.JOB_TITLES_TABLE_NAME, self.LOCATIONS_TABLE_NAME)
        if not all(reqd):
            raise Exception(
                'Attributes "URLS_TABLE_NAME", "JOB_TITLES_TABLE_NAME"'
                ' and "LOCATIONS_TABLE_NAME" should be set to use this'
                ' feature'
            )
        query_property = self.get_query_property()

        class ProfileURL(self.declarative_base):
            __tablename__: str = self.URLS_TABLE_NAME
            url_id: str = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
            linkedin_url: str = Column(Text)
            job_title: str = Column(Text)
            location: str = Column(Text)
            pdf_hash: t.Optional[str] = Column(Text, nullable=True)
            pdf_bytesize: t.Optional[str] = Column(Text, nullable=True)
            pdf_stage: t.Optional[bool] = Column(Boolean, nullable=True)
            json_stage: t.Optional[bool] = Column(Boolean, nullable=True)
            processor_stage: t.Optional[bool] = Column(Boolean, nullable=True)
            success: t.Optional[bool] = Column(Boolean, nullable=True)
            query = query_property

            def dict(self) -> t.Dict:
                retval = {
                    "url_id": self.url_id,
                    "linkedin_url": self.linkedin_url,
                    "job_title": self.job_title,
                    "location": self.location,
                    "pdf_hash": self.pdf_hash,
                    "pdf_bytesize": self.pdf_bytesize,
                    "pdf_stage": self.pdf_stage,
                    "json_stage": self.json_stage,
                    "processor_stage": self.processor_stage,
                    "success": self.success
                }
                return retval

        class JobTitle(self.declarative_base):
            __tablename__: str = self.JOB_TITLES_TABLE_NAME
            job_id: str = Column(Text, primary_key=True, nullable=False)
            job_title: str = Column(Text)
            query = query_property

            def dict(self) -> t.Dict:
                retval = {
                    "job_id": self.job_id,
                    "job_title": self.job_title
                }
                return retval

        class Location(self.declarative_base):
            __tablename__: str = self.LOCATIONS_TABLE_NAME
            location_id: str = Column(Text, primary_key=True, nullable=False)
            location: str = Column(Text)
            query = query_property

            def dict(self) -> t.Dict:
                retval = {
                    "location_id": self.location_id,
                    "location": self.location
                }
                return retval

        self.ProfileURLClass = ProfileURL
        self.JobTitleClass = JobTitle
        self.LocationClass = Location
        return ProfileURL, JobTitle, Location

    def create_tables_in_db(self):
        self.declarative_base.metadata.create_all(self.engine)

