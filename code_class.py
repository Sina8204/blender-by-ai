import tkinter as tk
import os , pyperclip , json
from file_tools_class import file_tools
from tkinter import messagebox , ttk
from pathlib import Path

ft = file_tools()
temp = {
    "file_path" : "",
    "obj_file_path" : "" ,
    "api_key" : ""
    }
button_sides = "left"

class creat_new_project_class:
    def __init__(self , root , main_root):
        self.root = root
        self.main_root = main_root
        self.root_tl = tk.Toplevel(self.root)
        self.root_tl.title("Creat new project")
        self.root_tl.geometry("300x100")
        self.root_tl.resizable(False , False)
        self.root_tl.attributes("-topmost", True) #Always be at top

        self.frame_widgets = tk.Frame(self.root_tl)
        self.frame_widgets.pack(expand=True)

        self.frame_name = tk.Frame(self.frame_widgets)
        self.label_name = tk.Label(self.frame_name , text="Project name : ")
        self.entry_name = tk.Entry(self.frame_name)
        self.label_name.pack(side="left")
        self.entry_name.pack()
        self.frame_name.pack()

        self.frame_api = tk.Frame(self.frame_widgets)
        self.label_api = tk.Label(self.frame_api , text="API key : ")
        self.api_key = tk.StringVar()
        self.entry_api = tk.Entry(self.frame_api , textvariable=self.api_key , show='*')
        self.label_api.pack(side="left")
        self.entry_api.pack()
        self.frame_api.pack(pady=10)

        self.frame_button = tk.Frame(self.frame_widgets)
        self.button_creat = tk.Button(self.frame_button , text="Creat project" , command=self.creat_new_project)
        self.button_creat.pack()
        self.frame_button.pack()
    
    def creat_new_project(self):
        self.root_tl.attributes("-topmost", False)
        print(f"API key = {self.api_key.get()}")
        if self.entry_name.get() == "" or self.api_key.get() == "":
            messagebox.showerror(title="Error" , message="Pleas insert your project name and api key")
            self.root_tl.attributes("-topmost", True)
            # self.root_tl.lift()
            # self.root_tl.focus_force()
            return
        dir = ft.open_folder()
        project_path = Path(f"{dir}/{self.entry_name.get()}")
        project_path.mkdir(parents=True , exist_ok=True)

        file_name = f"{project_path}\\{self.entry_name.get()}_code.py"
        object_name = f"{project_path}\\{self.entry_name.get()}_objects.json"
        project_details = f"{project_path}\\details.json"
        with open(file_name , "w+" , encoding="utf-8") as file:
            file.write("")
        with open(object_name , "w+" , encoding="utf-8") as file:
            json.dump({} , file , ensure_ascii=False , indent=2)
        
        project_data = {
            "file_path": f"{file_name}",
            "obj_file_path": f"{object_name}",
            "api_key" : f"{self.entry_api.get()}"
        }

        ft.import_data(name=project_details , data=project_data)
        ft.import_data(data=project_data)

        log = f"Code file created {project_data['file_path']}\nObjects file created {project_data['obj_file_path']}"
        messagebox.showinfo(title="Created new project" , message=f"{log}")
        self.root_tl.destroy()
        self.main_root.title(project_data["file_path"])


