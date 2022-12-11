import tkinter as tk
import tkinter.messagebox
import customtkinter as ctk
import os
from PIL import Image, ImageTk

PATH = os.path.dirname(os.path.realpath(__file__))
DEFAULT_FONT = ""

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class StartingScreen(ctk.CTk):
    WIDTH = 845
    HEIGHT = 540

    def __init__(self):
        super().__init__()

        self.title("Фронтенд системы управления университетами")
        self.center_app_on_screen()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

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
                                      fg_color="#212529", bg_color="#eeeeee", command=self.navigate_home)
        self.btn_home.grid(row=0, column=0, sticky="nsew")

        self.btn_group = ctk.CTkButton(master=self.navigation_bar, text="Group", corner_radius=0,
                                       font=("Segoe UI", -13), fg_color="#212529", bg_color="#eeeeee",
                                       command=self.navigate_group)
        self.btn_group.grid(row=0, column=1, sticky="nsew")

        self.btn_work = ctk.CTkButton(master=self.navigation_bar, text="Work Materials", corner_radius=0,
                                      font=("Segoe UI", -13), fg_color="#212529", bg_color="#eeeeee",
                                      command=self.navigate_work_materials)
        self.btn_work.grid(row=0, column=2, sticky="nsew")

        self.btn_timetable = ctk.CTkButton(master=self.navigation_bar, text="Timetable", corner_radius=0,
                                           font=("Segoe UI", -13), fg_color="#212529", bg_color="#eeeeee",
                                           command=self.navigate_timetable)
        self.btn_timetable.grid(row=0, column=3, sticky="nsew")

        self.btn_user = ctk.CTkButton(master=self.navigation_bar, text="SELECT USER", corner_radius=0, border_width=1,
                                      font=("Segoe UI", -13), fg_color="#212529", border_color="white",
                                      command=self.navigate_select_user)
        self.btn_user.grid(row=0, column=5, sticky="e", padx=5)

        # ===========================                ===========================

        self.init_user_info_UI()

    def init_user_info_UI(self):
        self.user_info = ctk.CTkFrame(master=self.content_frame)
        self.user_info.grid(row=0, column=0, sticky="nsew")

        self.user_info.columnconfigure((0, 4), weight=1)
        self.user_info.columnconfigure((1, 2, 3), weight=5)
        self.user_info.rowconfigure((0, 1), weight=1)

        self.user_info_profile = ctk.CTkFrame(master=self.user_info, border_color="black", border_width=1)
        self.user_info_profile.grid(row=0, column=1, sticky="nsew", padx=5, pady=(10, 5))

        self.user_info_basic = ctk.CTkFrame(master=self.user_info, border_color="black", border_width=1)
        self.user_info_basic.grid(row=0, column=2, columnspan=2, sticky="nsew", padx=5, pady=(10, 5))

        self.user_info_uni = ctk.CTkFrame(master=self.user_info, border_color="black", border_width=1)
        self.user_info_uni.grid(row=1, column=1, sticky="nsew", padx=5, pady=(5, 10))

        self.user_info_parameters = ctk.CTkFrame(master=self.user_info, border_color="black", border_width=1)
        self.user_info_parameters.grid(row=1, column=2, sticky="nsew", padx=5, pady=(5, 10))

        self.user_info_bio = ctk.CTkFrame(master=self.user_info, border_color="black", border_width=1)
        self.user_info_bio.grid(row=1, column=3, sticky="nsew", padx=5, pady=(5, 10))

    def hide_all_windows(self):
        self.user_info.grid_forget()

    def navigate_home(self):
        self.return_highlighted_texts_to_normal()
        self.btn_home.configure(font=("Segoe UI", -13, "bold"))
        self.user_info.grid(row=0, column=0, sticky="nsew")

    def navigate_group(self):
        self.return_highlighted_texts_to_normal()
        self.btn_group.configure(font=("Segoe UI", -13, "bold"))
        self.hide_all_windows()

    def navigate_work_materials(self):
        self.return_highlighted_texts_to_normal()
        self.btn_work.configure(font=("Segoe UI", -13, "bold"))
        self.hide_all_windows()

    def navigate_timetable(self):
        self.return_highlighted_texts_to_normal()
        self.btn_timetable.configure(font=("Segoe UI", -13, "bold"))
        self.hide_all_windows()

    def navigate_select_user(self):
        self.return_highlighted_texts_to_normal()
        self.btn_user.configure(font=("Segoe UI", -13, "bold"))
        self.hide_all_windows()

    def return_highlighted_texts_to_normal(self):
        self.btn_home.configure(font=("Segoe UI", -13))
        self.btn_group.configure(font=("Segoe UI", -13))
        self.btn_work.configure(font=("Segoe UI", -13))
        self.btn_timetable.configure(font=("Segoe UI", -13))
        self.btn_user.configure(font=("Segoe UI", -13))


if __name__ == "__main__":
    app = StartingScreen()
    app.mainloop()


