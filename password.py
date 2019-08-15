import random

def password_generator(count=8):
    arr = ['q', 'Q', 'w', 'W', 'e', 'E', 'r', 'R', 't', 'T', 'y', 'Y', 'u', 'U',
           'i', 'I', 'o', 'O', 'p', 'P', 'a', 'A', 's', 'S', 'd', 'D', 'f', 'F',
           'g', 'G', 'h', 'H', 'j', 'J', 'k', 'K', 'l', 'L', 'z', 'Z', 'x', 'X',
           'c', 'C', 'v', 'V', 'b', 'B', 'n', 'N', 'm', 'M',
           '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
           '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '=', '+',
           '?', ',', '.', '[', ']', '{', '}']
    #random.shuffle(arr)
    #passw = []
    #for i in range(count):
    #    passw.append(random.choice(arr))
    #print("".join(passw))
    print("".join(random.sample(arr, count)))

if __name__ == '__main__':
    password_generator()
    print('---***---')
    password_generator(15)  

while True:
    n = int(input('Введике кол-во символов в пароле: '))
    password_generator(n)
