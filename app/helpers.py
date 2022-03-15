import random
import string


def generate_random_password(length):
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    symbols = ":;!?"
    population = lower + upper + num + symbols

    return "".join(random.sample(population, length))