class save_as_class():
    def __init__(self , root , Main_root , text : tk.Text):
        self.root = root
        self.text = text
        self.main_root = Main_root

        self.save_as = tk.Toplevel(self.root)
        self.save_as.title("Save as")
        self.save_as.geometry("250x150")
        self.save_as.resizable(False , False)
        self.save_as.attributes("-topmost", True)

        self.fram_widgets = tk.Frame(self.save_as)
        self.fram_widgets.pack(anchor="center" , expand=True)

        self.fram_entry = tk.Frame(self.fram_widgets)
        self.fram_entry.pack()

        self.placeholder = "Enter your file name"
        self.entry_name = tk.Entry(self.fram_entry , fg="grey")
        self.entry_name.insert(0, self.placeholder)
        self.entry_name.bind("<FocusIn>", self.on_entry_click)
        self.entry_name.bind("<FocusOut>", self.on_focus_out)
        self.entry_name.pack(side="left")

        self.combobox_file_type = ttk.Combobox(self.fram_entry , width=3 , values=["py" , "txt"] , state="readonly")
        self.combobox_file_type.current(0)
        self.combobox_file_type.pack()

        self.button_save_as = tk.Button(self.fram_widgets , text="Save as" , command=self.save_action)
        self.button_save_as.pack(pady=10)

    def save_action(self):
        try:
            dir = ft.open_folder()
            with open(f"{dir}/{self.entry_name.get()}.{self.combobox_file_type.get()}" , "w+" , encoding="utf-8") as f:
                f.write(self.text.get("1.0" , tk.END))
            ft.import_data(data={"file_path" : f"{dir}/{self.entry_name.get()}.{self.combobox_file_type.get()}"} , mode="update")
            messagebox.showinfo(title="Save operation was sucssesfully" , message="Your file has been saved")
            self.save_as.destroy()
            self.main_root.title(ft.open_data()["file_path"])
        except Exception as e:
            messagebox.showerror(title="Error" , message=f"{e}")
    
    def on_entry_click(self , event):
        if self.entry_name.get() == self.placeholder:
            self.entry_name.delete(0, "end")  # پاک کردن متن پیشفرض
            self.entry_name.config(fg="black")  # تغییر رنگ به سیاه
    
    def on_focus_out(self , event):
        if self.entry_name.get() == "":
            self.entry_name.config(fg="grey")
            self.entry_name.insert(0, self.placeholder)


