from fastapi import status, UploadFile
from fastapi.exceptions import HTTPException
from sqlalchemy import text, Connection
from sqlalchemy.exc import SQLAlchemyError
from schemas.auth_schema import UserData, UserDataPASS

async def get_user_by_email(conn : Connection, email : str) -> UserData :
    try :
        query = 'select id, name, email from user where email = :email'
        result = await conn.execute(text(query).bindparams(email = email))

        if result.rowcount == 0 :
            return None
        
        row = result.fetchone()
        user = UserData(id = row[0], name = row[1], email = row[2])
        result.close()
        return user
    except SQLAlchemyError as e :
        print(e)
        conn.rollback()
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'해당 ID {id}는(은) 존재하지 않습니다.')

async def get_password_by_email(conn : Connection, email : str) -> UserDataPASS :
    try :
        query = 'select id, name, email, hashed_password from user where email = :email'
        result = await conn.execute(text(query).bindparams(email = email)) 

        if result.rowcount == 0 :
            return None
        
        row = result.fetchone()
        user = UserDataPASS(id = row[0], name = row[1], email = row[2], hashed_password = row[3])
        result.close()
        return user
    except SQLAlchemyError as e :
        print(e)
        conn.rollback()
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = '로그인 정보가 일치하지 않습니다.')

async def register_user(conn : Connection, name : str, email : str, hashed_password : str) :
    try :
        query = f'insert into user (name, email, hashed_password) values ("{name}", "{email}", "{hashed_password}")'
        await conn.execute(text(query))
        await conn.commit()
    except SQLAlchemyError as e :
        print(e)
        conn.rollback()
        raise HTTPException(status_code = status.HTTP_503_SERVICE_UNAVAILABLE, detail = '요청하신 서비스가 잠시 내부적으로 문제가 발생했습니다.')