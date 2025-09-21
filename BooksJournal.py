import customtkinter 
import json
import os

#make the json file save in the same folder as the script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENTRIES_FILE = os.path.join(BASE_DIR, "entries.json")

#main frame
app = customtkinter.CTk()
app.geometry("594x475")
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

#function to delete books
def delete_book(category, book_entry):
    if not os.path.exists(ENTRIES_FILE):
        return
    
    with open(ENTRIES_FILE, "r") as f:
        try:
            entries = json.load(f)
        except json.JSONDecodeError:
            entries = {"TBR": [], "Reading": [], "Books_Read": []}

    if book_entry in entries.get(category, []):
        entries[category].remove(book_entry)
    
    with open(ENTRIES_FILE, "w") as f:
        json.dump(entries, f, indent=4)

    if category == "TBR":
        display_titles()
    elif category == "Reading":
        display_titlesReading()
    elif category == "Books_Read":
        display_titlesread()

# function to edit book
def edit_book(category, old_book):
    edit_window = customtkinter.CTkToplevel(app)
    edit_window.title("Edit Book")
    edit_window.geometry("400x300")

    # Pre-fill entries
    title_entry = customtkinter.CTkEntry(edit_window, width=260, height=30, placeholder_text="Title (eg: House of Hades)")
    title_entry.insert(0, old_book.get("title", ""))
    title_entry.pack(pady=10)

    series_entry = customtkinter.CTkEntry(edit_window, width=260, height=30, placeholder_text="Series (eg: Heroes of Olympus)")
    series_entry.insert(0, old_book.get("series", ""))
    series_entry.pack(pady=10)

    author_entry = customtkinter.CTkEntry(edit_window, width=260, height=30, placeholder_text="Author (eg: Rick Riordan)")
    author_entry.insert(0, old_book.get("author", ""))
    author_entry.pack(pady=10)

    def save_changes():
        new_book = {
            "title": title_entry.get().strip(),
            "series": series_entry.get().strip(),
            "author": author_entry.get().strip()
        }

        if not os.path.exists(ENTRIES_FILE):
            return

        with open(ENTRIES_FILE, "r") as f:
            try:
                entries = json.load(f)
            except json.JSONDecodeError:
                entries = {"TBR": [], "Reading": [], "Books_Read": []}

        if old_book in entries.get(category, []):
            idx = entries[category].index(old_book)
            entries[category][idx] = new_book

        with open(ENTRIES_FILE, "w") as f:
            json.dump(entries, f, indent=4)

        # Refresh display
        if category == "TBR":
            display_titles()
        elif category == "Reading":
            display_titlesReading()
        elif category == "Books_Read":
            display_titlesread()

        edit_window.destroy()

    save_btn = customtkinter.CTkButton(edit_window, text="Save Changes", command=save_changes)
    save_btn.pack(pady=20)

#function to move books from frame to frame
def move_book(from_category, to_category, book_entry):
    if not os.path.exists(ENTRIES_FILE):
        return
    
    with open(ENTRIES_FILE, "r") as f:
        try:
            entries = json.load(f)
        except json.JSONDecodeError:
            entries = {"TBR": [], "Reading": [], "Books_Read": []}
    
    # Remove from old category
    entries[from_category] = [
        b for b in entries.get(from_category, [])
        if not (b["title"] == book_entry["title"] and b["author"] == book_entry["author"] and b["series"] == book_entry["series"])]
    
    # Add to new category
    entries[to_category].append(book_entry)

    with open(ENTRIES_FILE, "w") as f:
        json.dump(entries, f, indent=4)

    # Refresh UI
    if from_category == "TBR":
        display_titles()
    elif from_category == "Reading":
        display_titlesReading()
    elif from_category == "Books_Read":
        display_titlesread()

    if to_category == "TBR":
        display_titles()
    elif to_category == "Reading":
        display_titlesReading()
    elif to_category == "Books_Read":
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

addbooks = customtkinter.CTkEntry(Books_Add, width=260, height=30, placeholder_text="Booktitle (eg: House of Hades)")
addbooks.place(relx=0.5, rely=0.3, anchor="center")

books_series = customtkinter.CTkEntry(Books_Add, width=260, height=30, placeholder_text="Book series (eg: Heroes Of Olympus)")
books_series.place(relx=0.5, rely=0.4, anchor="center")

author = customtkinter.CTkEntry(Books_Add, width=260, height=30, placeholder_text="Author (eg: Rick Riordan)")
author.place(relx=0.5, rely=0.5, anchor="center")

