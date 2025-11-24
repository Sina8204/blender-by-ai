from tkinter import filedialog as fd
import sys , os , json

class file_tools:
    def __init__(self):
        pass

    def import_data(self , name = "temp.json" , data = {} , mode = 'w+'):
        if mode != "update":
            with open(name , mode , encoding = 'utf-8') as f:
                json.dump(data , f , ensure_ascii=False , indent=2)
        else:
            temp = {}
            with open(name , "r+" , encoding = 'utf-8') as f:
                temp = json.load(f)
            temp.update(data)
            with open(name , "w+" , encoding = 'utf-8') as f:
                json.dump(temp , f , ensure_ascii=False , indent=2)
    
    def open_data(self , name = "temp.json"):
        with open(name , "r+" , encoding = 'utf-8') as f:
            return json.load(f)
    
    def edit_data(self , key , value):
        data = self.open_data()
        if key in list(data):
            data.update({key : value})
            print(data)
            self.import_data(data)

    def open_file(self , Title = "Select a file" , type_files = []):
        return fd.askopenfilename(title=Title , filetypes=type_files)

    def open_folder(self , Title = "Select a folder"):
        return fd.askdirectory(title=Title)
    
    def save_file(self):
        return fd.asksaveasfilename(title="Test")
    
    def creat_file(self , path , name , mode = "w+"):
        with open (f"{path}/{name}" , mode , encoding="utf-8") as file:
            file.write("")
        return f"{path}/{name}"
    
    def creat_json(self , path , name , data = {}):
        with open(f"{path}/{name}.json" , "w+" , encoding = 'utf-8') as f:
            json.dump(data , f , ensure_ascii=False , indent=2)
        return f"{path}/{name}.json"
    
    def get_json_data(self , path_name = "temp.json"):
        with open(path_name , "r+" , encoding="utf-8") as f:
            return json.load(f)