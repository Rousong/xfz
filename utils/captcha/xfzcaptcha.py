import os
import random
import string
import time
# Image: 画板，ImageDraw: 画笔，ImageFont: 画笔的字体
from PIL import Image, ImageDraw, ImageFont


class Captcha(object):
    """验证码类"""
    # 字体文件
    font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'FreeSerifBoldItalic.ttf')
    number = 4  # 验证码位数
    size = (100, 40)  # 验证码图片宽、高
    bgcolor = (0, 0, 0)  # 验证码图片颜色rgb
    random.seed(int(time.time()))
    fontcolor = (random.randint(200, 255), random.randint(100, 255),
                 random.randint(100, 255))  # 字体颜色
    fontsize = 20  # 字体大小
    linecolor = (random.randint(0, 250), random.randint(0, 255),
                 random.randint(0, 250))  # 干扰线颜色
    draw_line = True  # 是否加入干扰线
    draw_point = True  # 是否加入干扰点
    line_number = 3  # 加入干扰线条数
    SOURCE = string.ascii_letters + string.digits  # 用于生成验证码的字符串，大小写字母+数字

    @classmethod
    def gene_text(cls):
        """生成验证码字符串"""
        return ''.join(random.sample(cls.SOURCE, cls.number))

    @classmethod
    def __gene_line(cls, draw, width, height):
        """绘制干扰线"""
        begin = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([begin, end], fill=cls.linecolor)

    @classmethod
    def __gene_points(cls, draw, point_chance, width, height):
        """绘制干扰点"""
        chance = min(100, max(0, int(point_chance)))
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    @classmethod
    def gene_code(cls):
        width, height = cls.size
        image = Image.new('RGBA', (width, height), cls.bgcolor)  # 生成一个画板对象
        font = ImageFont.truetype(cls.font_path, cls.fontsize)  # 创建字体对象
        draw = ImageDraw.Draw(image)  # 创建画笔对象
        text = cls.gene_text()
        font_width, font_height = font.getsize(text)
        draw.text(((width-font_width)/2, (height-font_height)/2), text,
                  font=font, fill=cls.fontcolor)
        if cls.draw_line:
            for x in range(cls.line_number):
                cls.__gene_line(draw, width, height)
        if cls.draw_point:
            cls.__gene_points(draw, 10, width, height)
        return text, image
