from PIL import Image, ImageOps
import os


def MakeIcon(file):
    PATH = os.path.dirname(os.path.realpath(__file__))
    mask = Image.open(os.path.join(PATH, "images", "mask.png")).convert('L')
    im = Image.open(os.path.join(PATH, "images", file))
    output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    return output


def get_speciality():
    return 'Искусственный интеллект'


def get_faculty():
    return 'ФИТиУ'


def edit():
    return None


def get_full_name():
    return 'Якубович Никита'


def get_email():
    return '0101010100@gmail.com'


def get_Home_Phone():
    return '80(17)-01-01-012'


def get_Mobile():
    return '+375(29)111-11-11'


def get_Adress():
    return 'Dzerzhinskogo 95, Minsk'


def get_number_course():
    return 'Курс: 3'


def get_social_networks():
    return 'Instagram: @_nkch_n'


def get_other_info_1():
    return 'Other info'


def get_other_info_2():
    return 'Other info'


def get_rating():
    return 'Рейтинг: 4'


def get_skills():
    return {'Front-end': 4, 'Soft Skills': 3, 'Hard Skills': 4}


def get_note():
    return ''' Пусть,
оскалясь короной,
вздымает британский лев вой.
Коммуне не быть покорённой.
Левой!
Левой!
Левой!'''
