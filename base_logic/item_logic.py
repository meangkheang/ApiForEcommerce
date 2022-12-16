# import models
import bcrypt
import main
import schemas
from main import Person
from sqlalchemy.orm import Session


def get_all_items(db: Session):
    q = db.query(main.Item).all()
    return q


def find_user_with_id(id: int,db: Session):
    q = db.query(main.Person).filter(main.Person.id == id).first()
    return q


def find_item_with_id(id: int,db: Session):
    q = db.query(main.Item).filter(main.Item.id == id).first()
    return q


def create_item(obj, db: Session):
    user = find_user_with_id(obj.person_id,db)
    if user:
        item = main.Item(**obj.dict())
        db.add(item)
        db.commit()
        return item
    else:
        return False


def update_item(id: int, obj,db: Session):
    item = find_item_with_id(id,db)
    if item:
        q = db.query(main.Item).filter(main.Item.id == id)
        q = q.update({'person_id': obj.person_id, 'name': obj.name})
        db.commit()
        return item
    else:
        return False


def delete_item(id: int, db: Session):
    item = find_item_with_id(id,db)
    if item:
        db.query(main.Item).filter(main.Item.id == id).delete();
        db.commit()
        return True
    else:
        return False


def find_items_with_name(name: str, db: Session):
    items = db.query(main.Item).filter(main.Item.name.like('%'+name+'%')).all()
    return items



