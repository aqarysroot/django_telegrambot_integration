import secrets
import string


def generate_token():
    characters = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(characters) for _ in range(60))

    return token

def format_message(name, message):
    return f"{name}, я получил от тебя сообщение:\n {message}"
