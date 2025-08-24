import customtkinter 
import json
import os

#make the json file save in the same folder as the script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENTRIES_FILE = os.path.join(BASE_DIR, "entries.json")

#main frame
app = customtkinter.CTk()
app.geometry("500x400")
app.title("Books Journal")
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

#frames
Books_Add = customtkinter.CTkFrame(app)
TBR = customtkinter.CTkFrame(app)
Books_Read = customtkinter.CTkFrame(app)
Main_Menu = customtkinter.CTkFrame(app)
Reading = customtkinter.CTkFrame(app)
#make a frame fill up the window
for frame in (Books_Add, TBR, Books_Read, Main_Menu, Reading):
    frame.place(relwidth=1, relheight=1)

#function to show frames
def Show_Frame(frame):
    frame.tkraise()
    if frame == TBR:
        display_titles()
    if frame == Reading:
        display_titlesReading()
    if frame == Books_Read:
         display_titlesread()


#Main Menu frame
label_main = customtkinter.CTkLabel(Main_Menu, text="Books Journal", font=("Arial", 42, "bold"))
label_main.place(relx = 0.5, rely=0.1, anchor="center")

btn_Books_Add = customtkinter.CTkButton(Main_Menu, text="Add books.", command=lambda: [Show_Frame(Books_Add)], width=190)
btn_Books_Add.place(relx=0.5, rely=0.4, anchor="center")

btn_TBR = customtkinter.CTkButton(Main_Menu, text="To be read books.", command=lambda: [Show_Frame(TBR)], width=190)
btn_TBR.place(relx=0.5, rely=0.55, anchor="center")

btn_Currently_Reading = customtkinter.CTkButton(Main_Menu, text="Books you're currently reading.", command=lambda: [Show_Frame(Reading)], width=190)
btn_Currently_Reading.place(relx=0.5, rely=0.7, anchor="center")

btn_Books_Read = customtkinter.CTkButton(Main_Menu, text="View books you have read", command=lambda: [Show_Frame(Books_Read)], width=190)
btn_Books_Read.place(relx=0.5, rely=0.85, anchor="center")


#books add frame
Add_Book_label = customtkinter.CTkLabel(Books_Add, text="Add books", font=("Arial", 42, "bold"))
Add_Book_label.place(relx=0.5, rely=0.1, anchor="center")

addbooks = customtkinter.CTkEntry(Books_Add, width=240, height=30, placeholder_text="Bookname (eg: House of Hades)")
addbooks.place(relx=0.5, rely=0.3, anchor="center")

btn_Save_Title = customtkinter.CTkButton(Books_Add, text="Save Title", command=lambda: [save_title()])
btn_Save_Title.place(relx=0.5, rely=0.8, anchor="center")

I_label = customtkinter.CTkLabel(Books_Add, text="I", font=("Arial", 20, "bold"))
I_label.place(relx = 0.31, rely=0.2, anchor="center")

choose_option = customtkinter.CTkComboBox(Books_Add, values=['will read this book.', 'am reading this book.', "have read this book."], width=170, height=28, state="readonly")
choose_option.place(relx=0.5, rely=0.2, anchor="center")

def save_title():
    Book_Title = addbooks.get().strip()
    choice = choose_option.get()

    if not Book_Title:
        return
    
    if os.path.exists(ENTRIES_FILE):
        with open(ENTRIES_FILE, "r") as f:
            try:
                entries = json.load(f)
            except json.JSONDecodeError:
                entries = []
    else:
        entries = {"TBR": [], "Reading": [], "Books_Read": []}
    
    #places books in right order
    if choice == "will read this book.":
        entries["TBR"].append(Book_Title)
    elif choice == "am reading this book.":
        entries["Reading"].append(Book_Title)
    elif choice == "have read this book.":
        entries["Books_Read"].append(Book_Title)

    with open(ENTRIES_FILE, "w") as file:
        json.dump(entries, file, indent=4)

    addbooks.delete(0, "end")

btn_GoToMainMenu =  customtkinter.CTkButton(Books_Add, text='Go to main menu', width=140, height=28, command=lambda: [Show_Frame(Main_Menu)])
btn_GoToMainMenu.place(relx= 0.5, rely=0.9, anchor="center")


