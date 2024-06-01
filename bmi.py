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
        
        # data
        self.metric_bool = ctk.BooleanVar(value=True)
        self.height_int = ctk.IntVar(value=170)
        self.weight_float = ctk.DoubleVar(value=65)
        self.bmi_string = ctk.StringVar()
        self.update_bmi()
        
        # tracing
        self.height_int.trace('w', self.update_bmi) #* w is writing, and r is reading the value, in our case we want write the value
        self.weight_float.trace('w', self.update_bmi)
        self.metric_bool.trace('w', self.change_units)
  
        # widgets
        ResultText(self, self.bmi_string)
        self.weight_input = WeightInput(self, self.weight_float, self.metric_bool)
        self.height_input = HeightInput(self, self.height_int, self.metric_bool)
        UnitSwitcher(self, self.metric_bool)

        self.mainloop()
        
        
        
    def update_bmi(self, *args):
        height_meter = self.height_int.get() / 100
        weight_kg = self.weight_float.get()
        bmi_result = weight_kg / height_meter ** 2
        self.bmi_string.set(f'{bmi_result:.1f}')
        
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
    
    def change_units(self, *args):
        self.height_input.update_text(self.height_int.get())
        self.weight_input.update_weight()
class ResultText(ctk.CTkLabel):
    def __init__(self, parent, bmi_string):
        font = ctk.CTkFont(family=FONT, size=MAIN_TEXT_SIZE, weight='bold')
        super().__init__(master=parent, text=22.5, font=font, text_color=WHITE, textvariable=bmi_string)
        self.grid(column=0, row=0, rowspan=2, sticky='nsew')
        
class WeightInput(ctk.CTkFrame):
    def __init__(self, parent, weight_float, metric_bool):
        super().__init__(master=parent, fg_color=WHITE)
        self.grid(column=0, row=2, sticky='nsew', padx=10, pady=10)
        self.weight_float = weight_float
        self.metric_bool = metric_bool
        
        self.output_string = ctk.StringVar()
        
        
        # layout
        self.rowconfigure(0, weight=1, uniform='b')
        self.columnconfigure(0, weight=2, uniform='b')
        self.columnconfigure(1, weight=1, uniform='b')
        self.columnconfigure(2, weight=2, uniform='b')
        self.columnconfigure(3, weight=2, uniform='b')
        self.columnconfigure(4, weight=1, uniform='b')
        self.columnconfigure(5, weight=1, uniform='b')
        self.columnconfigure(6, weight=2, uniform='b')
        self.entry = ctk.CTkEntry(self, textvariable = self.output_string, fg_color=WHITE, border_color=WHITE, placeholder_text_color=GRAY, text_color=GREEN)
        self.entry.grid(row=0, column=3)
        self.update_input()
        self.update_weight()
        # text
        font = ctk.CTkFont(family=FONT, size=INPUT_FONT_SIZE)
        font_ok = ctk.CTkFont(family=FONT, size=10)
        label = ctk.CTkLabel(self, textvariable = self.output_string, text_color=BLACK)
        label.grid(row=0, column=2)
        
        # buttons
        minus_button = ctk.CTkButton(self, command=lambda: self.update_weight(('minus', 'large')), text='-', font=font, text_color=BLACK, fg_color=LIGHT_GRAY,hover_color=GRAY, corner_radius=BUTTON_CORNER_RADIUS)
        minus_button.grid(row=0, column=0, sticky='ns', padx=8, pady=8)
        
        plus_button = ctk.CTkButton(self, command=lambda: self.update_weight(('plus', 'large')), text='+', font=font, text_color=BLACK, fg_color=LIGHT_GRAY,hover_color=GRAY, corner_radius=BUTTON_CORNER_RADIUS)
        plus_button.grid(row=0, column=6, sticky='ns', padx=8, pady=8)
        
        small_minus_button = ctk.CTkButton(self, command=lambda: self.update_weight(('minus', 'small')), text='-', font=font, text_color=BLACK, fg_color=LIGHT_GRAY,hover_color=GRAY, corner_radius=BUTTON_CORNER_RADIUS)
        small_minus_button.grid(row=0, column=1, padx=4, pady=4)
        
        small_plus_button = ctk.CTkButton(self, command=lambda: self.update_weight(('plus', 'small')), text='+', font=font, text_color=BLACK, fg_color=LIGHT_GRAY,hover_color=GRAY, corner_radius=BUTTON_CORNER_RADIUS)
        small_plus_button.grid(row=0, column=5, padx=4, pady=4)
        
        small_ok_button = ctk.CTkButton(self, command=lambda: self.update_input(), text='ok', font=font_ok, text_color=BLACK, fg_color=LIGHT_GRAY,hover_color=GRAY, corner_radius=BUTTON_CORNER_RADIUS)
        small_ok_button.grid(row=0, column=4, padx=4, pady=4)
        
    def update_weight(self, info=None):
        self.update_input()
        if info:
            if self.metric_bool.get():
                amount = 1 if info[1] == 'large' else 0.1
            else:
                amount = 0.453592 if info[1] == 'large' else 0.453592 / 16
                
                # self.output_string.set(f'{self.weight_float.get():.1f}kg')
                # return
            if info[0] == 'plus':
                self.weight_float.set(self.weight_float.get() + amount)
            else:
                self.weight_float.set(self.weight_float.get() - amount)
        if self.metric_bool.get():
            self.output_string.set(f'{self.weight_float.get():.1f}kg')
        else:
            raw_onces = self.weight_float.get() * 2.20462 * 16
            pounds, ounces = divmod(raw_onces, 16)
            self.output_string.set(f'{int(pounds)}lb {int(ounces)}oz')
        
        
    def update_input(self):
        print(self.entry.get()[:-2])
        try:
            self.weight_float.set(float(f'{self.entry.get()}kg'[:-2]))
            self.entry.delete(0, 'end')
            self.output_string.set(f'{self.weight_float.get():.1f}kg')
        except ValueError:
            print('Invalid value!')
    
        # print(self.weight_float.get())
        
