import random
from captcha.image import ImageCaptcha
import matplotlib.pyplot as plt

def generate_text():
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

def generate_index(n):
    start = random.randint(1,n-1)
    end = random.randint(start+1,n)
    return start,end

def generate_image(captcha):
    image_captcha = ImageCaptcha(width=len(captcha)*40,height=80)
    image = image_captcha.generate_image(captcha)

    # Add noise curve
    image_captcha.create_noise_curve(image, image.getcolors())

    # Add noise dots
    image_captcha.create_noise_dots(image, image.getcolors())

    # Save the image to a png file.
    image_file = "./captcha_"+captcha + ".png"
    image_captcha.write(captcha, image_file)
    print(image_file + " created")
    return image
    

class SubCaptcha:
    def __init__(self):
        self.fig = None
        self.image = None
        self.captcha = None

    def show_image(self,reload=False):
        # Display the image in a matplotlib viewer.
        if reload and self.fig != None:
            plt.close(self.fig)
        self.fig = plt.figure(figsize=(5,3))
        plt.imshow(self.image)
        plt.axis('off')
        plt.show(block=False)

    def sub_captcha(self):
        regen = False
        while(True):
            self.captcha = generate_text()
            self.image = generate_image(self.captcha)
            self.show_image(reload=regen)
            regen = False
            print(self.captcha)
            self.start, self.end = generate_index(len(self.captcha))
            user_captcha = input('Press * to reload captcha\nEnter the string from positions '+str(self.start)+' to '+str(self.end)+' shown in the text above: ')
            if user_captcha == '*':
                regen = True
                continue
            else:
                if user_captcha == self.captcha[self.start-1:self.end]:
                    print('Correct!')
                else:
                    print('Incorrect!')
                break

SubCaptcha().sub_captcha()