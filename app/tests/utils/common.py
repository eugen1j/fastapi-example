import random
import string


def random_lower_string(length: int = 32) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))


def random_email(user_length: int = 20, domain_length: int = 8) -> str:
    return (
        f"{random_lower_string(user_length)}@{random_lower_string(domain_length)}.com"
    )


def random_string(length: int = 32) -> str:
    symbols = string.digits + string.ascii_letters + string.punctuation
    return "".join(random.choices(symbols, k=length))
