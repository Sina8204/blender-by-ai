import tkinter as tk
import threading
import time
import tkinter as tk
import sys , os
import json
from tkinter import messagebox
from api_class import models
from code_class import code_panel_class as cps
from operator_class import operator_panel_class as opc

def send_requiest(root , key , prompt , verson):
    operator_model = models(root)
    operator_model.key = key
    operator_model.system_instruction = (
        "You are Gemini 2.5 Flash. Follow these rules strictly:",
        "1. Input format:",
        "- You will receive:",
        f"    a. A Python script written for Blender version {verson} using the `bpy` API.",
        "    b. A request asking for explanation, guidance, or commentary about this script.",
        "2. Task:",
        "- Provide clear explanations, guidance, or commentary about the given Blender Python script.",
        "- Tailor your response to the specific request made about the script (e.g., explain functionality, point out issues, suggest improvements).",
        "- Speak naturally to the user, as if guiding them through the code.",
        "- Do NOT generate or modify code unless explicitly requested.",
        "3. Constraints:",
        "- If the user asks about a different project or unrelated code, respond with: 'من فقط درباره کدی که نوشتی می‌توانم باهات صحبت کنم.'",
        "- Focus only on the provided Blender Python script.",
        f"- Ensure explanations are accurate, relevant to Blender version {verson}, and easy to understand.",
        "4. Output style:",
        "- Conversational and explanatory text.",
        "- No code output unless explicitly requested by the user."
    )

    operator_model.user_input = prompt
    operator_model.send_requiest_to_model()
    print(f"rispons : \n{operator_model.outpute()}")
    return operator_model.outpute()

class wait:
    def __init__(self, root):
        self.root = root
        self.loading_win = None

    def waiting(self):
        self.loading_win = tk.Toplevel(self.root)
        self.loading_win.title("Please Wait")
        self.loading_win.geometry("200x100")
        tk.Label(self.loading_win, text="Loading... Please wait").pack(expand=True)

    def end_wait(self):
        if self.loading_win and self.loading_win.winfo_exists():
            self.loading_win.destroy()
            self.loading_win = None

class ChatWindow:
    def __init__(self, root , code : cps , operator : opc):
        self.root = root
        self.wait = wait(self.root)
        self.promt_saver = ""
        self.code = code.text_code_area
        self.bl_version = operator.blender_version
        # self.root.title("Chat Window")

        # ساخت Canvas و Scrollbar
        self.canvas = tk.Canvas(root, width=400, height=300, bg="white")
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # اتصال اسکرول
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # ساخت Frame داخل Canvas
        self.message_frame = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.message_frame, anchor="nw")

        # تنظیم اسکرول هنگام تغییر اندازه
        self.message_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # فعال‌سازی اسکرول موس
        #self.root.bind_all("<MouseWheel>", self._on_mousewheel)

        # فعال‌سازی اسکرول موس روی کل برنامه
        self.root.bind_all("<MouseWheel>", self._on_mousewheel)   # ویندوز/مک
        self.root.bind_all("<Button-4>", self._on_mousewheel)     # لینوکس بالا
        self.root.bind_all("<Button-5>", self._on_mousewheel)     # لینوکس پایین

        # ورودی و دکمه ارسال
        self.entry = tk.Entry(root, width=40)
        self.entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.send_button = tk.Button(root, text="ارسال", command= self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=5)

    def _on_mousewheel(self, event):
        """اسکرول موس روی canvas حتی وقتی موس روی message_frame یا ویجت‌های داخلشه"""
        bbox = self.canvas.bbox("all")
        if not bbox:
            return

        content_height = bbox[3] - bbox[1]
        canvas_height = self.canvas.winfo_height()

        if content_height <= canvas_height:
            return

        # ویندوز/مک
        if event.delta:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        # لینوکس
        elif event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")

    def send_message(self):
        message = self.entry.get().strip()
        self.promt_saver = f"\n{message}"
        if message:
            self._add_message(message, sender="user")
            self.entry.delete(0, tk.END)
            # شبیه‌سازی دریافت پاسخ
            threading.Thread(target=self.receive_message , daemon=True).start()

    # def simulate_receive(self):
    #     # نمایش پنجره انتظار
    #     self.root.after(0, self.wait.waiting)
    #     # شبیه‌سازی تأخیر سرور
    #     time.sleep(5)
    #     # افزودن پیام و بستن پنجره در Thread اصلی
    #     self.root.after(0, lambda: self._add_message("سلام! چطور می‌تونم کمکتون کنم؟", sender="operator"))
    #     self.root.after(0, self.wait.end_wait)

    def receive_message(self):
        data = {}
        codes = ""
        try :
            with open("temp.json" , 'r+' , encoding='utf-8') as f:
                data = json.load(f)
            codes = self.code.get("1.0" , tk.END)
        except Exception as e:
            print(f"Error : {e}")
            messagebox.showerror(title ="Error" , message=f"{e}")
            return

        # self.root.after(0, self.wait.waiting)
        try:
            message = send_requiest(self.root , data["api_key"] , codes + self.promt_saver , self.bl_version)
            self.promt_saver = ""
            self.root.after(0, self._add_message(message, sender="operator"))
        except Exception as e:
            print(f"Error : {e}")
            messagebox.showerror(title="Error" , message=f"{e}")
        self.root.after(0, self.wait.end_wait)

    def _add_message(self, text, sender="user"):
        # قاب حباب
        bubble_frame = tk.Frame(self.message_frame, bg="white")
        bubble_frame.pack(fill="x", pady=2)

        if sender == "user":
            lbl = tk.Label(
                bubble_frame, text=text, bg="#cce5ff", fg="black",
                wraplength=250, justify="right", anchor="e", padx=10, pady=5
            )
            lbl.pack(anchor="e", padx=10)
        else:
            lbl = tk.Label(
                bubble_frame, text=text, bg="#d4edda", fg="black",
                wraplength=250, justify="left", anchor="w", padx=10, pady=5
            )
            lbl.pack(anchor="w", padx=10)


# if __name__ == "__main__":
#     root = tk.Tk()
#     chat = ChatWindow(root)
#     root.mainloop()