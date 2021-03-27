import sqlite3
import os
import hashlib
import binascii

from helpers import configuration
from helpers import statusmessage


def create_database():
    if not os.path.exists(configuration.DB_NAME):
        db_connection = sqlite3.connect(configuration.DB_NAME)
        cursor = db_connection.cursor()

        with open('schema.sql', 'r') as file_open:
            cursor.executescript(file_open.read())

        db_connection.close()


def add_newuser(name: str, email: str, pw: str) -> tuple:
    """
    returns (bool, statusmessage)
    """
    db_connection = sqlite3.connect(configuration.DB_NAME)
    try:
        cursor = db_connection.cursor()
        if __is_email_unique__(cursor, email):
            stmt = 'INSERT INTO User (name, email, pw) VALUES ("{}", "{}", "{}")'
            pw_hash = __hash_passwort__(pw)
            cursor.execute(stmt.format(name, email, pw_hash))
            db_connection.commit()
            return True, statusmessage.USER_ADDED_SUCCESSFULLY
        return False, statusmessage.EMAIL_ALREADY_EXISTS
    except Exception:
        return False, statusmessage.UNKNOWN_ERROR
    finally:
        db_connection.close()


def get_user_by_id(_id: int) -> tuple:
    """
    returns none if there is no user with this id
    """
    db_connection = sqlite3.connect(configuration.DB_NAME)
    cursor = db_connection.cursor()
    stmt = 'SELECT * FROM User WHERE id = {}'
    query = cursor.execute(stmt.format(_id))
    result = query.fetchone()
    return result


def get_user_by_email(email: str) -> tuple:
    """
    returns none if there is no user with this email
    """
    db_connection = sqlite3.connect(configuration.DB_NAME)
    cursor = db_connection.cursor()
    stmt = 'SELECT * FROM User WHERE email = "{}"'
    query = cursor.execute(stmt.format(email))
    result = query.fetchone()
    return result


def __is_email_unique__(cursor: sqlite3.Cursor, email: str) -> bool:
    stmt = 'SELECT * FROM User WHERE email = "{}"'
    query = cursor.execute(stmt.format(email))
    result = query.fetchone()
    return True if not result else False


def __hash_passwort__(pw: str) -> str:
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    # print("salt: ",salt)
    pw_hash = hashlib.pbkdf2_hmac("sha512", pw.encode("utf-8"), salt, 100000)
    pw_hash = binascii.hexlify(pw_hash)
    # print("pw_hash:",pw_hash)
    return (salt+pw_hash).decode("ascii")


def __verify_password__(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password
