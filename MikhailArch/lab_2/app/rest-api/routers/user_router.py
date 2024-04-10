from fastapi import APIRouter, Depends
from utils.postgres_connector import PostgresConnector
import psycopg2
from models.user import UpdateUserModel
import hashlib

router = APIRouter()

connection = PostgresConnector(db_name="messenger_db")


@router.get("/find_by_name")
async def find_by_name(first_name: str, second_name: str, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    print(first_name, second_name)
    sql_command = f"SELECT user_id, user_name, first_name, second_name from users " \
        f"WHERE first_name LIKE '{
            first_name}%' AND second_name  LIKE '{second_name}%'"
    cursor.execute(sql_command)
    result = cursor.fetchall()
    cursor.close()
    return result


@router.get("/find_by_login")
async def find_by_login(login, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    print(login)
    sql_command = f"""SELECT user_id, user_name, first_name, second_name
      FROM users
      WHERE user_name LIKE '{login}%'"""
    cursor.execute(sql_command)
    result = cursor.fetchall()
    cursor.close()
    return result


@router.get("/user_info")
async def get_user_info(id: int, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    sql_command = \
        f"SELECT user_id, user_name, first_name, second_name from users "\
        f"WHERE user_id = {id}"
    print(sql_command)
    cursor.execute(sql_command)
    result = cursor.fetchall()
    cursor.close()
    return result


@router.post("/new_user")
async def new_user(new_user: UpdateUserModel, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    try:
        sql_command: str = "INSERT INTO users (user_name, first_name, second_name, password) VALUES (%s, %s, %s, %s) RETURNING user_id"
        if new_user.password:
            password: str = hashlib.sha256(
                new_user.password.encode()).hexdigest()
        data: tuple = (new_user.user_name, new_user.first_name,
                       new_user.second_name, password)
        cursor.execute(sql_command, data)
        cursor.connection.commit()
    except Exception as e:
        print(e)
        cursor.connection.rollback()
        cursor.close()
        return {"result": "User created unsuccessfully"}
    cursor.close()
    return {"message": "User created successfully"}


@router.put("/update")
async def find_by_prefix(user_id: int, updated_user: UpdateUserModel, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
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


@router.delete("/delete")
async def delete_by_id(user_id: int, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    try:
        id_in_tuple: tuple = (user_id,)
        sql_command = "DELETE FROM users WHERE user_id=%s"
        cursor.execute(sql_command, id_in_tuple)
        cursor.connection.commit()
    except Exception as e:
        print(e)
        cursor.connection.rollback()
        cursor.close()
        return {"message": "User deleted unsuccessfully"}
    cursor.close()
    return {"message": "User deleted successfully"}
