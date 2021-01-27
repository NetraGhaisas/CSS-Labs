import random
def generate():
    captcha = ''
    r1 = random.randint(5,10)
    for i in range(r1):
        r2 = random.randint(1,10)
        if r2<6:
            r3 = str(random.randint(1,10))
        else:
            r3 = chr(random.randint(1,26)+96)
        captcha += r3
    return captcha


def text_captcha():
    captcha = generate()
    print(captcha)
    user_captcha = input('Enter the text shown above: ')
    if user_captcha == captcha:
        print('Correct!')
    else:
        print('Incorrect!')


text_captcha()
