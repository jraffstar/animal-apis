import requests
import tkinter as tk
from threading import *
from PIL import Image, ImageTk
import os

f = open("API_KEY.txt", "r")
API_KEY  = f.read()
save_path = "images/cat.jpg"

# Create directories used in program if they do not already exist
newpath = r'images/'
if not os.path.exists(newpath):
    os.makedirs(newpath)
newpath = r'images/perm/'
if not os.path.exists(newpath):
    os.makedirs(newpath)
newpath = r'images/perm/cat'
if not os.path.exists(newpath):
    os.makedirs(newpath)
newpath = r'images/perm/dog'
if not os.path.exists(newpath):
    os.makedirs(newpath)



class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        containter = tk.Frame(self)
        containter.pack(side = "top", fill = "both", expand = True)

        containter.grid_rowconfigure(0, weight = 1)
        containter.grid_columnconfigure(0, weight = 1)

        self.frames = {}

        for F in (home, catPage, dogPage):
            frame = F(containter, self)

            self.frames[F] = frame

            frame.grid(row = 0, column = 0, sticky = "nsew")

        self.show_frame(home)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class home(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        # Page buttons
        cat_page_button = tk.Button(self, text="Cats!", command=lambda:controller.show_frame(catPage))
        dog_page_button = tk.Button(self, text="Dogs!", command=lambda:controller.show_frame(dogPage))

        cat_page_button.pack()
        dog_page_button.pack()

class catPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        def fetch_image():
            r = requests.get(f"https://api.thecatapi.com/v1/images/search?api_key={API_KEY}")
            image_json = r.json()

            image = requests.get(image_json[0]["url"])

            if image.status_code == 200:
                with open(save_path, "wb") as file:
                    file.write(image.content)
                print("File downloaded successfully")

            else:
                print("NO")

        # Check whether the user has enabled the permanent store option
        def check_perm():
            global save_path
            print(bool_permanent_store.get())
            if bool_permanent_store.get() == 1:
                # Count how many images are in the directory currently
                dir_path = "images/perm/cat/"
                self.count = 0
                for path in os.listdir(dir_path):
                    if os.path.isfile(os.path.join(dir_path, path)):
                        self.count += 1

                save_path = f"images/perm/cat/cat{self.count}.jpg"
            else:
                save_path = "images/cat.jpg"

            fetch_image()

        def show_image():
            check_perm()

            print(save_path)
            if bool_permanent_store.get() == 1:
                img = Image.open(f"images/perm/cat/cat{self.count}.jpg")
            else:
                img = Image.open("images/cat.jpg")

            self.cat_image = ImageTk.PhotoImage(img)

            if hasattr(self, "image_label"):
                self.image_label.config(image=self.cat_image)
            else:
                self.image_label = tk.Label(self, image=self.cat_image)
                self.image_label.pack()
        
        def threading():
            t1=Thread(target=show_image)
            t1.start()


        display_image_button = tk.Button(self, text="Get random image", command=lambda:threading())
        display_image_button.pack()

        bool_permanent_store = tk.IntVar()
        permanent_store = tk.Checkbutton(self, text="Save images permanently?", variable=bool_permanent_store, onvalue=1)
        permanent_store.pack()

        home_page_button = tk.Button(self, text="Home", command=lambda:controller.show_frame(home))
        home_page_button.pack()


class dogPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def check_perm():
            global save_path
            print(bool_permanent_store.get())
            if bool_permanent_store.get() == 1:
                # Count how many images are in the directory currently
                dir_path = "images/perm/dog/"
                self.count = 0
                for path in os.listdir(dir_path):
                    if os.path.isfile(os.path.join(dir_path, path)):
                        self.count += 1

                save_path = f"images/perm/dog/dog{self.count}.jpg"
            else:
                save_path = "images/dog.jpg"

            fetch_dog_image()

        def fetch_dog_image():

            r = requests.get("https://dog.ceo/api/breeds/image/random")

            dog_json = r.json()
            dog_image = requests.get(dog_json["message"])

            if dog_image.status_code == 200:
                with open(save_path, "wb") as file:
                    file.write(dog_image.content)
                print("File downloaded successfully")
            else:
                print("NO")

        def show_dog_image():
            check_perm()

            if bool_permanent_store.get() == 1:
                img = Image.open(f"images/perm/dog/dog{self.count}.jpg")
            else:
                img = Image.open("images/dog.jpg")
            self.cat_image = ImageTk.PhotoImage(img)

            if hasattr(self, "image_label"):
                self.image_label.config(image=self.cat_image)
            else:
                self.image_label = tk.Label(self, image=self.cat_image)
                self.image_label.pack()

        
        def threading():
            t1=Thread(target=show_dog_image)
            t1.start()


        display_image_button = tk.Button(self, text="Get random image", command=lambda:threading())
        display_image_button.pack()

        bool_permanent_store = tk.IntVar()
        permanent_store = tk.Checkbutton(self, text="Save images permanently?", variable=bool_permanent_store, onvalue=1)
        permanent_store.pack()

        home_page_button = tk.Button(self, text="Home", command=lambda:controller.show_frame(home))
        home_page_button.pack()


root = tkinterApp()
root.mainloop()