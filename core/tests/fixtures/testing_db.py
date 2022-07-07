import pytest

from core.db import Base, testing_engine


@pytest.fixture(scope="function", autouse=True)
def testing_db():
    Base.metadata.create_all(bind=testing_engine)

    yield

    Base.metadata.drop_all(bind=testing_engine)
