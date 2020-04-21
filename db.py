import atexit

from sqlalchemy import create_engine, MetaData, Table, Column, Text, Integer
from sqlalchemy.orm import sessionmaker, class_mapper, mapper
from sqlalchemy.orm.exc import UnmappedClassError
from testcontainers.postgres import PostgresContainer

# spin up a testcontainer

class Thingy:
    def __init__(self, database, id, name):
        self.db = database
        self.id = id
        self.name = name

    def __enter__(self):
        self.db.session.add(self)
        self.db.session.commit()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if exception_type:
            self.db.session.rollback()
            # in the real world, we set job.status = 'failed' here
        self.db.session.add(self)
        self.db.session.commit()
        return False


class Database:
    """
    Example database
    """

    def __init__(self):
        self.url = self.get_connection_string()
        self.engine = create_engine(self.url)
        self.metadata = MetaData(bind=self.engine, schema='example')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        self.add_unrelated_table()
        self.add_thingy_table()

        self.reset()

    def add_unrelated_table(self):
        """ This is an unrelated table on the same db and schema """
        Table('unrelated_guff', self.metadata,
              Column('id', Integer, primary_key=True))

    def add_thingy_table(self):
        """ We have to map this manually """
        thingy_table = Table('thingy', self.metadata,
                             Column('id', Integer, primary_key=True),
                             Column('name', Text, nullable=False))

        try:
            class_mapper(Thingy)
        except UnmappedClassError:
            mapper(Thingy, thingy_table)

    def get_connection_string(self):
        postgres = PostgresContainer('postgres')
        postgres.start()
        atexit.register(postgres.stop)
        return postgres.get_connection_url()

    def get_things(self, name):
        return self.session.query(Thingy).filter(Thingy.name == name).all()

    def reset(self):
        self.engine.execute('DROP SCHEMA IF EXISTS example CASCADE;')
        self.engine.execute('CREATE SCHEMA example;')
        #self.session.commit()

        self.metadata.create_all()

db = Database()
