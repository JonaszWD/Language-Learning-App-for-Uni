import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import user as _user  # noqa: F401  (registers the table)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.utils.db import Base


@pytest.fixture()
def repo():
    engine = create_engine("sqlite:///:memory:")
    import app.models.post, app.models.vocabulary  # noqa: F401  (register relations)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    yield UserRepository(session)
    session.close()


def test_save_and_fetch_by_name(repo):
    saved = repo.save(User(name="ana", password=b"x"))
    assert saved.id is not None
    assert repo.get_by_name("ana").id == saved.id
    assert repo.get_by_id(saved.id).name == "ana"


def test_verify_username(repo):
    repo.save(User(name="ana", password=b"x"))
    assert repo.verify_username("ana")
    assert not repo.verify_username("nobody")


def test_delete_by_name(repo):
    repo.save(User(name="ana", password=b"x"))
    repo.delete_by_name("ana")
    assert repo.get_by_name("ana") is None


def test_delete_missing_user_is_a_noop(repo):
    repo.delete_by_name("ghost")
