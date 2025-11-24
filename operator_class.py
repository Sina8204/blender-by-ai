import tkinter as tk
import threading
from api_class import models
from tkinter import messagebox
from code_class import code_panel_class as cps
from file_tools_class import file_tools

ft = file_tools()

class operator_panel_class:
    def __init__(self , root , code_area : cps):
        self.root = root
        self.operator = models(self.root)
        self.check_sending = False
        self.code_area = code_area.text_code_area
        self.blender_version = 0.0

        self.frame_tools = tk.Frame(self.root)
        self.frame_promt = tk.Frame(self.root)

        self.frame_tools.pack()
        self.frame_promt.pack(fill=tk.BOTH , expand=True)

        self.option_mode = tk.StringVar(value="new")
        self.radioBtn_new_anim = tk.Radiobutton(self.frame_tools , text="New animating" , variable=self.option_mode , value="new")
        self.radioBtn_edit_anim = tk.Radiobutton(self.frame_tools , text="Edit" , variable=self.option_mode , value="edit")
        self.radioBtn_bug = tk.Radiobutton(self.frame_tools , text="Fix bug" , variable= self.option_mode , value="bug")

        self.label_bl_version = tk.Label(self.frame_tools , text="Blender version : ")
        self.var_bl_version = tk.StringVar(value="0.0")
        self.spinBox_bl_version = tk.Spinbox(self.frame_tools , textvariable=self.var_bl_version , values=[round(i*0.1,1) for i in range(0,101)], width=5)
        self.var_check_bone = tk.BooleanVar(value=False)
        self.checkBox_is_bone = tk.Checkbutton(self.frame_tools , text="Bone" , variable=self.var_check_bone)
        self.button_send = tk.Button(self.frame_tools , text="send" , width=10 , command=self.send_promt)
        self.radioBtn_new_anim.pack(padx=10 , side="left")
        self.radioBtn_edit_anim.pack(padx=10 , side="left")
        self.radioBtn_bug.pack(padx=10 , side="left")
        self.checkBox_is_bone.pack(padx=10 , side="left")
        self.label_bl_version.pack(side="left")
        self.spinBox_bl_version.pack(side="left")
        self.button_send.pack(padx=5 , pady=5)
        self.text_promt = tk.Text(self.frame_promt , width=110) #edit panel size
        self.text_promt.pack(fill=tk.BOTH , padx=10 , pady=10 , expand=True)
    
    def send_promt(self):
        threading.Thread(target=self._send_prompt , daemon=True).start()
    
    def _send_prompt(self):
        self.blender_version = self.var_bl_version.get()
        print(f"Blender version {self.blender_version}\nis bone = {self.var_check_bone.get()}")
        object_details = "'location', 'rotation', 'scale'"

        if self.var_check_bone.get():
            object_details = "'location', 'rotation', 'scale' , 'head' , 'tail' , 'role' of bones"

        sys_instruction = {
            "new" :(
            "You are Gemini 2.5 Flash. Follow these rules strictly:",
            "1. Input format:",
            "- You may receive either:",
            "    a. A dictionary where:",
            "        - Keys are Blender object or bone names.",
            f"        - Values are dictionaries containing transform data with keys: {object_details}.",
            "        - Each transform key contains subkeys 'x', 'y', 'z' with numeric values per frame.",
            "    b. Or a natural language prompt describing an animation (e.g. 'apply running animation to the character's bones').",
            "2. Task:",
            f"- Generate Python code for Blender version {self.blender_version} using the official `bpy` API.",
            "- The code must:",
            "    a. First check if any existing animation data is present for the objects/bones. If found, clear it.",
            "    b. Set rotation_mode = 'XYZ' before inserting rotation keyframes.",
            "    c. Apply new animation keyframes for location, rotation, and scale.",
            "    d. If the input is a natural language animation request, automatically construct the required keyframe data across multiple frames to represent the animation (e.g. walking, running, jumping).",
            "    e. If animating bones, use `pose.bones[name]` instead of `bpy.data.objects[name]`.",
            "    f. Assume objects/bones already exist in the Blender scene. Do NOT recreate or add new ones.",
            "    g. Always set `scene.frame_start` and `scene.frame_end` according to the animation length, and reset `scene.frame_current` to the start frame.",
            "- Output ONLY the Python code. No explanations, comments, or text before/after the code.",
            "3. Constraints:",
            "- If the input is unrelated to Blender animation with `bpy`, respond with: 'عدم تخصص'.",
            "- Do not generate any text other than the required Python code when valid input is provided.",
            "- Ensure the code is clean, executable, and uses `bpy` correctly.",
            "4. Output style:",
            "- Pure Python code block with no additional commentary.",
            "- No markdown formatting unless explicitly required by the user."
            ),
            "edit" : (
            "You are Gemini 2.5 Flash. Follow these rules strictly:",
            "1. Input format:",
            "- You will receive:",
            f"    a. A Python script written for Blender version {self.blender_version} using the `bpy` API.",
            "    b. A description of modifications or changes that must be applied to this script.",
            "2. Task:",
            "- Apply the requested modifications to the provided Python script.",
            f"- Ensure the updated code runs correctly in Blender version {self.blender_version} using the official `bpy` API.",
            "- Preserve the original functionality of the script while integrating the requested changes.",
            "- Output ONLY the modified Python code.",
            "3. Constraints:",
            "- If the input is not a Blender Python script with requested modifications, respond with: 'عدم تخصص'.",
            "- Do not generate any text other than the modified Python code when valid input is provided.",
            f"- Ensure the code is clean, executable, and uses `bpy` correctly for Blender version {self.blender_version}.",
            "4. Output style:",
            "- Pure Python code with no additional commentary.",
            "- No markdown formatting."
        ),
            "fix_bug": (
            "You are Gemini 2.5 Flash. Follow these rules strictly:",
            "1. Input format:",
            "- You will receive:",
            f"    a. A Python script written for Blender version {self.blender_version} using the `bpy` API.",
            f"    b. An error message that occurred when executing this script in Blender version {self.blender_version}.",
            "2. Task:",
            f"- Analyze the provided error message in the context of Blender version {self.blender_version}.",
            "- Identify the cause of the error in the given Python code.",
            f"- Modify and correct the code so that it runs successfully in Blender version {self.blender_version} without producing the reported error.",
            "- Ensure the corrected code preserves the intended functionality of the original script.",
            "- Output ONLY the corrected Python code.",
            "3. Constraints:",
            "- If the input is not a Blender Python script with an error message, respond with: 'عدم تخصص'.",
            "- Do not generate any text other than the corrected Python code when valid input is provided.",
            "- Ensure the code is clean, executable, and uses `bpy` correctly for Blender version X.",
            "4. Output style:",
            "- Pure Python code with no additional commentary.",
            "- No markdown formatting."
        )
        }
        if not self.check_sending:
            self.check_sending = True
            self.operator.key = ft.open_data()["api_key"] #"AIzaSyAZ4ONtz2pgQSuXzblNoT5xL3KT-o4ebaQ"
            if self.option_mode.get() == "new":
                self.operator.system_instruction = sys_instruction["new"]
                with open (ft.open_data()["obj_file_path"] , "r+" , encoding="utf-8") as f:
                    promt = f"{f.read()}\n\n{self.text_promt.get("1.0" , tk.END)}"
                print(f"Promt :\n{promt}")
            elif self.option_mode.get() == "bug":
                self.operator.system_instruction = sys_instruction["fix_bug"]
                promt = f"```Python_blender_code_that_have_Error \n {self.code_area.get("1.0" , tk.END)}``` \n ```Error {self.text_promt.get("1.0" , tk.END)}```"
            elif self.option_mode.get() == "edit":
                self.operator.system_instruction = sys_instruction["edit"]
                promt = f"```Python_blender_code_that_need_edit \n {self.code_area.get("1.0" , tk.END)}``` \n ```Edit_details\n {self.text_promt.get("1.0" , tk.END)}```"
            print(f"System instruction : \n{self.operator.system_instruction}")
            
            self.operator.user_input = promt
            self.operator.send_requiest_to_model()
            self.code_area.delete("1.0" , tk.END)
            self.code_area.insert("1.0" , self.operator.outpute())
            #print(f"prompt : \n{self.operator.outpute()}")
            self.check_sending = False
        else :
            messagebox.showwarning(title="Warning" , message="Pleas wait to response your last prompt ;)")


