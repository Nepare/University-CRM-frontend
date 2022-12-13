import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from tkinter import simpledialog
import customtkinter as ctk
import os
from PIL import Image, ImageTk
import requests
from functools import partial
from business_logic import UserInfo

PATH = os.path.dirname(os.path.realpath(__file__))
DEFAULT_FONT = ""

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class StartingScreen(ctk.CTk):
    WIDTH = 911
    HEIGHT = 550
    is_teacher: bool = False
    debug_mode: bool = False

    def __init__(self):
        super().__init__()

        self.title("Фронтенд системы управления университетами")
        self.center_app_on_screen()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.email = tk.StringVar()
        self.password = tk.StringVar()
        self.logged_in = ""

        self.initUI()

    def center_app_on_screen(self):
        w = self.WIDTH
        h = self.HEIGHT
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) / 2 + 75
        y = (sh - h) / 2
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def on_closing(self, event=0):
        self.destroy()

    def initUI(self):
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=30)
        self.columnconfigure(0, weight=1)

        self.navigation_bar = ctk.CTkFrame(master=self, fg_color="#212529", height=40, corner_radius=0)
        self.navigation_bar.grid(row=0, sticky="nsew")

        self.content_frame = ctk.CTkFrame(master=self)
        self.content_frame.grid(row=1, sticky="nsew")
        self.content_frame.rowconfigure(0, weight=1)
        self.content_frame.columnconfigure(0, weight=1)

        # =========================== NAVIGATION BAR ===========================

        self.navigation_bar.rowconfigure(0, weight=1)
        self.navigation_bar.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.btn_home = ctk.CTkButton(master=self.navigation_bar, text="Home", corner_radius=0, font=("Segoe UI", -13),
                                      fg_color="#212529", bg_color="#eeeeee", command=self.navigate_home, state="disabled")
        self.btn_home.grid(row=0, column=0, sticky="nsew")

        self.btn_group = ctk.CTkButton(master=self.navigation_bar, text="Group", corner_radius=0,
                                       font=("Segoe UI", -13), fg_color="#212529", bg_color="#eeeeee",
                                       command=self.navigate_group, state="disabled")
        self.btn_group.grid(row=0, column=1, sticky="nsew")

        self.btn_work = ctk.CTkButton(master=self.navigation_bar, text="Work Materials", corner_radius=0,
                                      font=("Segoe UI", -13), fg_color="#212529", bg_color="#eeeeee",
                                      command=self.navigate_work_materials, state="disabled")
        self.btn_work.grid(row=0, column=2, sticky="nsew")

        self.btn_timetable = ctk.CTkButton(master=self.navigation_bar, text="Timetable", corner_radius=0,
                                           font=("Segoe UI", -13), fg_color="#212529", bg_color="#eeeeee",
                                           command=self.navigate_timetable, state="disabled")
        self.btn_timetable.grid(row=0, column=3, sticky="nsew")

        self.btn_user = ctk.CTkButton(master=self.navigation_bar, text="SELECT USER", corner_radius=0, border_width=1,
                                      font=("Segoe UI", -13), fg_color="#212529", border_color="white", height=20,
                                      command=self.navigate_select_user)
        self.btn_user.grid(row=0, column=5, sticky="nse", padx=5, pady=5)

        # ===========================                ===========================

        self.init_authorization_screen()
        self.init_user_info_UI()
        self.init_timetable_screen()
        self.hide_all_windows()
        self.navigate_select_user()

    def init_user_info_UI(self):
        self.user_info = ctk.CTkFrame(master=self.content_frame, fg_color='#E8E8E8')

        self.user_info.columnconfigure((0, 4), weight=1)
        self.user_info.columnconfigure((1, 2, 3), weight=5)
        self.user_info.rowconfigure((0, 1), weight=1)

        # =========================== user faculty\image            ===========================
        self.user_info_profile = ctk.CTkFrame(master=self.user_info, border_color="#c5c7c4", border_width=0.5,
                                              fg_color='#F8F9F9')
        self.user_info_profile.grid(row=0, column=1, sticky="nsew", padx=5, pady=(10, 5))

        image = userinfo.MakeIcon(userinfo.profile_pic)
        icon_image = ctk.CTkImage(light_image=image, size=(image.size[0] / 1.5, image.size[1] / 1.5))
        self.label_icon = ctk.CTkLabel(master=self.user_info_profile, text='', image=icon_image)
        self.label_icon.pack(pady=15)
        self.speciality = ctk.CTkLabel(master=self.user_info_profile, text=userinfo.get_speciality(),
                                       text_color='grey', font=("Segoe UI", 13))
        self.speciality.pack()
        self.faculty = ctk.CTkLabel(master=self.user_info_profile, text=userinfo.get_faculty(),
                                    text_color='grey', font=("Segoe UI", 13))
        self.faculty.pack()
        self.button_edit = ctk.CTkButton(master=self.user_info_profile, text='Изменить', font=("Segoe UI", 13),
                                         fg_color='#0090DE', text_color='white',
                                         command=userinfo.edit).pack(pady=15)

        # =========================== user contacts            ===========================
        self.user_info_basic = ctk.CTkFrame(master=self.user_info, border_color="#c5c7c4", border_width=0.5,
                                            fg_color='#F8F9F9')
        self.user_info_basic.grid(row=0, column=2, columnspan=2, sticky="nsew", padx=5, pady=(10, 5))
        self.user_info_basic.columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(master=self.user_info_basic, text='Full Name', font=("Segoe UI", 13)).grid(column=0, row=0,
                                                                                                padx=30, pady=10,
                                                                                                sticky='w')
        ctk.CTkLabel(master=self.user_info_basic, text='Email', font=("Segoe UI", 13)).grid(column=0, row=2, padx=30,
                                                                                            pady=10, sticky='w')
        ctk.CTkLabel(master=self.user_info_basic, text='Home Phone', font=("Segoe UI", 13)).grid(column=0, row=4,
                                                                                                 padx=30, pady=10,
                                                                                                 sticky='w')
        ctk.CTkLabel(master=self.user_info_basic, text='Mobile Phone', font=("Segoe UI", 13)).grid(column=0, row=6,
                                                                                                   padx=30, pady=10,
                                                                                                   sticky='w')
        ctk.CTkLabel(master=self.user_info_basic, text='Address', font=("Segoe UI", 13)).grid(column=0, row=8, padx=30,
                                                                                              pady=10, sticky='w')

        for i in [1, 3, 5, 7, 9]:
            ttk.Separator(master=self.user_info_basic, orient='horizontal').grid(column=0, columnspan=3, row=i,
                                                                                 sticky='ewns')

        self.full_name = ctk.CTkLabel(master=self.user_info_basic, text=userinfo.get_full_name(), font=("Segoe UI", 13),
                                      text_color='grey')
        self.full_name.grid(column=2, row=0, sticky='w', padx=165, pady=10)
        self.lbl_email = ctk.CTkLabel(master=self.user_info_basic, text=userinfo.get_email(), font=("Segoe UI", 13),
                                      text_color='grey')
        self.lbl_email.grid(column=2, row=2, sticky='w', padx=165, pady=10)
        self.h_phone = ctk.CTkLabel(master=self.user_info_basic, text=userinfo.get_Home_Phone(), font=("Segoe UI", 13),
                                    text_color='grey')
        self.h_phone.grid(column=2, row=4, sticky='w', padx=165, pady=10)
        self.m_phone = ctk.CTkLabel(master=self.user_info_basic, text=userinfo.get_Mobile(), font=("Segoe UI", 13),
                                    text_color='grey')
        self.m_phone.grid(column=2, row=6, sticky='w', padx=165, pady=10)
        self.address = ctk.CTkLabel(master=self.user_info_basic, text=userinfo.get_Address(), font=("Segoe UI", 13),
                                    text_color='grey')
        self.address.grid(column=2, row=8, sticky='w', padx=165, pady=10)

        # =========================== user other info           ===========================
        self.user_info_uni = ctk.CTkFrame(master=self.user_info, border_color="#c5c7c4", border_width=0.5,
                                          fg_color='#F8F9F9')
        self.user_info_uni.grid(row=1, column=1, sticky="nsew", padx=5, pady=(5, 10))
        self.user_info_uni.columnconfigure((0, 1, 2, 3), weight=1)

        for i in [1, 3, 5, 7, 9]:
            ttk.Separator(master=self.user_info_uni, orient='horizontal').grid(column=1, columnspan=2, row=i,
                                                                               sticky='ewns')

        self.course = ctk.CTkLabel(master=self.user_info_uni, text=userinfo.get_number_course(), font=("Segoe UI", 13))
        self.course.grid(column=2, row=0, sticky='ew', padx=40, pady=8)
        self.rating = ctk.CTkLabel(master=self.user_info_uni, text=userinfo.get_rating(), font=("Segoe UI", 13))
        self.rating.grid(column=2, row=2, sticky='ew', padx=40, pady=8)
        self.social_networks = ctk.CTkLabel(master=self.user_info_uni, text=userinfo.get_social_networks(),
                                            font=("Segoe UI", 13))
        self.social_networks.grid(column=2, row=4, sticky='ew', padx=40, pady=8)
        self.other1 = ctk.CTkLabel(master=self.user_info_uni, text=userinfo.get_other_info_1(), font=("Segoe UI", 13))
        self.other1.grid(column=2, row=6, sticky='ew', padx=40, pady=8)
        self.other2 = ctk.CTkLabel(master=self.user_info_uni, text=userinfo.get_other_info_2(), font=("Segoe UI", 13))
        self.other2.grid(column=2, row=8, sticky='ew', padx=40, pady=8)

        # =========================== user skills          ===========================
        self.user_info_parameters = ctk.CTkFrame(master=self.user_info, border_color="#c5c7c4", border_width=0.5,
                                                 fg_color='#F8F9F9')
        self.user_info_parameters.grid(row=1, column=2, sticky="nsew", padx=5, pady=(5, 10))

        ctk.CTkLabel(master=self.user_info_parameters, text='ASSIGNMENT:', font=("Segoe UI", 13),
                     text_color='#0090DE').pack(pady=10, padx=10, anchor='w')
        self.list_of_keys = []
        self.list_of_progressbars = []
        list_of_skills = userinfo.get_skills()
        for key, value in list_of_skills.items():
            key1 = ctk.CTkLabel(master=self.user_info_parameters, text=key, font=("Segoe UI", 11))
            key1.pack(anchor='w', padx=10)
            self.list_of_keys.append(key1)
            pg = ctk.CTkProgressBar(master=self.user_info_parameters, height=12, progress_color='#0090DE',
                                    fg_color='#E8E8E8', corner_radius=4)
            pg.pack(padx=(10, 10), pady=(0, 10))
            pg.set(value / 5)
            self.list_of_progressbars.append(pg)

        # =========================== user notes         ===========================
        self.user_info_bio = ctk.CTkFrame(master=self.user_info, border_color="#c5c7c4", border_width=0.5,
                                          fg_color='#F8F9F9')
        self.user_info_bio.grid(row=1, column=3, sticky="nsew", padx=5, pady=(5, 10))
        self.bio_string = ctk.CTkLabel(master=self.user_info_bio, text=userinfo.get_note(), text_color='grey',
                                       font=("Segoe UI", 13, 'italic'))
        self.bio_string.pack(pady=20, padx=20, anchor='center')

    def init_authorization_screen(self):
        self.auth_info = ctk.CTkFrame(master=self.content_frame)

        self.auth_info.rowconfigure(0, weight=1)
        self.auth_info.columnconfigure((0, 2), weight=1)
        self.auth_info.columnconfigure(1, weight=5)

        self.auth_info_login_form = ctk.CTkFrame(master=self.auth_info, border_color="black", border_width=1)
        self.auth_info_login_form.grid(row=0, column=1, sticky="nsew", pady=10, padx=225)

        self.auth_info_login_form.rowconfigure((0, 1, 2, 3, 6), weight=1)
        self.auth_info_login_form.rowconfigure(4, weight=15)
        self.auth_info_login_form.columnconfigure((0, 2), weight=1)
        self.auth_info_login_form.columnconfigure(1, weight=5)

        self.login_label = ctk.CTkLabel(master=self.auth_info_login_form, text="Авторизация", font=("Segoe UI", -20))
        self.login_label.grid(row=0, column=1, sticky="n", pady=15)

        self.login_email = ctk.CTkEntry(master=self.auth_info_login_form, placeholder_text="E-mail", height=40)
        self.login_email.grid(row=1, column=1, sticky="new", pady=(25, 0))

        self.login_password = ctk.CTkEntry(master=self.auth_info_login_form, placeholder_text="Пароль", height=40,
                                           show="*")
        self.login_password.grid(row=2, column=1, sticky="new")

        self.is_teacher_checkbox = ctk.CTkCheckBox(master=self.auth_info_login_form, text="Зайти как преподаватель")
        self.is_teacher_checkbox.grid(row=3, column=1, sticky="we")

        self.login_submit_btn = ctk.CTkButton(master=self.auth_info_login_form, text="Войти", height=40,
                                              font=("Segoe UI", -18), command=self.login)
        self.login_submit_btn.grid(row=6, column=1, sticky="sew", pady=25)

        self.login_debug_btn = ctk.CTkButton(master=self.auth_info_login_form, text="Отладка", command=self.debug)
        self.login_debug_btn.grid(row=5, column=1, sticky="snew")

    def init_timetable_screen(self):
        self.timetable_info = ctk.CTkFrame(master=self.content_frame)
        self.timetable_info.grid(row=0, column=0)
        self.timetable_info.rowconfigure((0, 1), weight=1)
        self.timetable_info.columnconfigure((0, 1, 2), weight=1)

        days_of_the_week = []
        days_of_the_week_names = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
        self.subject_list = []
        for i in range(6):
            column_of_timetable = i // 2
            row_of_timetable = i % 2
            current_day = ctk.CTkFrame(master=self.timetable_info, border_color="black", border_width=1,
                                       fg_color="#F8F9F9")
            current_day.grid(row=row_of_timetable, column=column_of_timetable, sticky="nsew", padx=2, pady=2)
            current_day.grid_propagate(False)
            current_day.columnconfigure((0, 2), weight=1)
            current_day.columnconfigure(1, weight=15)
            current_day.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
            ctk.CTkLabel(master=current_day, text=days_of_the_week_names[i], height=10,
                         font=("Segoe UI", -19)).grid(row=0, column=0, columnspan=3, sticky="ew", padx=5)
            subjects_of_the_day = []
            for j in [1, 3, 5, 7]:
                subject_form = ctk.CTkFrame(master=current_day, corner_radius=5)
                subject_form.grid(row=j, column=1, sticky="nsew", pady=4, padx=5)
                subject_form.grid_forget()

                subject_form.columnconfigure((0, 2, 3), weight=1)
                subject_form.columnconfigure(1, weight=15)
                subject_form.rowconfigure((0, 1), weight=1)

                subject_starts = ctk.CTkLabel(master=subject_form, text="00:00")
                subject_starts.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

                subject_ends = ctk.CTkLabel(master=subject_form, text="99:99")
                subject_ends.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)

                subject_name = ctk.CTkLabel(master=subject_form, text="Название")
                subject_name.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)

                subject_teacher = ctk.CTkLabel(master=subject_form, text="")
                subject_teacher.grid(row=1, column=1, sticky="nsew", padx=2, pady=2)

                subject_weeks = ctk.CTkLabel(master=subject_form, text="Недели")
                subject_weeks.grid(row=0, column=2, sticky="nsew", padx=2, pady=2)

                subject_subgroups = ctk.CTkLabel(master=subject_form, text="Подгруппы")
                subject_subgroups.grid(row=1, column=2, sticky="nsew", padx=2, pady=2)

                im = Image.open(os.path.join(PATH, "images", "bell.png"))
                image = ctk.CTkImage(light_image=im)
                btn_notify = ctk.CTkButton(master=subject_form, text="", image=image, command=self.notify, width=10)
                btn_notify.grid(row=0, rowspan=2, column=3, padx=2, pady=2)

                subject_dict = {'form': subject_form, 'starts': subject_starts, 'subgroups': subject_subgroups,
                                'name': subject_name, 'ends': subject_ends, 'teacher': subject_teacher,
                                'weeks': subject_weeks, 'btn': btn_notify}

                subjects_of_the_day.append(subject_dict)
            self.subject_list.append(subjects_of_the_day)
            for separ_index in [2, 4, 6]:
                ttk.Separator(master=current_day, orient='horizontal').grid(column=1, row=separ_index, sticky='ewns')
            days_of_the_week.append(current_day)

    def hide_all_windows(self):
        self.user_info.grid_forget()
        self.auth_info.grid_forget()
        self.timetable_info.grid_forget()

    def navigate_home(self):
        self.return_highlighted_texts_to_normal()
        self.btn_home.configure(font=("Segoe UI", -15, "bold"))
        self.hide_all_windows()
        self.user_info.grid(row=0, column=0, sticky="nsew")
        self.content_frame.grid_propagate(False)

    def navigate_group(self):
        self.return_highlighted_texts_to_normal()
        self.btn_group.configure(font=("Segoe UI", -15, "bold"))
        self.hide_all_windows()

    def navigate_work_materials(self):
        self.return_highlighted_texts_to_normal()
        self.btn_work.configure(font=("Segoe UI", -15, "bold"))
        self.hide_all_windows()

    def navigate_timetable(self):
        self.return_highlighted_texts_to_normal()
        self.btn_timetable.configure(font=("Segoe UI", -15, "bold"))
        self.hide_all_windows()
        self.timetable_info.grid(row=0, column=0, sticky="nsew")
        self.content_frame.grid_propagate(False)

        def callback(resp: requests.Response, *args, **kwargs):
            if resp.status_code == 201 or resp.status_code == 200:
                data = resp.json()['data']
                print(data)
                self.timetable_data = data
                self.draw_timetable()
            else:
                print('error')

        hooks = {'response': callback}

        if not self.debug_mode:
            if self.is_teacher:
                body = {'teacherId': int(self.id)}
                requests.post('http://192.168.108.208:3002/api/v1/teachers/schedule', json=body, hooks=hooks)
            else:
                requests.get('http://192.168.108.208:3001/api/v1/groups/' + str(self.group_id) + '/schedule', hooks=hooks)
        else:
            self.draw_timetable()

    def draw_timetable(self):
        if self.debug_mode:
            self.timetable_data = [{'class': {'dayOfTheWeek': '3', 'ends': '11:55', 'name': 'ПБЗ', 'starts': '10:35', 'type': 'ЛР', 'id': 51}, 'group': {'name': '021703', 'course': 1, 'id': 0}, 'subgroups': [{'subgroup': 2, 'id': 5}], 'teacher': {'lastName': 'Шункевич', 'firstName': 'Даниил', 'middleName': 'Вячеславович', 'email': 'here.tempest@gmail.com', 'id': 48}, 'weeks': [{'number': 1, 'id': 32}]},
                                   {'class': {'dayOfTheWeek': '2', 'ends': '11:55', 'name': 'ПБЗ', 'starts': '10:35', 'type': 'ЛК', 'id': 47}, 'group': {'name': '021703', 'course': 1, 'id': 0}, 'subgroups': [{'subgroup': 2, 'id': 5}, {'subgroup': 1, 'id': 4}], 'teacher': {'lastName': 'Шункевич', 'firstName': 'Даниил', 'middleName': 'Вячеславович', 'email': 'here.tempest@gmail.com', 'id': 48}, 'weeks': [{'number': 1, 'id': 32}, {'number': 3, 'id': 34}]},
                                   {'class': {'dayOfTheWeek': '3', 'ends': '11:55', 'name': 'ПБЗ', 'starts': '10:35', 'type': 'ЛК', 'id': 47}, 'group': {'name': '021703', 'course': 1, 'id': 0}, 'subgroups': [{'subgroup': 2, 'id': 5}, {'subgroup': 1, 'id': 4}], 'teacher': {'lastName': 'Шункевич', 'firstName': 'Даниил', 'middleName': 'Вячеславович', 'email': 'here.tempest@gmail.com', 'id': 48}, 'weeks': [{'number': 1, 'id': 32}, {'number': 3, 'id': 34}]},
                                   {'class': {'dayOfTheWeek': '3', 'ends': '10:20', 'name': 'СиМОИБ', 'starts': '9:00', 'type': 'ЛР', 'id': 40}, 'group': {'name': '021703', 'course': 1, 'id': 0}, 'subgroups': [{'subgroup': 1, 'id': 4}, {'subgroup': 2, 'id': 5}], 'teacher': {'lastName': 'Захаров', 'firstName': 'Владимир', 'middleName': 'Владимирович', 'email': 'igrakkaunt@gmail.com', 'id': 41}, 'weeks': [{'number': 4, 'id': 35}, {'number': 2, 'id': 33}]},
                                   {'class': {'dayOfTheWeek': '1', 'ends': '10:20', 'name': 'СиМОИБ', 'starts': '9:00', 'type': 'ЛР', 'id': 40}, 'group': {'name': '021703', 'course': 1, 'id': 0}, 'subgroups': [{'subgroup': 1, 'id': 4}, {'subgroup': 2, 'id': 5}], 'teacher': {'lastName': 'Захаров', 'firstName': 'Владимир', 'middleName': 'Владимирович', 'email': 'igrakkaunt@gmail.com', 'id': 41}, 'weeks': [{'number': 4, 'id': 35}, {'number': 2, 'id': 33}]}]
        days_of_the_week = [[], [], [], [], [], []]
        for class_info in self.timetable_data:
            current_day = int(class_info['class']['dayOfTheWeek']) - 1
            subgroups = []
            for i in class_info['subgroups']:
                subgroups.append(i['subgroup'])
            sub_dict = {'subgroups': subgroups}
            weeks = []
            for i in class_info['weeks']:
                weeks.append(i['number'])
            weeks_dict = {'weeks': weeks}
            name_dict = {}
            if not self.is_teacher:
                final_name = class_info['teacher']['lastName'] + " " + class_info['teacher']['firstName'][0] + ". " + \
                             class_info['teacher']['middleName'][0] + "."
                name_dict = {'teacher': final_name}
            all_info = class_info['class'] | sub_dict | weeks_dict | name_dict
            days_of_the_week[current_day].append(all_info)

        for day in range(len(days_of_the_week)):
            print(days_of_the_week[day])
            for subject in range(len(days_of_the_week[day])):
                subject_type = days_of_the_week[day][subject]['type']
                subject_name = days_of_the_week[day][subject]['name']
                subject_ends = days_of_the_week[day][subject]['ends']
                subject_starts = days_of_the_week[day][subject]['starts']
                subject_id = days_of_the_week[day][subject]['id']
                subject_weeks = days_of_the_week[day][subject]['weeks']
                subject_weeks_str = 'Нед. ' + ', '.join(list(map(lambda x: str(x), subject_weeks)))
                subject_subgroups = days_of_the_week[day][subject]['subgroups']
                subject_subgroups_str = 'Подгр. ' + ', '.join(list(map(lambda x: str(x), subject_subgroups)))
                if not self.is_teacher:
                    subject_teacher = days_of_the_week[day][subject]['teacher']
                else:
                    subject_teacher = ""

                self.subject_list[day][subject]['form'].grid(row=subject * 2 + 1, column=1, sticky="ew", pady=4, padx=2)
                self.subject_list[day][subject]['starts'].configure(text=subject_starts)
                self.subject_list[day][subject]['ends'].configure(text=subject_ends)
                self.subject_list[day][subject]['teacher'].configure(text=subject_teacher)
                self.subject_list[day][subject]['name'].configure(text=subject_name)
                self.subject_list[day][subject]['weeks'].configure(text=subject_weeks_str)
                self.subject_list[day][subject]['subgroups'].configure(text=subject_subgroups_str)
                notify_arg = partial(self.notify, subject_id)
                self.subject_list[day][subject]['btn'].configure(command=notify_arg)
                if subject_type == "ЛР":
                    self.subject_list[day][subject]['starts'].configure(fg_color="red", corner_radius=35)
                if subject_type == "ЛК":
                    self.subject_list[day][subject]['starts'].configure(fg_color="green", corner_radius=35)
                if subject_type == "ПЗ":
                    self.subject_list[day][subject]['starts'].configure(fg_color="yellow", corner_radius=35)

    def navigate_select_user(self):
        self.return_highlighted_texts_to_normal()
        self.btn_user.configure(font=("Segoe UI", -13, "bold"))
        self.hide_all_windows()
        self.auth_info.grid(row=0, column=0, sticky="nsew")
        self.content_frame.grid_propagate(False)

    def return_highlighted_texts_to_normal(self):
        self.btn_home.configure(font=("Segoe UI", -13))
        self.btn_group.configure(font=("Segoe UI", -13))
        self.btn_work.configure(font=("Segoe UI", -13))
        self.btn_timetable.configure(font=("Segoe UI", -13))
        self.btn_user.configure(font=("Segoe UI", -13))

    def update_user_info(self):
        image = userinfo.MakeIcon(userinfo.profile_pic)
        icon_image = ctk.CTkImage(light_image=image, size=(image.size[0] / 1.5, image.size[1] / 1.5))
        self.label_icon.configure(image=icon_image)
        self.bio_string.configure(text=userinfo.get_note())
        new_skills = userinfo.get_skills()
        i = 0
        for key in new_skills.keys():
            self.list_of_keys[i].configure(text=key)
            i += 1
        i = 0
        for value1 in new_skills.values():
            self.list_of_progressbars[i].set(value1 / 5)
            i += 1
        self.other1.configure(text=userinfo.get_other_info_1())
        self.other2.configure(text=userinfo.get_other_info_2())
        self.full_name.configure(text=userinfo.get_full_name())
        self.lbl_email.configure(text=userinfo.get_email())
        self.address.configure(text=userinfo.get_Address())
        self.course.configure(text=userinfo.get_number_course())
        self.social_networks.configure(text=userinfo.get_social_networks())
        self.m_phone.configure(text=userinfo.get_Mobile())
        self.h_phone.configure(text=userinfo.get_Home_Phone())
        self.rating.configure(text=userinfo.get_rating())
        self.faculty.configure(text=userinfo.get_faculty())
        self.speciality.configure(text=userinfo.get_speciality())

    def login(self):
        self.email = self.login_email.get()
        self.password = self.login_password.get()
        self.is_teacher = bool(self.is_teacher_checkbox.get())

        body = {'login': self.email, 'password': self.password}

        def callback(resp: requests.Response, *args, **kwargs):
            if resp.status_code == 201:
                data = resp.json()['data']
                self.btn_home.configure(state="normal")
                self.btn_group.configure(state="normal")
                self.btn_timetable.configure(state="normal")
                self.btn_work.configure(state="normal")
                print(data)
                self.id = data['id']
                if 'group' in data.keys():
                    group_info = data['group']
                    self.group_id = group_info['id']
                    self.group_name = group_info['name']
                if self.email != self.logged_in:
                    if 'profile' in data.keys() and data['profile'] is not None:
                        os.system(f"curl {data['profile']['uri']} > ./images/profile.png")
                        userinfo.profile_pic = 'profile.png'
                    else:
                        userinfo.profile_pic = 'profile_pic.jpg'
                self.logged_in = self.email
                userinfo.import_json(data, self.is_teacher)
            else:
                print('error')

        hooks = {'response': callback}

        if self.is_teacher:
            requests.post('http://192.168.108.208:3002/api/v1/auth/sign-in', json=body, hooks=hooks)
        else:
            requests.post('http://192.168.108.208:3003/api/v1/auth/sign-in', json=body, hooks=hooks)

        self.update_user_info()

    def debug(self):
        self.email = self.login_email.get()
        self.password = self.login_password.get()
        self.is_teacher = bool(self.is_teacher_checkbox.get())
        self.btn_home.configure(state="normal")
        self.btn_group.configure(state="normal")
        self.btn_timetable.configure(state="normal")
        self.btn_work.configure(state="normal")
        userinfo.change_user(self.is_teacher)
        self.debug_mode = True

        self.update_user_info()

    def notify(self, id_in):
        message = tk.simpledialog.askstring('', 'Введите ваше сообщение')

        def callback(resp: requests.Response, *args, **kwargs):
            if resp.status_code == 201 or resp.status_code == 200:
                print("Event called!")
            else:
                print('error')

        hooks = {'response': callback}

        if self.is_teacher:
            body = {
                'classId': int(id_in),
                'message': message,
                'teacherId': int(self.id)
                    }
            requests.post('http://192.168.108.208:3002/api/v1/teachers/event', json=body, hooks=hooks)
        else:
            body = {
                'classId': int(id_in),
                'message': message,
                'studentId': int(self.id)
                    }
            requests.post('http://192.168.108.208:3003/api/v1/students/event', json=body, hooks=hooks)


if __name__ == "__main__":
    userinfo = UserInfo()
    userinfo.change_user(-1)
    app = StartingScreen()
    app.mainloop()
