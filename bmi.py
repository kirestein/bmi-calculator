import customtkinter as ctk
from settings import *
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

class BMI(ctk.CTk):
    def __init__(self):
        # window setup
        super().__init__(fg_color = GREEN)
        self.title('')
        self.iconbitmap("empty.ico")
        self.geometry('400x400')
        self.resizable(False, False)
        self.change_title_bar_color()

        # layout
        # self.grid_columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0,1,2,3), weight=1, uniform='a')
  
        # widgets
        ResultText(self)

        self.mainloop()
        
    def change_title_bar_color(self):
            
            try:
                HWND = windll.user32.GetParent(self.winfo_id())
                DWMWA_ATTRIBUTE = 35
                COLOR = TITLE_HEX_COLOR
                windll.dwmapi.DwmSetWindowAttribute(HWND,DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
            except:
                pass
            #exercise
            # change the color of the title bar
            # this will onle work on windows, make sure it does not crash on macos
            
class ResultText(ctk.CTkLabel):
    def __init__(self, parent):
        super().__init__(master=parent, text=22.5)
        self.grid(column=0, row=0, rowspan=2, sticky='nsew')
        
if __name__ == '__main__':
    BMI()