import tkinter as tk
import os
import json

from tkinter import ttk , messagebox
from code_class import code_panel_class
from operator_class import operator_panel_class
from chat_window_class import ChatWindow

temp = {
    "file_path" : "",
    "obj_file_path" : "" ,
    "api_key" : ""
}

class bl_animate(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Blender animating by AI")
        self.geometry("1280x720")
        if not os.path.exists("temp.json"):
            with open("temp.json" , "w+" , encoding="utf-8") as f:
                json.dump(temp , f , ensure_ascii=False , indent=2)
        else :
            with open("temp.json" , "w+" , encoding="utf-8") as f:
                json.dump(temp , f , ensure_ascii=False , indent=2)

        self.main_pw = tk.PanedWindow(self)
        self.main_pw.pack(fill=tk.BOTH , expand=True)

        self.horizontal_pws = tk.PanedWindow(self.main_pw , orient=tk.VERTICAL , relief="solid")
        self.vertical_pws = tk.PanedWindow(self.main_pw , orient=tk.VERTICAL , relief="solid")

        self.main_pw.add(self.horizontal_pws)
        self.main_pw.add(self.vertical_pws)

        self.cod_pw = tk.PanedWindow(self.horizontal_pws , relief="solid")
        self.send_prompt_pw = tk.PanedWindow(self.horizontal_pws , orient=tk.HORIZONTAL , relief="solid")
        self.operator_pw = tk.PanedWindow(self.vertical_pws , orient=tk.VERTICAL , relief="solid")

        self.horizontal_pws.add(self.cod_pw)
        self.horizontal_pws.add(self.send_prompt_pw)
        self.vertical_pws.add(self.operator_pw)

        self.frame_code = tk.Frame(self.cod_pw , width=900 , height=500) #edit panel sizes
        self.frame_send_prompt = tk.Frame(self.send_prompt_pw)
        self.frame_operator = tk.Frame(self.operator_pw)

        self.cod_pw.add(self.frame_code)
        self.send_prompt_pw.add(self.frame_send_prompt)
        self.operator_pw.add(self.frame_operator)

        self.code_panel = code_panel_class(self.frame_code , self)
        self.prompt_send_panel = operator_panel_class(self.frame_send_prompt , self.code_panel)
        self.chatWindow_panel = ChatWindow(self.frame_operator , self.code_panel , self.prompt_send_panel)


app_class = bl_animate()
app_class.mainloop()