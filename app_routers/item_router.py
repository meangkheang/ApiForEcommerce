from fastapi import APIRouter,Depends
from pydantic import BaseModel
import main
from base_logic import item_logic
from main import session
from typing import Optional,List

def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()


class Item(BaseModel):
    id: int
    name: str
    user_id: int


class CreateItem(BaseModel):
    name: str
    person_id: int


class ListItem(BaseModel):
    code: str
    message: str
    data: Optional[List[Item]]


router = APIRouter(prefix='/items',tags=["items"])


@router.get('/items')
async def get_items(db: main.Session = Depends(get_db)):
    result = dict(code='000',message='success',data='')
    items = item_logic.get_all_items(db)
    result['data'] = items
    return result


@router.post('/items')
async def create_item(item: CreateItem,db = Depends(get_db)):
    result = dict(code='000',message='success',data='')
    obj = item_logic.create_item(item,db)
    if obj:
        result['data'] = obj
        return result
    result['code'] = '100'
    result['message'] = 'Fail to create cause User not founded'
    return result


@router.put('/items/{id}')
async def update_item(id: int, item: CreateItem,db= Depends(get_db)):
    result = dict(code='000',message='success',data='')
    item = item_logic.update_item(id,item,db)
    if item:
        result['data'] = item
        return result
    result['code'] = '100'
    result['message'] = 'fail'
    return result


@router.delete('/items')
async def delete_item(id: int, db = Depends(get_db)):
    result = dict(code='000',message='deleted item successfully',data='')
    is_success = item_logic.delete_item(id,db)
    if is_success:
        return result

    result['code'] = '100'
    result['message'] = 'item not found'
    return result


@router.get('/find_items_with_names')
async def find_items_with_name(name: str,db = Depends(get_db)):
    result = dict(code='000',message='success',data='')
    items = item_logic.find_items_with_name(name,db)
    result['data'] = items
    return result


@router.get('/items/{id}')
async def find_item_with_id(id: int,db = Depends(get_db)):
    result = dict(code='000',message='success',data='')
    item = item_logic.find_item_with_id(id,db)
    if item:
        result['data'] = item
        return result

    result['code'] = '100'
    result['message'] = 'item not found'
    return result