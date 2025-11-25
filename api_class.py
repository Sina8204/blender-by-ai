from google import genai 
import tkinter as tk
from tkinter import messagebox

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

class models :
    def __init__(self , root):
        self.root = root
        self.wait = wait(self.root)
        self.key = ""
        self.system_instruction = "" #Explain to your model what to do
        self.user_input = "" #Your promt
        #creat model
        self.response_text = ""
    
    def send_requiest_to_model(self):
        self.root.after(0, self.wait.waiting)
        try :
            self.client = genai.Client(api_key=self.key) #Input your api key
            self.response = self.client.models.generate_content (
            model="gemini-2.5-flash",
            config=genai.types.GenerateContentConfig(system_instruction=self.system_instruction),
            contents=self.user_input
            )
            self.response_text = self.response.text
        except Exception as e:
            messagebox.showerror(title="Error" , message=f"{e}")
        self.root.after(0, self.wait.end_wait)

    def outpute(self):
        try:
            return self.response_text
        except Exception as e:

            return f"Error : {e}"