class object_inputer:
    def __init__(self , root , canvas , check_bone : bool):
        self.root = root
        self.canvas = canvas
        self.check_bone = check_bone
        self.root_tl = tk.Toplevel(self.root)
        self.root_tl.title("Objects editor")
        self.root_tl.geometry("300x400")
        self.root_tl.resizable(False , False)
        self.root_tl.attributes("-topmost", True) #Always be at top

        self.frame_name = tk.Frame(self.root_tl)
        self.frame_location = tk.Frame(self.root_tl)
        self.frame_rotation = tk.Frame(self.root_tl)
        self.frame_scale = tk.Frame(self.root_tl)

        self.frame_head = tk.Frame(self.root_tl)
        self.frame_tail = tk.Frame(self.root_tl)
        self.frame_roll = tk.Frame(self.root_tl)

        self.frame_button = tk.Frame(self.root_tl)

        pad = 10
        self.frame_name.pack(fill=tk.X , padx= pad , pady=pad)
        self.frame_location.pack(fill=tk.X , padx= pad , pady=pad)
        self.frame_rotation.pack(fill=tk.X , padx= pad , pady=pad)
        self.frame_scale.pack(fill=tk.X , padx= pad , pady=pad)
        if self.check_bone:
            self.frame_head.pack(fill=tk.X , padx= pad , pady=pad)
            self.frame_tail.pack(fill=tk.X , padx= pad , pady=pad)
            self.frame_roll.pack(fill=tk.X , padx= pad , pady=pad)
        self.frame_button.pack(fill=tk.X , padx= pad , pady=pad)

        ################################### Location ###################################
        self.label_name = tk.Label(self.frame_name , text="Name :")
        self.entry_name = tk.Entry(self.frame_name)
        self.label_name.pack(side="left" , padx=5)
        self.entry_name.pack(fill=tk.X , expand=True)

        self.var_loc_x = tk.StringVar(value="0.0")
        self.var_loc_y = tk.StringVar(value="0.0")
        self.var_loc_z = tk.StringVar(value="0.0")

        self.label_location = tk.Label(self.frame_location , text="Location : ")
        self.label_location.pack(padx=10 , side="left")
        self.label_loc_x = tk.Label(self.frame_location , text="X")
        self.spinBox_loc_x = tk.Spinbox(self.frame_location , textvariable=self.var_loc_x , values=[round(i*0.1,1) for i in range(0,101)], width=5)
        self.label_loc_x.pack(side="left")
        self.spinBox_loc_x.pack(side="left")

        self.label_loc_y = tk.Label(self.frame_location , text="Y")
        self.spinBox_loc_y = tk.Spinbox(self.frame_location , textvariable=self.var_loc_y , values=[round(i*0.1,1) for i in range(0,101)], width=5)
        self.label_loc_y.pack(side="left")
        self.spinBox_loc_y.pack(side="left")

        self.label_loc_z = tk.Label(self.frame_location , text="Z")
        self.spinBox_loc_z = tk.Spinbox(self.frame_location , textvariable=self.var_loc_z , values=[round(i*0.1,1) for i in range(0,101)], width=5)
        self.label_loc_z.pack(side="left")
        self.spinBox_loc_z.pack(side="left")
        ################################### Location ###################################

        ################################### Rotation ###################################
        self.var_rot_x = tk.StringVar(value="0.0")
        self.var_rot_y = tk.StringVar(value="0.0")
        self.var_rot_z = tk.StringVar(value="0.0")

        self.label_rotation = tk.Label(self.frame_rotation , text="Rotation : ")
        self.label_rotation.pack(padx=10 , side="left")
        self.label_rot_x = tk.Label(self.frame_rotation , text="X")
        self.spinBox_rot_x = tk.Spinbox(self.frame_rotation , textvariable=self.var_rot_x , values=[round(i*0.1,1) for i in range(0,101)], width=5)
        self.label_rot_x.pack(side="left")
        self.spinBox_rot_x.pack(side="left")

        self.label_rot_y = tk.Label(self.frame_rotation , text="Y")
        self.spinBox_rot_y = tk.Spinbox(self.frame_rotation , textvariable=self.var_rot_y , values=[round(i*0.1,1) for i in range(0,101)], width=5)
        self.label_rot_y.pack(side="left")
        self.spinBox_rot_y.pack(side="left")

        self.label_rot_z = tk.Label(self.frame_rotation , text="Z")
        self.spinBox_rot_z = tk.Spinbox(self.frame_rotation , textvariable=self.var_rot_z , values=[round(i*0.1,1) for i in range(0,101)], width=5)
        self.label_rot_z.pack(side="left")
        self.spinBox_rot_z.pack(side="left")
        ################################### Rotation ###################################

        ################################### Scale ###################################
        self.var_scale_x = tk.StringVar(value="0.0")
        self.var_scale_y = tk.StringVar(value="0.0")
        self.var_scale_z = tk.StringVar(value="0.0")

        self.label_scale = tk.Label(self.frame_scale , text="Scale : ")
        self.label_scale.pack(padx=10 , side="left")
        self.label_scale_x = tk.Label(self.frame_scale , text="X")
        self.spinBox_scale_x = tk.Spinbox(self.frame_scale , textvariable=self.var_scale_x , values=[round(i*0.1,1) for i in range(0,101)], width=5)
        self.label_scale_x.pack(side="left")
        self.spinBox_scale_x.pack(side="left")

        self.label_scale_y = tk.Label(self.frame_scale , text="Y")
        self.spinBox_scale_y = tk.Spinbox(self.frame_scale , textvariable=self.var_scale_y , values=[round(i*0.1,1) for i in range(0,101)], width=5)
        self.label_scale_y.pack(side="left")
        self.spinBox_scale_y.pack(side="left")

        self.label_scale_z = tk.Label(self.frame_scale , text="Z")
        self.spinBox_scale_z = tk.Spinbox(self.frame_scale , textvariable=self.var_scale_z , values=[round(i*0.1,1) for i in range(0,101)], width=5)
        self.label_scale_z.pack(side="left")
        self.spinBox_scale_z.pack(side="left")
        ################################### Scale ###################################

        ################################### Head ###################################
        self.var_head_x = tk.StringVar(value="0.0")
        self.var_head_y = tk.StringVar(value="0.0")
        self.var_head_z = tk.StringVar(value="0.0")

        self.label_head = tk.Label(self.frame_head , text="Head : ")
        self.label_head.pack(padx=10 , side="left")
        self.label_head_x = tk.Label(self.frame_head , text="X")
        self.spinBox_head_x = tk.Spinbox(self.frame_head , textvariable=self.var_head_x , values=[round(i*0.1,1) for i in range(0,101)], width=5)
        self.label_head_x.pack(side="left")
        self.spinBox_head_x.pack(side="left")

        self.label_head_y = tk.Label(self.frame_head , text="Y")
        self.spinBox_head_y = tk.Spinbox(self.frame_head , textvariable=self.var_head_y , values=[round(i*0.1,1) for i in range(0,101)], width=5)
        self.label_head_y.pack(side="left")
        self.spinBox_head_y.pack(side="left")

        self.label_head_z = tk.Label(self.frame_head , text="Z")
        self.spinBox_head_z = tk.Spinbox(self.frame_head , textvariable=self.var_head_z , values=[round(i*0.1,1) for i in range(0,101)], width=5)
        self.label_head_z.pack(side="left")
        self.spinBox_head_z.pack(side="left")
        ################################### Head ###################################

        ################################### Tail ###################################
        self.var_tail_x = tk.StringVar(value="0.0")
        self.var_tail_y = tk.StringVar(value="0.0")
        self.var_tail_z = tk.StringVar(value="0.0")

        self.label_tail = tk.Label(self.frame_tail , text="Tail : ")
        self.label_tail.pack(padx=10 , side="left")
        self.label_tail_x = tk.Label(self.frame_tail , text="X")
        self.spinBox_tail_x = tk.Spinbox(self.frame_tail , textvariable=self.var_tail_x , values=[round(i*0.1,1) for i in range(0,101)], width=5)
        self.label_tail_x.pack(side="left")
        self.spinBox_tail_x.pack(side="left")

        self.label_tail_y = tk.Label(self.frame_tail , text="Y")
        self.spinBox_tail_y = tk.Spinbox(self.frame_tail , textvariable=self.var_tail_y , values=[round(i*0.1,1) for i in range(0,101)], width=5)
        self.label_tail_y.pack(side="left")
        self.spinBox_tail_y.pack(side="left")

        self.label_tail_z = tk.Label(self.frame_tail , text="Z")
        self.spinBox_tail_z = tk.Spinbox(self.frame_tail , textvariable=self.var_tail_z , values=[round(i*0.1,1) for i in range(0,101)], width=5)
        self.label_tail_z.pack(side="left")
        self.spinBox_tail_z.pack(side="left")
        ################################### Tail ###################################

        ################################### Roll ###################################
        self.var_roll = tk.StringVar(value="0.0")

        self.label_roll = tk.Label(self.frame_roll , text="Roll : ")
        self.label_roll.pack(padx=10 , side="left")
        self.label_roll_deg = tk.Label(self.frame_roll , text="Degree")
        self.spinBox_roll_deg = tk.Spinbox(self.frame_roll , textvariable=self.var_roll , values=[round(i*0.1,1) for i in range(0,101)], width=5)
        self.label_roll_deg.pack(side="left")
        self.spinBox_roll_deg.pack(side="left")
        ################################### Roll ###################################

        self.button_input = tk.Button(self.frame_button , text="Input" , command=self.input_obj)
        self.button_input.pack(fill=tk.X , expand=True)

    def input_obj(self):
        obj_name = self.entry_name.get()
        obj_transform = {
            "location" : {
                "x" : self.var_loc_x.get() ,
                "y" : self.var_loc_y.get() ,
                "z" : self.var_loc_z.get()
            } ,
            "rotation" : {
                "x" : self.var_rot_x.get() ,
                "y" : self.var_rot_y.get() ,
                "z" : self.var_rot_z.get()
            } ,
            "scale" : {
                "x" : self.var_scale_x.get() ,
                "y" : self.var_scale_y.get() ,
                "z" : self.var_scale_z.get()
            }
        }
        bone_detail ={
            "Head" : {
                "x" : self.var_head_x.get() ,
                "y" : self.var_head_y.get() ,
                "z" : self.var_head_z.get()
            },
            "Tail" : {
                "x" : self.var_tail_x.get() ,
                "y" : self.var_tail_y.get() ,
                "z" : self.var_tail_z.get()
            },
            "Roll" : self.var_roll.get()
        }

        if self.check_bone :
            obj_transform.update(bone_detail)
        obj_item = {obj_name : obj_transform}
        try:
            self.root_tl.attributes("-topmost", False)
            self.root.attributes("-topmost", False)
            if os.path.exists(ft.open_data()["obj_file_path"]):
                ft.import_data(ft.open_data()["obj_file_path"] , obj_item , mode="update")
                # with open(ft.open_data()["obj_file_path"] , "a+" , encoding="utf-8") as f:
                #     json.dump(obj_item , f , ensure_ascii=False , indent=4)
            else:
                dir = ft.open_file(Title="Select an object json file" , type_files=[("objects.json" , "*objects.json") ,("json" , ".json") , ("txt" , ".txt") , ("" , "*.All files")])
                temp = ft.open_data()
                temp.update({"obj_file_path" : dir})
                with open("temp.json" , "w+" , encoding="utf-8") as f:
                    json.dump(temp , f , ensure_ascii=False , indent=2)
                ft.import_data(ft.open_data()["obj_file_path"] , obj_item , mode="update")
                # with open(ft.open_data()["obj_file_path"] , "a+" , encoding="utf-8") as f:
                #     json.dump(obj_item , f , ensure_ascii=False , indent=4)
            self.add_obj_item(self.canvas)
            self.root_tl.destroy()
        except Exception as e:
            messagebox.showerror(title="Error" , message=f"{e}")
            self.root_tl.destroy()
        self.root.attributes("-topmost", True)
    
    def add_obj_item(self , root):
        frame_items = tk.Frame(root , bd=1 , relief="solid")
        label_name = tk.Label(frame_items , text = f"Name : {self.entry_name.get()}")
        label_loc = tk.Label(frame_items , text = f"Location : X({self.var_loc_x.get()})  Y({self.var_loc_y.get()})  Z({self.var_loc_z.get()})")
        label_rot = tk.Label(frame_items , text = f"Rotation : X({self.var_rot_x.get()})  Y({self.var_rot_y.get()})  Z({self.var_rot_z.get()})")
        label_scale = tk.Label(frame_items , text = f"Scale : X({self.var_scale_x.get()})  Y({self.var_scale_y.get()})  Z({self.var_scale_z.get()})")
        label_name.pack(pady=5)
        label_loc.pack(pady=5)
        label_rot.pack(pady=5)
        label_scale.pack(pady=5)
        if self.check_bone:
            label_Head = tk.Label(frame_items , text = f"Head : X({self.var_head_x.get()})  Y({self.var_head_y.get()})  Z({self.var_head_z.get()})")
            label_Tail = tk.Label(frame_items , text = f"Tail : X({self.var_tail_x.get()})  Y({self.var_tail_y.get()})  Z({self.var_tail_z.get()})")
            label_Roll = tk.Label(frame_items , text = f"Roll : Degree({self.var_roll.get()})")
            label_Head.pack(pady=5)
            label_Tail.pack(pady=5)
            label_Roll.pack(pady=5)
        
        frame_items.pack(pady=10)


