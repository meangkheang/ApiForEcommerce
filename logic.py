import models
import bcrypt
import main
import schemas
from main import Person
from sqlalchemy.orm import Session


def get_people(db: Session):
    q = db.query(Person).all()
    return q


def find_person_via_id(user_id: int,db: Session):
    q = db.query(Person).filter(Person.id == user_id).first()
    return q


def find_person_via_email(email: str,db: Session):
    q = db.query(Person).filter(Person.email == email).first()
    return q


def create_user(user: schemas.CreateUserModel,db: Session):
    # find user
    is_duplicate = find_person_via_email(user.email,db)
    if is_duplicate:
        return False
    hash_pw = bcrypt.hashpw(user.password.encode('utf-8'),bcrypt.gensalt())
    person = Person(username=user.username,email=user.email,password=hash_pw)
    db.add(person)
    db.commit()
    db.refresh(person)
    return True


def verify_user(password: str, hashed_password: str):
    result = bcrypt.checkpw(password.encode('utf-8'),hashed_password)
    if result:
        return True
    else:
        return False