class HeightInput(ctk.CTkFrame):
    def __init__(self, parent, height_int, metric_bool):
        super().__init__(master=parent, fg_color=WHITE)
        self.grid(row=3, column=0, sticky='nsew', padx=10, pady=10)
        self.metric_bool = metric_bool
        
        # widgets
        slider = ctk.CTkSlider(
            master=self, 
            command=self.update_text,
            button_color=GREEN,
            button_hover_color=GRAY,
            progress_color=GREEN,
            fg_color=LIGHT_GRAY,
            variable=height_int,
            from_=100,
            to=250
        )
        slider.pack(side='left', fill='x', expand=True, padx=10, pady=10)
        
        self.output_string = ctk.StringVar()
        self.update_text(height_int.get())
        
        output_text = ctk.CTkLabel(self, textvariable=self.output_string, text_color=BLACK, font=ctk.CTkFont(family=FONT, size=INPUT_FONT_SIZE))
        output_text.pack(side='left', padx=20)
        
    def update_text(self, amount):
        if self.metric_bool.get():
            text_string = str(int(amount))
            meter = text_string[0]
            cm = text_string[1:]
            self.output_string.set(f'{meter}.{cm}m')
        else: # imperial
            feet, inches = divmod(amount / 2.54, 12)
            self.output_string.set(f'{int(feet)}\'{int(inches)}\"')
            print(feet)
        
class UnitSwitcher(ctk.CTkLabel):
    def __init__(self, parent, metric_bool):
        super().__init__(master=parent, text='metric', text_color=DARK_GREEN, font=ctk.CTkFont(family=FONT, size=SWITCH_FONT_SIZE, weight='bold'))
        self.place(relx=0.98, rely=0.01, anchor='ne') #ne = north east
        
        self.metric_bool = metric_bool
        self.bind('<Button>', self.change_units)
        
    def change_units(self, event):
        #change the metric bool True -> False
        self.metric_bool.set(not self.metric_bool.get())
        
        if self.metric_bool.get():
            self.configure(text='metric')
        else:
            self.configure(text='imperial')
        
        
if __name__ == '__main__':
    BMI()