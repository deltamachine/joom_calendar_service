from core.db import SessionLocal


def get_db():
    """
    Возвращает инстанс базы данных.
    """

    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
