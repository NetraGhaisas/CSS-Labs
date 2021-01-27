import random
from captcha.image import ImageCaptcha
import matplotlib.pyplot as plt

def generate_math():
    numbers = ['zero','one','two','three','four','five','six','seven','eight','nine']
    operators = ['+','-','*']
    i1 = random.randint(0,9)
    i2 = random.randint(0,9)
    n1 = numbers[i1]
    n2 = numbers[i2]
    op = random.randint(0,2)
    operator = operators[op]
    ans = i1+i2 if operator=='+' else i1-i2 if operator=='-' else i1*i2
    calc_captcha = ' '.join([str(n1),operator,str(n2)])
    return calc_captcha, ans

def generate_image(captcha):
    image_captcha = ImageCaptcha(width=len(captcha)*40,height=80)
    image = image_captcha.generate_image(captcha)

    # noise curve
    image_captcha.create_noise_curve(image, image.getcolors())
    # noise dots
    image_captcha.create_noise_dots(image, image.getcolors())

    # save image to png file
    image_file = "./captcha_math.png"
    image_captcha.write(captcha, image_file)
    print(image_file + " created")
    return image
    

class MathCaptcha:
    def __init__(self):
        self.fig = None
        self.image = None

    def show_image(self,reload=False):
        # Display the image in a matplotlib viewer.
        if reload and self.fig != None:
            plt.close(self.fig)
        self.fig = plt.figure(figsize=(5,3))
        plt.imshow(self.image)
        plt.axis('off')
        plt.show(block=False)

    def math_captcha(self):
        regen = False
        while(True):
            expr, ans = generate_math()
            self.image = generate_image(expr)
            self.show_image(reload=regen)
            regen = False
            # print(expr,ans)
            result = input('Press * to reload captcha\nEnter numeric result of given mathematical expression: ')
            
            if result == '*':
                regen = True
                continue
            else:
                try:
                    if int(result) == ans:
                        print('Correct!')
                    else:
                        print('Incorrect!')
                except Exception as e:
                    print('Error! Please enter numeric value')
                break       


MathCaptcha().math_captcha()
