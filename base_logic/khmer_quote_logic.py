import math
import random

# import models
import bcrypt
import main
import schemas
from main import Person
from sqlalchemy.orm import Session


def create_quote(obj, db: Session):
    quote = main.KhmerQuote(**obj.dict())
    db.add(quote)
    db.commit()
    db.refresh(quote)
    return quote


def get_all_quotes(db: Session):
    quotes = db.query(main.KhmerQuote).all()
    return quotes


def get_random_quote(db: Session):
    quotes = db.query(main.KhmerQuote).all()
    maxlen = len(quotes)
    ranvalue = math.floor(random.randint(0,maxlen-1 ))
    return quotes[ranvalue]