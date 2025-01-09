from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite DB 사용
DATABASE_URL = "sqlite:///./sql_app.db"
# DATABASE_URL = "postgresql://myuser:mypassword@localhost:5432/mydatabase"
# 데이터베이스 엔진 생성
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 세션 생성
SessionLocal = sessionmaker(engine)

# 모델용 베이스 클래스
Base = declarative_base()

# DB 세션 가져오기
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
