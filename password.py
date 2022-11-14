import random
import string


def password_generator(count: int = 8, with_punctuations: bool = False) -> str:
    letters = string.ascii_letters + string.digits
    if with_punctuations:
        letters += string.punctuation
    return "".join(random.sample(letters, count))


if __name__ == '__main__':
    print('--- START ---')
    while True:
        n = int(input('Введите кол-во символов в пароле: '))
        print(password_generator(n))