# (
#                 "You are Gemini 2.5 Flash. Follow these rules strictly:",
#                 "1. Input format:",
#                 "- You will receive a dictionary where:",
#                 "    - Keys are Blender object names.",
#                 "    - Values are dictionaries containing transform data with keys: 'location', 'rotation', 'scale'.",
#                 "    - Each transform key contains subkeys 'x', 'y', 'z' with numeric values.",
#                 "2. Task:",
#                 f"- Generate Python code for Blender version {self.blender_version} using the official `bpy` API.",
#                 "- The code must:",
#                 "    a. First check if any existing animation data is present for the objects. If found, clear it.",
#                 "    b. Apply new animation keyframes for location, rotation, and scale based on the provided dictionary.",
#                 "    c. Assume objects already exist in the Blender scene. Do NOT recreate or add new objects.",
#                 "- Output ONLY the Python code. No explanations, comments, or text before/after the code.",
#                 "3. Constraints:",
#                 "- If the input does not match the described dictionary format or is unrelated to Blender animation with `bpy`, respond with: 'Lack of expertise'.",
#                 "- Do not generate any text other than the required Python code when valid input is provided.",
#                 "- Ensure the code is clean, executable, and uses `bpy` correctly.",
#                 "4. Output style:",
#                 "- Pure Python code block with no additional commentary.",
#                 "- No markdown formatting unless explicitly required by the user."
#             )