btn_Save_Title = customtkinter.CTkButton(Books_Add, text="Save Title", command=lambda: [save_title()])
btn_Save_Title.place(relx=0.5, rely=0.8, anchor="center")

I_label = customtkinter.CTkLabel(Books_Add, text="I", font=("Arial", 20, "bold"))
I_label.place(relx = 0.31, rely=0.2, anchor="center")

choose_option = customtkinter.CTkComboBox(Books_Add, values=['will read this book.', 'am reading this book.', "have read this book."], width=170, height=28, state="readonly")
choose_option.place(relx=0.5, rely=0.2, anchor="center")

def save_title():
    Book_Title = addbooks.get().strip()
    Book_Series = books_series.get().strip()
    Book_Author = author.get().strip()
    choice = choose_option.get()

    if not Book_Title:
        return
    
    if os.path.exists(ENTRIES_FILE):
        with open(ENTRIES_FILE, "r") as f:
            try:
                entries = json.load(f)
            except json.JSONDecodeError:
                entries = {"TBR": [], "Reading": [], "Books_Read": []}
    else:
        entries = {"TBR": [], "Reading": [], "Books_Read": []}
    
    book_entry = {
        "title": Book_Title,
        "series": Book_Series,
        "author": Book_Author
    }


    #places books in right order
    if choice == "will read this book.":
        entries["TBR"].append(book_entry)
    elif choice == "am reading this book.":
        entries["Reading"].append(book_entry)
    elif choice == "have read this book.":
        entries["Books_Read"].append(book_entry)

    with open(ENTRIES_FILE, "w") as file:
        json.dump(entries, file, indent=4)

    addbooks.delete(0, "end")
    books_series.delete(0, "end")
    author.delete(0, "end")

btn_GoToMainMenu =  customtkinter.CTkButton(Books_Add, text='Go to main menu', width=140, height=28, command=lambda: [Show_Frame(Main_Menu)])
btn_GoToMainMenu.place(relx= 0.5, rely=0.9, anchor="center")


#TBR screen 
scroll_frame_tbr = customtkinter.CTkScrollableFrame(TBR, width=460, height=276)
scroll_frame_tbr.place(relx=0.5, rely=0.5, anchor="center")

tbr_counter_label = customtkinter.CTkLabel(TBR, text="Books I want to read: 0", font=("Arial", 14, "bold"))
tbr_counter_label.place(relx=0.62, rely=0.1, anchor="center")

sort_option_tbr = customtkinter.CTkComboBox(
    TBR, values=["Title", "Author", "Series"], 
    width=120, state="readonly", command=lambda choice: display_titles()
)
sort_option_tbr.set("Title")  # default sort
sort_option_tbr.place(relx=0.87, rely=0.1, anchor="center")

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
        return
    #Get search text
    query = search_entry_TBR.get().strip().lower()
    if query:
        Titles = [book for book in Titles if 
                  query in book["title"].lower() or
                  query in book ["author"].lower() or
                  query in book["series"].lower()]
    
    #apply sorting
    sort_by = sort_option_tbr.get().lower()
    if sort_by == "author":
        Titles.sort(key=lambda x: x.get("author", ""))
    elif sort_by == "series":
        Titles.sort(key=lambda x: x.get("series", ""))
    else:  # title
        Titles.sort(key=lambda x: x.get("title", ""))

    #display search results
    if not Titles:
        label = customtkinter.CTkLabel(scroll_frame_tbr, text="No matches found.", font=("Arial", 13))
        label.pack(pady=5)
        return

    for book in Titles:
        series = book.get("series", "").strip()
        title = book.get("title", "").strip()
        author = book.get("author", "").strip()

        if series:
            text = f"{series}: {title} by {author}"
        else:
            text = f"{title} by {author}"

        frame = customtkinter.CTkFrame(scroll_frame_tbr)
        frame.pack(fill="x", padx=5, pady=2)

        label = customtkinter.CTkLabel(
            frame,
            text=text,
            wraplength=200,   # max width before wrapping
            anchor="w",       # align text to the left
            justify="left"    # align multi-line text to left
            )
        label.pack(side="left", padx=10, pady=2, fill="x", expand=True)


        delete_btn = customtkinter.CTkButton(frame, text="Delete", width=60, command=lambda b=book: delete_book("TBR", b))
        delete_btn.pack(side="right", padx=5, pady=2)

        edit_btn = customtkinter.CTkButton(frame, text="Edit", width=60, command=lambda b=book: edit_book("TBR", b))
        edit_btn.pack(side="right", padx=5, pady=2)

        move_btn = customtkinter.CTkButton(frame, text="→ Reading", width=100, command=lambda b=book: move_book("TBR", "Reading", b))
        move_btn.pack(side="right", padx=5, pady=2)

        