class objects_input:
    def __init__(self , root):
        self.root = root
        self.root_tl = tk.Toplevel(self.root)
        self.root_tl.title("Objects editor")
        self.root_tl.geometry("300x500")
        self.root_tl.resizable(False , False)
        self.root_tl.attributes("-topmost", True) #Always be at top

        self.frame_buttons = tk.Frame(self.root_tl)
        self.frame_canvas = tk.Frame(self.root_tl)

        self.frame_buttons.pack(fill=tk.X)
        self.frame_canvas.pack(fill=tk.BOTH , expand=True)

        self.var_check_bone = tk.BooleanVar(value=False)
        self.checkBox_is_bone = tk.Checkbutton(self.frame_buttons , text="Bone" , variable=self.var_check_bone)
        self.button_input_new_object = tk.Button(self.frame_buttons , text="New object" , command=self.new_object)
        self.button_import_object = tk.Button(self.frame_buttons , text="Import object")
        self.checkBox_is_bone.pack(padx=10 , side="left")
        self.button_input_new_object.pack(fill=tk.X , side="left" , expand=True )
        self.button_import_object.pack(fill=tk.X , side="left" , expand=True)
        # ساخت Canvas و Scrollbar
        self.canvas = tk.Canvas(self.frame_canvas, width=400, height=300, bg="white")
        self.scrollbar = tk.Scrollbar(self.frame_canvas, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # اتصال اسکرول
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # ساخت Frame داخل Canvas
        self.objects_frame = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.objects_frame, anchor="center")

        self._import_objects()

        # تنظیم اسکرول هنگام تغییر اندازه
        self.objects_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # فعال‌سازی اسکرول موس روی کل برنامه
        self.root_tl.bind_all("<MouseWheel>", self._on_mousewheel)   # ویندوز/مک
        self.root_tl.bind_all("<Button-4>", self._on_mousewheel)     # لینوکس بالا
        self.root_tl.bind_all("<Button-5>", self._on_mousewheel)     # لینوکس پایین

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
    
    def new_object(self):
        self.root_tl.attributes("-topmost", False) #Always be at top
        new_object = object_inputer(self.root_tl , self.objects_frame , self.var_check_bone.get())

    def _import_objects(self):
        try :
            dir = ft.open_data()["obj_file_path"]
            if os.path.exists(dir):
                objects = ft.open_data(dir)
                objects_names = list(objects.keys())
                for i in objects_names:
                    frame_items = tk.Frame(self.objects_frame , bd=1 , relief="solid")
                    label_name = tk.Label(frame_items , text = f"Name : {i}")
                    label_loc = tk.Label(frame_items , text = f"Location : X({objects[i]["location"]["x"]})  Y({objects[i]["location"]["y"]})  Z({objects[i]["location"]["z"]})")
                    label_rot = tk.Label(frame_items , text = f"Rotation : X({objects[i]["rotation"]["x"]})  Y({objects[i]["rotation"]["y"]})  Z({objects[i]["rotation"]["z"]})")
                    label_scale = tk.Label(frame_items , text = f"Scale : X({objects[i]["scale"]["x"]})  Y({objects[i]["scale"]["y"]})  Z({objects[i]["scale"]["z"]})")
                    
                    label_name.pack(pady=5)
                    label_loc.pack(pady=5)
                    label_rot.pack(pady=5)
                    label_scale.pack(pady=5)
                    frame_items.pack(pady=10)

                    try:
                        label_Head = tk.Label(frame_items , text = f"Head : X({objects[i]["Head"]["x"]})  Y({objects[i]["Head"]["y"]})  Z({objects[i]["Head"]["z"]})")
                        label_Tail = tk.Label(frame_items , text = f"Tail : X({objects[i]["Tail"]["x"]})  Y({objects[i]["Tail"]["y"]})  Z({objects[i]["Tail"]["z"]})")
                        label_Roll = tk.Label(frame_items , text = f"Roll : Degree({objects[i]["Roll"]})")
                        label_Head.pack(pady=5)
                        label_Tail.pack(pady=5)
                        label_Roll.pack(pady=5)
                    except Exception as e:
                        pass
            else :
                self.root_tl.attributes("-topmost", False)
                dir = ft.open_file("Select a json file" , type_files=[("objects.json" , "*objects.json") , ("json" , ".json") , ("txt" , ".txt")])
                ft.import_data(data={"obj_file_path" : dir} , mode="update")
                objects = ft.open_data(dir)
                objects_names = list(objects.keys())
                self.root_tl.attributes("-topmost", True)
                for i in objects_names:
                    frame_items = tk.Frame(self.objects_frame , bd=1 , relief="solid")
                    label_name = tk.Label(frame_items , text = f"Name : {i}")
                    label_loc = tk.Label(frame_items , text = f"Location : X({objects[i]["location"]["x"]})  Y({objects[i]["location"]["y"]})  Z({objects[i]["location"]["z"]})")
                    label_rot = tk.Label(frame_items , text = f"Rotation : X({objects[i]["rotation"]["x"]})  Y({objects[i]["rotation"]["y"]})  Z({objects[i]["rotation"]["z"]})")
                    label_scale = tk.Label(frame_items , text = f"Scale : X({objects[i]["scale"]["x"]})  Y({objects[i]["scale"]["y"]})  Z({objects[i]["scale"]["z"]})")
                    
                    label_name.pack(pady=5)
                    label_loc.pack(pady=5)
                    label_rot.pack(pady=5)
                    label_scale.pack(pady=5)
                    frame_items.pack(pady=10)

                    try:
                        label_Head = tk.Label(frame_items , text = f"Head : X({objects[i]["Head"]["x"]})  Y({objects[i]["Head"]["y"]})  Z({objects[i]["Head"]["z"]})")
                        label_Tail = tk.Label(frame_items , text = f"Tail : X({objects[i]["Tail"]["x"]})  Y({objects[i]["Tail"]["y"]})  Z({objects[i]["Tail"]["z"]})")
                        label_Roll = tk.Label(frame_items , text = f"Roll : Degree({objects[i]["Roll"]})")
                        label_Head.pack(pady=5)
                        label_Tail.pack(pady=5)
                        label_Roll.pack(pady=5)
                    except Exception as e:
                        pass
        except Exception as e:
            messagebox.showerror(title="Error" , message=f"{e}")


