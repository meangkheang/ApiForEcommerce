from fastapi import FastAPI, Depends
import auth
import logic
import schemas
from app_routers import item_router,khmer_quote_router
from main import session


def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()


app = FastAPI(
    dependencies=[Depends(auth.authorize_user)]
)


@app.get('/users',response_model=schemas.ResponseListUser)
async def get_all_users(db: logic.Session = Depends(get_db)):
    result = dict(code='000',message='success',data='')
    users = logic.get_people(db)
    items = []
    for user in users:
        items.append(schemas.UserModel(id=user.id,username=user.username,email=user.email))
    result['data'] = items
    return result


@app.get('/users/{id}')
async def find_user_via_id(user_id: int, db: logic.Session = Depends(get_db)):
    result = dict(code='000',message='success',data='')
    user = logic.find_person_via_id(user_id,db)
    if not user:
        result.update({
            'code': "100",
            'message': 'No record found.'
        })
        return result
    result['data'] = schemas.UserModel(id= user.id, username=user.username,email=user.email)
    return result


@app.post('/users',response_model=schemas.ResponseUser)
async def create_user(user: schemas.CreateUserModel,db: logic.Session = Depends(get_db)):
    result = dict(code='000',message='success',data='')
    is_success = logic.create_user(user,db)
    if is_success:
        result['data'] = user
        return result
    else:
        result.update({
            'code': "100",
            'message': 'try to create user already exists'
        })
        return result


@app.post('/users/logic')
async def user_login(email: str, password: str,db: logic.Session= Depends(get_db)):
    result = dict(code='000',message='success',data='')
    user = logic.find_person_via_email(email,db)
    if user:
        invalid_pw =  logic.verify_user(password,user.password)
        if invalid_pw:
            result['message'] = 'log in successfully.'
            return result
        else:
            result['code'] = '100'
            result['message'] = 'incorrect password.'
            return result


@app.put('/update_user')
async def update_user(id: int,user: schemas.CreateUserModel, db = Depends(get_db)):
    result = dict(code='000',message='update user successfully',data='')
    is_success = logic.update_user(id,user  ,db)
    if is_success[0]:
        return result
    else:
        result['code'] = '100'
        result['message'] = is_success[1]
        return result


@app.delete('/delete_user')
async def delete_user(id: int, db = Depends(get_db)):
    result = dict(code='000',message='deleted user successfully',data='')
    is_success = logic.delete_user(id,db)
    if is_success:
        return result
    result['message'] = 'Fail to delete cause user not founded'
    result['code'] = '100'
    return result

app.include_router(item_router.router)
app.include_router(khmer_quote_router.router)
