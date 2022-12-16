import models
import bcrypt
import main
import schemas
from main import Person
from sqlalchemy.orm import Session


def get_people(db: Session):
    q = db.query(Person).all()
    return q


def find_person_via_id(user_id: int, db: Session):
    q = db.query(Person).filter(Person.id == user_id).first()
    return q


def find_person_via_email(email: str, db: Session):
    q = db.query(Person).filter(Person.email == email).first()
    return q


def create_user(user: schemas.CreateUserModel, db: Session):
    # find user
    is_duplicate = find_person_via_email(user.email, db)
    if is_duplicate:
        return False
    hash_pw = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    person = Person(username=user.username, email=user.email, password=hash_pw)
    db.add(person)
    db.commit()
    db.refresh(person)
    return True


def verify_user(password: str, hashed_password: str):
    result = bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    if result:
        return True
    else:
        return False


def update_user(id: int, obj, db: Session):
    user = find_person_via_id(id, db)
    if user:
        email = obj.email
        valid_email = find_person_via_email(email, db)
        if not valid_email:
            hash_pw = bcrypt.hashpw(obj.password.encode('utf-8'), bcrypt.gensalt())
            q = db.query(main.Person).filter(main.Person.id == id).update(
                {'password': hash_pw, 'username': obj.username,'email': obj.email});
            db.commit()
            return True, 'Update successfully'
        else:
            return False, 'Email already exists'
    else:
        return False, 'User could not be found'


def delete_user(id: int, db: Session):
    user = find_person_via_id(id,db)
    if user:
        db.query(main.Person).filter(main.Person.id == id).delete()
        db.commit()
        return True
    return False