class code_panel_class:
    def __init__(self , root , main_root):
        self.root = root
        self.main_root = main_root

        self.frame_buttons = tk.Frame(self.root)
        self.frame_texts = tk.Frame(self.root)

        self.frame_buttons.pack(fill=tk.X , expand=True)
        self.frame_texts.pack(fill=tk.BOTH , expand=True)

        self.button_new = tk.Button(self.frame_buttons , text="New" , command=self.new_action)
        self.button_open = tk.Button(self.frame_buttons , text="Open" , command=self.open_action)
        self.button_import = tk.Button(self.frame_buttons , text="Import" , command=self.import_action)
        self.button_objects = tk.Button(self.frame_buttons , text="Objects" , command=self.objects_action)
        self.button_save = tk.Button(self.frame_buttons , text="Save" , command=self.save_action)
        self.button_save_as = tk.Button(self.frame_buttons , text="Save as" , command=self.save_as_action)
        self.button_copy = tk.Button(self.frame_buttons , text="Copy" , command=self.copy_action)

        self.button_new.pack(fill=tk.X , padx=5 , pady=5 , expand=True , side=button_sides)
        self.button_open.pack(fill=tk.X , padx=5 , pady=5 , expand=True , side=button_sides)
        self.button_import.pack(fill=tk.X , padx=5 , pady=5 , expand=True , side=button_sides)
        self.button_objects.pack(fill=tk.X , padx=5 , pady=5 , expand=True , side=button_sides)
        self.button_save.pack(fill=tk.X , padx=5 , pady=5 , expand=True , side=button_sides)
        self.button_save_as.pack(fill=tk.X , padx=5 , pady=5 , expand=True , side=button_sides)
        self.button_copy.pack(fill=tk.X , padx=5 , pady=5 , expand=True , side=button_sides)

        self.text_code_area = tk.Text(self.frame_texts , width=110) #edit panel size
        self.text_code_area.pack(fill=tk.BOTH , padx=5 , pady=5 , expand=True)
    
    def new_action(self):
        try :
            new_action = creat_new_project_class(self.root , self.main_root)
            self.text_code_area.delete("1.0" , tk.END)
            self.main_root.title("*new project")
            ft.import_data(data=temp)
        except Exception as e:
            messagebox.showerror(title="Error" , message=f"{e}")
    
    def open_action(self):
        dir = ft.open_file()
        self.main_root.title(f"{dir}")
        self.text_code_area.delete("1.0" , tk.END)
        with open (dir , "r+" ,  encoding="utf-8") as f:
            self.text_code_area.insert("1.0" , f.read())
    
    def import_action(self):
        try :
            dir = ft.open_file(type_files=[("details.json" , "*details.json") ,("json" , ".json")])
            details = ft.get_json_data(dir)
            ft.import_data(data=details)
            self.text_code_area.delete("1.0" , tk.END)
            with open(details["file_path"] , "r" , encoding="utf-8") as f:
                self.text_code_area.insert("1.0" , f.read())
            self.main_root.title(ft.open_data()["file_path"])
        except Exception as e:
            messagebox.showerror(title="Error" , message=f"{e}")
    
    def objects_action(self):
        objects_input(self.root)

    def save_action(self):
        try:
            with open(ft.get_json_data()["file_path"] , "w+" , encoding="utf-8") as f:
                f.write(self.text_code_area.get("1.0" , tk.END))
            messagebox.showinfo(title="Save operation was sucssesfully" , message="Your file has been saved")
        except Exception as e:
            messagebox.showerror(title="Error" , message=f"{e}")

    def save_as_action(self):
        save_as_class(self.root , self.main_root , self.text_code_area)

    def copy_action(self):
        try:
            pyperclip.copy(self.text_code_area.get("1.0" , tk.END))
            messagebox.showinfo(title="Copy operation was sucssesfully" , message="The codes copied in your clipboard")
        except Exception as e:
            messagebox.showerror(title="Error" , message=f"{e}")