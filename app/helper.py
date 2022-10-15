import sqlite3


def get_refresh_token(wrong_token: bool = False) -> str:
    with sqlite3.connect("auth.db") as connection:
        cursor = connection.cursor()

        cursor.execute("SELECT value FROM auth_data WHERE key='refresh_token'")
        data = cursor.fetchone()

        if data is None or wrong_token:
            refresh_token = input()

            cursor.execute("UPDATE auth_data SET value=? WHERE key='refresh_token'", [refresh_token])
            connection.commit()

            return refresh_token
        else:
            return data[0]
