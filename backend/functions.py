from sqlalchemy import Integer, String, Float, Column, create_engine, DateTime
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime, timedelta, timezone
import jwt

DB_PATH = "warehouse.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

USERNAME = "Soham"
PASSWORD = "123456"

ACCESS_TOKEN_EXPIRY = 1
REFRESH_TOKEN_EXPIRY = 7 * 24 * 60
SECRET_KEY = "SECRET123"
ALGORITHM = "HS256"

class Package(Base):
    __tablename__ = "packages"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    destination = Column(String)
    weight = Column(Float)
    arrival_date = Column(DateTime, default=datetime.now)
    status = Column(String)

Base.metadata.create_all(engine)

def add_package(name, destination, weight, status="pending"):
    session = Session(engine)
    pkg = Package(
        name=name,
        destination=destination,
        weight=float(weight),
        status=status
    )
    session.add(pkg)
    session.commit()
    response = {
        "id": pkg.id,
        "name": pkg.name,
        "destination": pkg.destination,
        "weight": pkg.weight,
        "arrival_date": pkg.arrival_date,
        "status": pkg.status
    }
    session.close()
    return response

def get_package(id):
    session = Session(engine)
    pkg = session.get(Package, id)
    if not pkg:
        session.close()
        return None
    response = {
        "id": pkg.id,
        "name": pkg.name,
        "destination": pkg.destination,
        "weight": pkg.weight,
        "arrival_date": pkg.arrival_date,
        "status": pkg.status
    }
    session.close()
    return response

def update_package(id, name=None, destination=None, weight=None, status=None):
    session = Session(engine)
    pkg = session.get(Package, id)
    if not pkg:
        session.close()
        return None

    if name is not None:
        pkg.name = name
    if destination is not None:
        pkg.destination = destination
    if weight is not None:
        pkg.weight = float(weight)
    if status is not None:
        pkg.status = status

    session.commit()
    response = {
        "id": pkg.id,
        "name": pkg.name,
        "destination": pkg.destination,
        "weight": pkg.weight,
        "arrival_date": pkg.arrival_date,
        "status": pkg.status
    }
    session.close()
    return response

def delete_package(id):
    session = Session(engine)
    pkg = session.get(Package, id)
    if not pkg:
        session.close()
        return "not_found"

    if pkg.status == "dispatched":
        session.close()
        return "dispatched"

    session.delete(pkg)
    session.commit()
    session.close()
    return "deleted"

def verify_login(username:{__eq__}, password:{__eq__}):
    if username == USERNAME and password == PASSWORD:
        access_token = create_token(username=username, token_type="access")
        refresh_token = create_token(username=username, token_type="refresh")
        return {"access_token": access_token, "refresh_token": refresh_token}
    return None

def create_token(username, token_type):
    time = ACCESS_TOKEN_EXPIRY
    if token_type == "refresh":
        time = REFRESH_TOKEN_EXPIRY
    payload = {
        "username": username,
        "token_type": token_type,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=time)
    }
    token = jwt.encode(payload = payload, key = SECRET_KEY, algorithm =ALGORITHM)
    return token

def verify_token(token, token_type):
    try:
        payload = jwt.decode(jwt = token, key = SECRET_KEY, algorithms = [ALGORITHM])
    except:
        return False
    if payload["token_type"] == token_type:
        return payload["username"]
    return False