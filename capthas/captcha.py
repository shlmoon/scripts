# encoding:utf-8

from PIL import Image, ImageDraw, ImageFont
import random
import string
import StringIO
import os
from math import ceil
current_path = os.getcwd()


class CaptchaObj(object):
    def __init__(self, **kwargs):
        self._checkcode = ''
        self.chtype = kwargs.get('type', 'number')
        self.img_width = kwargs.get('img_width', 150)
        self.img_height = kwargs.get('img_height', 30)

    @property
    def chtype(self):
        return self._chtype

    @chtype.setter
    def chtype(self, _type):
        if _type not in ['number', 'word']:
            raise ValueError('Type Error')
        self._chtype = _type

    @property
    def checkcode(self):
        return self._checkcode

    @checkcode.setter
    def checkcode(self, answer):
        self._checkcode = str(answer)

    def _get_font_size(self):
        """  将图片高度的80%作为字体大小
        """
        s1 = int(self.img_height * 0.8)
        s2 = int(self.img_width / len(self.checkcode))
        return int(min((s1, s2)) + max((s1, s2)) * 0.05)

    # 英文单词验证码
    def word(self):
        def _get_words():
            return ''.join(
                random.choice(
                    string.ascii_letters + string.digits
                ) for _ in range(6)
            )
        code = random.choice(self._get_words())
        self.checkcode = code
        return code

    # 数字公式验证码
    def number(self):
        m, n = 1, 100
        x = random.randrange(m, n)
        y = random.randrange(m, n)
        if x < y:
            x, y = y, x
        if random.randrange(0, 2):
            code = "%s - %s = ?" % (x, y)
            z = x - y
        else:
            code = "%s + %s = ?" % (x, y)
            z = x + y
        self.checkcode = z
        return code

    def _yield_code(self):
        fun = getattr(self, self.chtype.lower())
        return fun()

    def display(self):
        self.background = (
            random.randrange(230, 255),
            random.randrange(230, 255),
            random.randrange(230, 255)
        )
        im = Image.new(
            'RGB',
            (self.img_width, self.img_height),
            self.background
        )

        # creat
        font_path = os.path.join(current_path, 'timesbi.ttf')
        font_color = ['black', 'darkblue', 'darkred']
        font_size = self._get_font_size()
        draw = ImageDraw.Draw(im)
        for i in range(random.randrange(2, 4)):
            line_color = (
                random.randrange(0, 255),
                random.randrange(0, 255),
                random.randrange(0, 255)
            )
            xy = (
                random.randrange(0, int(self.img_width * 0.2)),
                random.randrange(0, self.img_height),
                random.randrange(3 * self.img_width / 4, self.img_width),
                random.randrange(0, self.img_height)
            )
            draw.line(xy, fill=line_color, width=int(font_size * 0.1))

        code = self._yield_code()
        j = int(font_size * 0.3)
        k = int(font_size * 0.5)
        x = random.randrange(j, k)
        for i in code:
            m = int(len(code))
            y = random.randrange(1, 3)
            if i in ('+', '-', '*', '=', '?'):
                # 对计算符号等特殊字符放大处理
                m = ceil(self.font_size * 0.8)
            else:
                # 字体大小变化量,字数越少,字体大小变化越多
                m = random.randrange(
                    0, int(45 / font_size) + int(font_size / 5)
                )
            font = ImageFont.truetype(
                font_path.replace('\\', '/'),
                font_size + int(ceil(m))
            )
            draw.text(
                (x, y),
                i,
                font=font,
                fill=random.choice(font_color)
            )
            x += font_size * 0.9

        del x
        del draw
        buf = StringIO.StringIO()
        im.save(buf, 'gif')
        im.close()
        return buf.getvalue()

    def validate(self, code, _checkcode):
        """
        validate user's input
        """
        if not code:
            return False
        return code.lower() == str(_checkcode).lower()
