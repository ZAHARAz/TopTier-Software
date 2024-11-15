import customtkinter

def SetCenterWindow(parent, width, height):
    position_top = int(parent.winfo_screenheight() / 2 - height / 2)
    position_right = int(parent.winfo_screenwidth() / 2 - width / 2)

    parent.geometry(f'{width}x{height}+{position_right}+{position_top}')

class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, selected_case_names, total_fine, total_jail_time):
        super().__init__(parent)

        self.title('TopTier Software - Calculate Result')       
        self.resizable(False, False)
        self.attributes("-topmost", True)
        SetCenterWindow(self, 400, 300)
        
        self.textbox = customtkinter.CTkTextbox(self, height=100, width=380)
        self.textbox.pack(padx=10, pady=10)
        
        for case_name in selected_case_names:
            self.textbox.insert("end", case_name + " ")
        self.textbox.configure(state="disabled")

        self.result_label = customtkinter.CTkLabel(self, text=f"ค่าปรับรวม: {total_fine} บาท\nเวลาจำคุกรวม: {total_jail_time} วินาที")
        self.result_label.pack(padx=20, pady=10)
