from fastapi import APIRouter, Depends, Header, status, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from utils.postgres_connector import PostgresConnector
import psycopg2
from models.user import UpdateUserModel
import hashlib
from datetime import datetime, timedelta
import jwt
router = APIRouter()

connection = PostgresConnector(db_name="messenger_db")


def get_current_user(Authorization: str = Header(...)):
    try:
        payload = jwt.decode(Authorization.split()[
                             1], "secret_key", algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=402, detail="Invalid authentication credentials")
    except jwt.DecodeError:
        raise HTTPException(
            status_code=403, detail="Invalid authentication credentials")
    return user_id


@router.get("/show_all_users")
async def show_all_users(offset: int, limit: int, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    sql_command = "SELECT user_id, user_name, first_name, second_name from users OFFSET %s LIMIT %s"
    cursor.execute(sql_command, (offset, limit,))
    result = cursor.fetchall()
    cursor.close()
    return result


@ router.get("/user_info")
async def get_user_info(id: int, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    sql_command = f"SELECT user_id, user_name, first_name, second_name from users "
    f"WHERE user_id = {id}"
    print(sql_command)
    cursor.execute(sql_command)
    result = cursor.fetchall()
    cursor.close()
    return result


@ router.get("/find_by_name")
async def find_by_name(first_name: str, second_name: str, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    print(first_name, second_name)
    sql_command = f"SELECT user_id, user_name, first_name, second_name from users "
    f"WHERE first_name LIKE '{
        first_name}%' AND second_name  LIKE '{second_name}%'"
    cursor.execute(sql_command)
    result = cursor.fetchall()
    cursor.close()
    return result


@ router.get("/find_by_login")
async def find_by_login(login, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    print(login)
    sql_command = f"""SELECT user_id, user_name, first_name, second_name
      FROM users
      WHERE user_name LIKE '{login}%'"""
    cursor.execute(sql_command)
    result = cursor.fetchall()
    cursor.close()
    return result


@ router.post("/new_user")
async def new_user(new_user: UpdateUserModel, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    try:
        print("Было 1")
        sql_command: str = "INSERT INTO users (user_name, first_name, second_name, password) VALUES (%s, %s, %s, %s) RETURNING user_id"
        if new_user.password:
            password: str = hashlib.sha256(
                new_user.password.encode()).hexdigest()
        print("Было 2")
        data: tuple = (new_user.user_name, new_user.first_name,
                       new_user.second_name, password)
        cursor.execute(sql_command, data)
        user_id = cursor.fetchone()[0]
        cursor.connection.commit()
    except Exception as e:
        print(e)
        cursor.connection.rollback()
        cursor.close()
        raise HTTPException(
            status_code=400, detail="Can't create user")
    cursor.close()
    return {"message": f"User {user_id} created successfully"}


@ router.put("/update")
async def update(user_id: int, updated_user: UpdateUserModel, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor), jwt_id=Depends(get_current_user)):
    if jwt_id != user_id:
        return HTTPException(
            status_code=402, detail="Invalid authentication credentials")
    try:
        if updated_user.password:
            updated_user.password = hashlib.sha256(
                updated_user.password.encode()).hexdigest()
        print(user_id)
        updated_user_dict = UpdateUserModel.model_dump(
            updated_user, exclude_none=True)

        columns_to_update = ', '.join(
            [f"{key} = %s" for key in updated_user_dict.keys()])
        sql = f"UPDATE users SET {columns_to_update} WHERE user_id = %s"
        values = list(updated_user_dict.values())
        cursor.execute(sql, values + [user_id])
        cursor.connection.commit()
    except Exception as e:
        print(e)
        cursor.connection.rollback()
        cursor.close()
        return {"message": "User updated unsuccessfully"}
    cursor.close()
    return {"message": "User updated successfully"}


@ router.delete("/delete")
async def delete_by_id(user_id: int, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor), jwt_id=Depends(get_current_user)):
    if jwt_id != user_id:
        return HTTPException(
            status_code=402, detail="Invalid authentication credentials")
    try:
        id_in_tuple: tuple = (user_id,)
        sql_command = "DELETE FROM users WHERE user_id=%s"
        cursor.execute(sql_command, id_in_tuple)
        print(cursor.fetchone())
        cursor.connection.commit()
    except Exception as e:
        print(e)
        cursor.connection.rollback()
        cursor.close()
        return {"message": "User deleted unsuccessfully"}
    cursor.close()
    return {"message": "User deleted successfully"}


@ router.post("/login")
async def login(credentials: HTTPBasicCredentials = Depends(HTTPBasic()), cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    cursor.execute(
        "SELECT user_id, user_name, password FROM users WHERE user_name = %s", (credentials.username,))
    user = cursor.fetchone()
    cursor.close()
    if user and user[1] != credentials.username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username",
            headers={"WWW-Authenticate": "Basic"},
        )
    hashed_password = hashlib.sha256(credentials.password.encode()).hexdigest()
    print(user)
    if hashed_password != user[2]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Basic"},
        )
    user_id = user[0]
    expiration = datetime.now() + timedelta(minutes=20)
    token_data = {"sub": user_id, "exp": expiration}
    access_token = jwt.encode(token_data, "secret_key", algorithm="HS256")
    return {"access_token": access_token, "token_type": "bearer"}
