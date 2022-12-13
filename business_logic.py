from PIL import Image, ImageOps
import os


class UserInfo:
    is_teacher: bool
    speciality = "Специальность"
    faculty = "Факультет"
    full_name = "ФИО"
    email = "E-mail"
    home_phone = "Home Phone"
    mobile_phone = "Mobile Phone"
    address = "Address"
    number_course = "Course number"
    social_media = "Social Media"
    bio = "Bio"
    other1 = "Other info"
    other2 = "Other info"
    rating = "Rating"
    skills = {'Front-end': 0, 'Soft Skills': 0, 'Hard Skills': 0}
    profile_pic = 'profile_pic.jpg'

    @staticmethod
    def MakeIcon(file):
        PATH = os.path.dirname(os.path.realpath(__file__))
        mask = Image.open(os.path.join(PATH, "images", "mask.png")).convert('L')
        im = Image.open(os.path.join(PATH, "images", file))
        output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        return output

    def get_speciality(self):
        return self.speciality

    def get_faculty(self):
        return self.faculty

    def edit(self):
        pass

    def get_full_name(self):
        return self.full_name

    def get_email(self):
        return self.email

    def get_Home_Phone(self):
        return self.home_phone

    def get_Mobile(self):
        return self.mobile_phone

    def get_Address(self):
        return self.address

    def get_number_course(self):
        return self.number_course

    def get_social_networks(self):
        return self.social_media

    def get_other_info_1(self):
        return self.other1

    def get_other_info_2(self):
        return self.other2

    def get_rating(self):
        return self.rating

    def get_skills(self):
        return self.skills

    def get_note(self):
        return self.bio

    def change_user(self, user_id):
        if user_id == 0:
            self.speciality = "Искусственный интеллект"
            self.faculty = "ФИТиУ"
            self.full_name = "Якубович Никита"
            self.email = "nikita_yakub@gmail.com"
            self.home_phone = "999 99 99"
            self.mobile_phone = "+375 29 111 11 11"
            self.address = "г. Минск, пр. Дзержинского, д. 35"
            self.number_course = "Курс: 3"
            self.social_media = "Instagram: @_nkch_n"
            self.bio = '''
            Пусть,
            оскалясь короной,
            вздымает британский лев вой.
            Коммуне не быть покорённой.
            Левой!
            Левой!
            Левой!'''
            self.other1 = ""
            self.other2 = ""
            self.rating = "Рейтинг: 4"
            self.skills = {'Front-end': 4, 'Soft Skills': 3, 'Hard Skills': 4}
        elif user_id == 1:
            self.speciality = "Кафедра ИИТ"
            self.faculty = "ФИТиУ"
            self.full_name = "Петров Пётр Петрович"
            self.email = "petr_petr@gmail.com"
            self.home_phone = "312 83 22"
            self.mobile_phone = "+375 29 812 92 22"
            self.address = "г. Минск, ул. Платонова, д. 1"
            self.number_course = "Образование: Политех, 1999"
            self.social_media = "twitter.com/petr_petr"
            self.bio = """
            Падение - это не провал.
            Провал - это провал.
            Падение - это где упал.
            """
            self.other1 = ""
            self.other2 = ""
            self.rating = "0% пересдач"
            self.skills = {'Знания': 1, 'Преподавание': 3, 'Личность': 4}
        else:
            self.speciality = "Специальность"
            self.faculty = "Факультет"
            self.full_name = "ФИО"
            self.email = "E-mail"
            self.home_phone = "Home Phone"
            self.mobile_phone = "Mobile Phone"
            self.address = "Address"
            self.number_course = "Course number"
            self.social_media = "Social Media"
            self.bio = "Bio"
            self.other1 = "Other info"
            self.other2 = "Other info"
            self.rating = "Rating"
            self.skills = {'Front-end': 0, 'Soft Skills': 0, 'Hard Skills': 0}

    def import_json(self, json_data: dict, is_teacher):
        if is_teacher:
            self.change_user(1)
        else:
            self.change_user(0)
        self.full_name = json_data['lastName'] + " " + json_data['firstName'] + " " + json_data['middleName']
        self.email = json_data['email']
        if 'group' in json_data.keys():
            group_info = json_data['group']
            group_name = group_info['name']
            group_course = group_info['course']
            self.number_course = "Курс: " + str(group_course)
            self.other1 = "Группа: " + group_name