#TBR screen
scroll_frame_tbr = customtkinter.CTkScrollableFrame(TBR, width=460, height=276)
scroll_frame_tbr.place(relx=0.5, rely=0.5, anchor="center")

tbr_counter_label = customtkinter.CTkLabel(TBR, text="Books I want to read: 0", font=("Arial", 14, "bold"))
tbr_counter_label.place(relx=0.5, rely=0.1, anchor="center")

def load_titels(category):
    if os.path.exists(ENTRIES_FILE):
        with open(ENTRIES_FILE, "r") as file:
            try: 
                data = json.load(file)
                if isinstance(data, dict) and category in data:
                    return data[category]
                else: 
                    return []
            except json.JSONDecodeError:
                return []
    else:
        return []

btn_GoToMainMenu =  customtkinter.CTkButton(TBR, text='Go to main menu', width=140, height=28, command=lambda: [Show_Frame(Main_Menu)])
btn_GoToMainMenu.place(relx= 0.5, rely=0.9, anchor="center")

def display_titles():
    for widget in scroll_frame_tbr.winfo_children():
        widget.destroy()
    
    Titles = load_titels("TBR")
    tbr_counter_label.configure(text=f"Books i want to read: {len(Titles)}")
    if not Titles:
        label = customtkinter.CTkLabel(scroll_frame_tbr, text="No book titles saved.", font=("Arial", 13))
        label.pack(pady=5)
    else:
        for title in Titles:
            label = customtkinter.label = customtkinter.CTkLabel(scroll_frame_tbr, text=title)
            label.pack(anchor="w", padx=10, pady=2)


#books that have been read screen
scroll_frame_read = customtkinter.CTkScrollableFrame(Books_Read, width=460, height=276)
scroll_frame_read.place(relx=0.5, rely=0.5, anchor="center")

read_counter_label = customtkinter.CTkLabel(Books_Read, text="Books I have read: 0", font=("Arial", 14, "bold"))
read_counter_label.place(relx=0.5, rely=0.1, anchor="center")

def display_titlesread():
    for widget in scroll_frame_read.winfo_children():
        widget.destroy()
    
    Titles = load_titels("Books_Read")
    read_counter_label.configure(text=f"Books read: {len(Titles)}")

    if not Titles:
        label = customtkinter.CTkLabel(scroll_frame_read, text="No book titles saved.", font=("Arial", 13))
        label.pack(pady=5)
    else:
        for title in Titles:
            label = customtkinter.label = customtkinter.CTkLabel(scroll_frame_read, text=title)
            label.pack(anchor="w", padx=10, pady=2)

btn_GoToMainMenu =  customtkinter.CTkButton(Books_Read, text='Go to main menu', width=140, height=28, command=lambda: [Show_Frame(Main_Menu)])
btn_GoToMainMenu.place(relx= 0.5, rely=0.9, anchor="center")


#books that are being read 
scroll_frame = customtkinter.CTkScrollableFrame(Reading, width=460, height=276)
scroll_frame.place(relx=0.5, rely=0.5, anchor="center")

reading_counter_label = customtkinter.CTkLabel(Reading, text="Books I am reading: 0", font=("Arial", 14, "bold"))
reading_counter_label.place(relx=0.5, rely=0.1, anchor="center")

btn_GoToMainMenu =  customtkinter.CTkButton(Reading, text='Go to main menu', width=140, height=28, command=lambda: [Show_Frame(Main_Menu)])
btn_GoToMainMenu.place(relx= 0.5, rely=0.9, anchor="center")

def display_titlesReading():
    for widget in scroll_frame.winfo_children():
        widget.destroy()
    Titles = load_titels("Reading")
    reading_counter_label.configure(text=f"Books I am reading: {len(Titles)}")
    if not Titles:
        label = customtkinter.CTkLabel(scroll_frame, text="No book titles saved.", font=("Arial", 13))
        label.pack(pady=5)
    else:
        for title in Titles:
            label = customtkinter.label = customtkinter.CTkLabel(scroll_frame, text=title)
            label.pack(anchor="w", padx=10, pady=2)

#start in main menu
Show_Frame(Main_Menu)

app.mainloop()