#Search bar TBR
search_entry_TBR = customtkinter.CTkEntry(TBR, width=180, height=28, placeholder_text="Search...")
search_entry_TBR.place(relx=0.17, rely=0.1, anchor="center")
search_button_TBR = customtkinter.CTkButton(TBR, text="Search", width=80, height=28, command=lambda: display_titles())
search_button_TBR.place(relx=0.4, rely=0.1, anchor="center")

#bind enter key to search
def search_TBR_event(event=None):
    display_titles()

search_entry_TBR.bind("<Return>", search_TBR_event)

#books that have been read screen
scroll_frame_read = customtkinter.CTkScrollableFrame(Books_Read, width=460, height=276)
scroll_frame_read.place(relx=0.5, rely=0.5, anchor="center")

read_counter_label = customtkinter.CTkLabel(Books_Read, text="Books I have read: 0", font=("Arial", 14, "bold"))
read_counter_label.place(relx=0.62, rely=0.1, anchor="center")

sort_option_read = customtkinter.CTkComboBox(
    Books_Read, values=["Title", "Author", "Series"], 
    width=120, state="readonly", command=lambda choice: display_titlesread()
)
sort_option_read.set("Title")  # default sort
sort_option_read.place(relx=0.87, rely=0.1, anchor="center")

def display_titlesread():
    for widget in scroll_frame_read.winfo_children():
        widget.destroy()
    
    Titles = load_titels("Books_Read")
    read_counter_label.configure(text=f"Books I have read: {len(Titles)}")

    if not Titles:
        label = customtkinter.CTkLabel(scroll_frame_read, text="No book titles saved.", font=("Arial", 13))
        label.pack(pady=5)
        return
    
     # Get search text
    query = search_entry_read.get().strip().lower()
    if query:
        Titles = [book for book in Titles if 
                  query in book["title"].lower() or 
                  query in book["author"].lower() or 
                  query in book["series"].lower()]
        
    #apply sorting
    sort_by_read = sort_option_read.get().lower()
    if sort_by_read == "author":
        Titles.sort(key=lambda x: x.get("author", ""))
    elif sort_by_read == "series":
        Titles.sort(key=lambda x: x.get("series", ""))
    else:  # title
        Titles.sort(key=lambda x: x.get("title", ""))

        # Display search results
    if not Titles:
        label = customtkinter.CTkLabel(scroll_frame_read, text="No matches found.", font=("Arial", 13))
        label.pack(pady=5)
        return
    
    for book in Titles:
        series = book.get("series", "").strip()
        title = book.get("title", "").strip()
        author = book.get("author", "").strip()

        if series:  
            text = f"{series}: {title} by {author}"
        else:
            text = f"{title} by {author}"

        frame = customtkinter.CTkFrame(scroll_frame_read)
        frame.pack(fill="x", padx=5, pady=2)

        label = customtkinter.CTkLabel(
            frame,
            text=text,
            wraplength=200,   # max width before wrapping
            anchor="w",       # align text to the left
            justify="left"    # align multi-line text to left
            )
        label.pack(side="left", padx=10, pady=2, fill="x", expand=True)

        delete_btn = customtkinter.CTkButton(frame, text="Delete", width=60, command=lambda b=book: delete_book("Books_Read", b))
        delete_btn.pack(side="right", padx=5)

        edit_btn = customtkinter.CTkButton(frame, text="Edit", width=60, command=lambda b=book: edit_book("Books_Read", b))
        edit_btn.pack(side="right", padx=5, pady=2)
        
        move_btn = customtkinter.CTkButton(frame, text="→ TBR", width=100, command=lambda b=book: move_book("Books_Read", "TBR", b))
        move_btn.pack(side="right", padx=5, pady=2)



btn_GoToMainMenu =  customtkinter.CTkButton(Books_Read, text='Go to main menu', width=140, height=28, command=lambda: [Show_Frame(Main_Menu)])
btn_GoToMainMenu.place(relx= 0.5, rely=0.9, anchor="center")

