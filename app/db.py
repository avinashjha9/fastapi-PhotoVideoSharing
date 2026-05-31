#ORM
from  collections.abc import AsyncGenerator
import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime


DATABASE_URL = "sqlite+aiosqlite:///./test.db"

"""Datamodels are the tables in the database. They are defined as classes that inherit from the Base class provided by SQLAlchemy. 
Each class represents a table, and each attribute of the class represents a column in the table.
Datamodel are the type of the data that we want to store in the database. They are defined as classes that inherit from the BaseModel class provided by Pydantic.
Each class represents a type of data, and each attribute of the class represents a field in the data.
"""

class Base(DeclarativeBase): #DeclarativeBase is a class that provides a base for all the datamodels. It is used to create the tables in the database.
    pass

#create async engine is used to create a connection to the database. 
#It is used to execute SQL queries and to create tables in the database. The echo parameter is set to True to log all the SQL queries that are executed.

engine = create_async_engine(DATABASE_URL, echo=True)

#async_sessionmaker is used to create a session that is used to execute SQL queries. 
#The expire_on_commit parameter is set to False to prevent the session from expiring after a commit. 
#This allows us to access the data that was committed to the database without having to refresh the session.

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

#create_db_and_tables is a function that is used to create the tables in the database. It is called when the application starts. 
#It uses the metadata of the Base class to create the tables in the database. 
#The metadata is a collection of all the datamodels that are defined in the application.

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

#get_asyn_session is a function that is used to get a session that is used to execute SQL queries. 
#It is an asynchronous generator that yields a session. The session is created using the async_session_maker and is closed after the yield statement.
#This function is used in the routes to get a session that is used to execute SQL queries. 
#This allows us to use the session in the routes without having to worry about closing the session after the request is completed.

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


class Post(Base):        #Post is a datamodel that represents the posts table in the database. It has the following columns: id, title, content, created_at.
    __tablename__ = "posts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    caption = Column(Text)
    url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
