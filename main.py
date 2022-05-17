from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from authentication.hashing import Hash
from models.todo import Todo
from models.user import User
from authentication.auth_handler import get_current_user
from database.todo import TodoDB
from database.user import UserDB
from authentication.jwt import create_jwt_token
from services.response import success_response, error_response


app = FastAPI()

@app.post('/api/register/')
async def create_user(request:User):
    ''' Register User for Authentication '''
    user = await UserDB().find_user(request.username)
    if user:
        return error_response(status=400,msg="User already exists")
    hashed_pass = Hash.bcrypt(request.password)
    data = dict(request)
    data["password"] = hashed_pass
    response = await UserDB().create_user(data)
    return success_response(msg="User Registered Successfully")

@app.post('/api/login/')
async def login(request:OAuth2PasswordRequestForm = Depends()):
    ''' Login API to get Jwt Token for Authentication '''
    user = await UserDB().find_user(request.username)
    if not user:
       return error_response(status=400,msg="Invalid username or password")
    if not Hash.verify(user["password"],request.password):
        return error_response(status=400,msg="Invalid username or password")
    access_token = create_jwt_token(user=user["username"])
    return {
            "access_token":access_token,
            "type":"bearer"
        }

@app.get("/api/todo/")
async def get_todo():
    '''Get list of all Todos'''
    try:
        response = await TodoDB().todo_list()
    except Exception as error:
        return HTTPException(400,error)
    if response:
        return success_response(data=response)
    return success_response(msg="No Todos found")

@app.post("/api/todo/")
async def post_todo(todo: Todo,current_user:User = Depends(get_current_user)):
    ''' Create New Todo with Jwt Authentication '''
    try:
        data = todo.dict()
        response = await TodoDB().create_new_todo(data)
    except Exception as error:
        return HTTPException(400,error)
    if response:
        return success_response(data=response)
    return error_response(status=400,msg="Unable to create todo")


@app.get("/api/todo/{name}/")
async def get_todo(name):
    ''' Get Single Todo using name field'''
    try:
        response = await TodoDB().get_todo_detail(name)
    except Exception as error:
        return HTTPException(400,error)
    if response:
        return success_response(data=response)
    return error_response(status=404,msg=f"There is no todo with the title {name}")



@app.patch("/api/todo/{name}/")
async def update(name:str,data:dict,current_user:User = Depends(get_current_user)):
    ''' Update Todo API with Jwt Authentication '''
    try:
        response = await TodoDB().update_todo(name,data)
    except Exception as error:
        return HTTPException(400,error)
    if response:
        return success_response(data=response)
    return error_response(status=404,msg=f"There is no todo with the title {name}")


@app.delete("/api/todo/{name}/")
async def delete(name:str,current_user:User = Depends(get_current_user)):
    ''' Delete Todo API with Jwt Authentication '''
    try:
        response = await TodoDB().delete_todo(name)
    except Exception as error:
        return HTTPException(400,error)
    if response:
        return success_response(msg="Todo deleted Successfully")
    return error_response(status=404,msg=f"There is no todo with the title {name}")