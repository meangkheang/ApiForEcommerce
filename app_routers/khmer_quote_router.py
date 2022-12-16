from fastapi import APIRouter,Depends
from pydantic import BaseModel
import main
from base_logic import item_logic,khmer_quote_logic
from main import session
from typing import Optional,List


def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()


class KhmerQuote(BaseModel):
    content: str


router = APIRouter(tags=['KhmerQuotes'],prefix='/khmer_quotes')


@router.get('')
async def get_all_khmer_quotes(db= Depends(get_db)):
    result = dict(code='000',message='success',data='')
    quotes = khmer_quote_logic.get_all_quotes(db)
    result['data'] = quotes
    return result


@router.post('')
async def create_khmer_quote(quote: KhmerQuote, db= Depends(get_db)):
    result = dict(code='000',message='success',data='')
    data = khmer_quote_logic.create_quote(quote,db)
    result['data'] = data
    return result


@router.get('/random/quote')
async def get_random_quote(db = Depends(get_db)):
    quote = khmer_quote_logic.get_random_quote(db)
    return quote