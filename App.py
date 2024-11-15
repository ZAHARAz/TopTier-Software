import customtkinter
import sys
import os
import json
from PIL import Image
from tkinter import messagebox
from components.CaseCalculator import calculate_fine_and_jail_time, validate_and_prepare_cases
from components.Result import ToplevelWindow, SetCenterWindow

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Center window function
def center_window(parent, width, height):
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()
    position_top = int(screen_height / 2 - height / 2)
    position_right = int(screen_width / 2 - width / 2)
    parent.geometry(f'{width}x{height}+{position_right}+{position_top}')

# Load case data from JSON
def load_cases():
    with open('utils/Case.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['cases'], data['global_jail_time_limit']

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Root element configuration
        self.iconbitmap('assets/images/TopTier.ico')
        self.title('TopTier Software - Newthing Police Department Tool v1.0')
        self.resizable(False, False)

        # Initialize case-related attributes
        self.case_checkboxes = []
        self.case_entries = {}

        # Load case data from JSON
        self.cases, self.global_jail_time_limit = load_cases()

        # Center window
        center_window(self, 1000, 550)

        # Grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Image assets
        home_image_path = resource_path("assets/images/home.png")
        user_image_path = resource_path("assets/images/user.png")
        
        self.home_image = customtkinter.CTkImage(Image.open(home_image_path), size=(20, 20))
        self.user_image = customtkinter.CTkImage(Image.open(user_image_path), size=(20, 20))

        # Create sidebar frame
        self.sidebar_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Sidebar labels and buttons
        self.navigation_frame_label = customtkinter.CTkLabel(self.sidebar_frame, text="TopTier Software", compound="center", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        # General page button
        self.general_page_button = customtkinter.CTkButton(self.sidebar_frame, corner_radius=0, height=40, border_spacing=10, text="General", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.home_image, anchor="w", command=self.general_page_event)
        self.general_page_button.grid(row=1, column=0, sticky="ew")

        # Quick case page button
        self.quick_case_button = customtkinter.CTkButton(self.sidebar_frame, corner_radius=0, height=40, border_spacing=10, text="Quick Case", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.user_image, anchor="w", command=self.quick_case_page_event)
        self.quick_case_button.grid(row=2, column=0, sticky="ew")

        # Frame for case lists
        self.general_parent_frame = customtkinter.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.general_parent_frame.grid_columnconfigure(0, weight=1)
        self.quick_case_parent_frame = customtkinter.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")

        # Create list of cases
        self.create_case_list()

        # Calculate button
        self.btn_calculate = customtkinter.CTkButton(self.sidebar_frame, text='คำนวนคดี', command=self.calculate_cases)
        self.btn_calculate.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # Select default frame
        self.SelectPage("general")

    def create_case_list(self):
        for i, case in enumerate(self.cases):
            case_var = customtkinter.BooleanVar()
            checkbox = customtkinter.CTkCheckBox(self.general_parent_frame, text=case['case_name'], variable=case_var)
            checkbox.grid(row=i, column=0, sticky="w", padx=10, pady=5)
            self.case_checkboxes.append((case_var, case))

            if case.get("requires_quantity", True):
                quantity_entry = customtkinter.CTkEntry(self.general_parent_frame, placeholder_text="ระบุจำนวน")
                quantity_entry.grid(row=i, column=1, padx=10)
                self.case_entries[case['case_name']] = quantity_entry

    def calculate_cases(self):
        selected_cases, selected_case_names = validate_and_prepare_cases(self.case_checkboxes, self.case_entries)
        if selected_cases is None:  # There was an error
            return

        total_fine, total_jail_time = calculate_fine_and_jail_time(selected_cases, self.global_jail_time_limit)
        
        # เปิด ToplevelWindow และส่ง selected_case_names ไปให้
        ToplevelWindow(self, selected_case_names, total_fine, total_jail_time)

    def SelectPage(self, name):
        self.general_page_button.configure(fg_color=("gray75", "gray25") if name == "general" else "transparent")
        self.quick_case_button.configure(fg_color=("gray75", "gray25") if name == "quick_case" else "transparent")

        if name == "general":
            self.general_parent_frame.grid(row=0, column=1, sticky="nsew")
            self.quick_case_parent_frame.grid_forget()
        elif name == "quick_case":
            self.quick_case_parent_frame.grid(row=0, column=1, sticky="nsew")
            self.general_parent_frame.grid_forget()

    def general_page_event(self):
        self.SelectPage("general")

    def quick_case_page_event(self):
        self.SelectPage("quick_case")

if __name__ == "__main__":
    app = App()
    app.mainloop()
