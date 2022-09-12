import os


def get_refresh_token(filename: str, check_file: bool = True) -> str:
    if check_file and os.path.exists(filename):
        with open(filename, "r", encoding="UTF-8") as file:
            return file.read().strip()
    else:
        refresh_token = input("Refresh Token: ")
        with open(filename, "w", encoding="UTF-8") as file:
            file.write(refresh_token)
        return refresh_token