#Search bar Read books
search_entry_read = customtkinter.CTkEntry(Books_Read, width=180, height=28, placeholder_text="Search...")
search_entry_read.place(relx=0.17, rely=0.1, anchor="center")
search_button_read = customtkinter.CTkButton(Books_Read, text="Search", width=80, height=28, command=lambda: display_titlesread())
search_button_read.place(relx=0.4, rely=0.1, anchor="center")

#bind enter key to search
def search_TBR_event(event=None):
    display_titles()

search_entry_TBR.bind("<Return>", search_TBR_event)

#books that are being read 
scroll_frame = customtkinter.CTkScrollableFrame(Reading, width=460, height=276)
scroll_frame.place(relx=0.5, rely=0.5, anchor="center")

reading_counter_label = customtkinter.CTkLabel(Reading, text="Books I am reading: 0", font=("Arial", 14, "bold"))
reading_counter_label.place(relx=0.62, rely=0.1, anchor="center")

btn_GoToMainMenu =  customtkinter.CTkButton(Reading, text='Go to main menu', width=140, height=28, command=lambda: [Show_Frame(Main_Menu)])
btn_GoToMainMenu.place(relx= 0.5, rely=0.9, anchor="center")

sort_option_reading = customtkinter.CTkComboBox(
    Reading, values=["Title", "Author", "Series"], 
    width=120, state="readonly", command=lambda choice: display_titlesReading()
) 
sort_option_reading.set("Title")  # default sort
sort_option_reading.place(relx=0.87, rely=0.1, anchor="center")

def display_titlesReading():
    for widget in scroll_frame.winfo_children():
        widget.destroy()
    Titles = load_titels("Reading")
    reading_counter_label.configure(text=f"Books I am reading: {len(Titles)}")
    if not Titles:
        label = customtkinter.CTkLabel(scroll_frame, text="No book titles saved.", font=("Arial", 13))
        label.pack(pady=5)
        return
    
    #Get search text
    query = search_entry_reading.get().strip().lower()
    if query:
        Titles = [book for book in Titles if 
                  query in book["title"].lower() or 
                  query in book["author"].lower() or 
                  query in book["series"].lower()]

    #apply sorting
    sort_by_reading = sort_option_reading.get().lower()
    if sort_by_reading == "author":
        Titles.sort(key=lambda x: x.get("author", ""))
    elif sort_by_reading == "series":
        Titles.sort(key=lambda x: x.get("series", ""))
    else:  # title
        Titles.sort(key=lambda x: x.get("title", ""))

    # Display results
    if not Titles:
        label = customtkinter.CTkLabel(scroll_frame, text="No matches found.", font=("Arial", 13))
        label.pack(pady=5)
        return

    for book in Titles:
        series = book.get("series", "").strip()
        title = book.get("title", "").strip()
        author = book.get("author", "").strip()

        if series:  
            text = f"{series}: {title} by {author}"

        else:
            text = f"{title} by {author}"
        
        frame = customtkinter.CTkFrame(scroll_frame)
        frame.pack(fill="x", padx=5, pady=2)

        label = customtkinter.CTkLabel(
            frame,
            text=text,
            wraplength=200,   # max width before wrapping
            anchor="w",       # align text to the left
            justify="left"    # align multi-line text to left
            )
        label.pack(side="left", padx=10, pady=2, fill="x", expand=True)

        delete_btn = customtkinter.CTkButton(frame, text="Delete", width=60, command=lambda b=book: delete_book("Reading", b))
        delete_btn.pack(side="right", padx=5)

        edit_btn = customtkinter.CTkButton(frame, text="Edit", width=60, command=lambda b=book: edit_book("Reading", b))
        edit_btn.pack(side="right", padx=5, pady=2)

        move_btn = customtkinter.CTkButton(frame, text="→ Read", width=100, command=lambda b=book: move_book("Reading", "Books_Read", b))
        move_btn.pack(side="right", padx=5, pady=2)

#Search bar reading
search_entry_reading = customtkinter.CTkEntry(Reading, width=180, height=28, placeholder_text="Search...")
search_entry_reading.place(relx=0.17, rely=0.1, anchor="center")
search_button_reading = customtkinter.CTkButton(Reading, text="Search", width=80, height=28, command=lambda: display_titlesReading())
search_button_reading.place(relx=0.4, rely=0.1, anchor="center")

#bind enter key to search
def search_TBR_event(event=None):
    display_titles()

search_entry_TBR.bind("<Return>", search_TBR_event)


#start in main menu
Show_Frame(Main_Menu)

app.mainloop()