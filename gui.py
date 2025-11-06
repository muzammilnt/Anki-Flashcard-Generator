
from tkinter import *
from fetch_definition import get_definition
from upload_to_anki import upload_anki, is_anki_listening, ensure_deck_exists

"""
Contains the AnkiGUI class, which builds a Tkinter-based interface for entering words,
selecting card types, and optionally including pronunciation. 
It integrates with AnkiConnect to upload definitions, example sentences, and pronunciation (if chosen) to Anki.
"""

class AnkiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Anki-GPT")
        self.root.configure(background="black")

        # Center the window
        window_width = 1300
        window_height = 750
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        y = (screen_height // 2) - (window_height // 2)
        x = (screen_width // 2) - (window_width // 2)
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")


        # ==== Dropdown ====
        self.drop = StringVar()
        options = ["Basic", "Basic (and reversed card)"]
        self.drop.set(options[1])
        dropbox = OptionMenu(root, self.drop, *options)
        dropbox.config(bg="#101010", fg="white", width=29,
                       activebackground="#212121", activeforeground="white",
                       bd=0, font=("Arial", 15), highlightthickness=0)
        dropbox["menu"].config(bg="#101010", fg="white",
                               activebackground="#212121", activeforeground="white",
                               bd=0, font=("Arial", 15), border=0)
    
        # Place the dropbox
        dropbox.place(relx=0.5, rely=0.33, anchor='center')


        # ==== Entry box ====
        self.ent = Entry(root)
        self.ent.config(width=29, background="#101010", foreground="white",
                        borderwidth=0, bd=0, font=("Arial", 25), justify="center")
        self.ent.focus_set()

        # Place the entry box
        self.ent.place(relx=0.5, rely=0.5, anchor='center')


        # ==== Checkbox ====
        self.checkbox = IntVar()
        self.checkbox.set(1)
        cb = Checkbutton(root, text="Include pronunciation", variable=self.checkbox)
        cb.config(background="black", foreground="white",
                  selectcolor="#212121", bd=0, highlightthickness=0,
                  activebackground="#101010", activeforeground="white", font=("Arial", 12))

        # Place the checkbox
        cb.place(relx=0.5, rely=0.6, anchor='center')


        # ==== Status bar ====
        self.status = Label(root, text="", bd=1, anchor="w", font=("Arial", 19))
        self.status.grid(column=1, columnspan=1, row=6, sticky="w")

        # ==== Submit button ====
        submit_button = Button(root, command=self.submit, text="Submit",
                               bg="#101010", fg="white", height=2, width=30,
                               activeforeground="white", activebackground="#212121",
                               bd=0, highlightthickness=0)
        submit_button.grid(row=20, column=1, columnspan=2, pady=(15, 70))

        # Place the submit button
        submit_button.place(relx=0.5, rely=0.7, anchor='center')

        # Bind Enter key
        self.ent.bind("<Return>", self.submit)
        

    def show_status(self, duration=3000):
        self.status.config(text="Done!", fg="white", bg="black")
        self.root.after(duration, lambda: self.status.config(text=""))

    def error_window(self, error_msg):
        popup_width = 350
        popup_height = 150

        popup = Toplevel(self.root)
        popup.transient(self.root)
        popup.grab_set()
        popup.title("Error")
        popup.config(bg="#080808")

        # Get root window position and size
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()

        # Center popup relative to root window
        x = root_x + (root_width // 2) - (popup_width // 2)
        y = root_y + (root_height // 2) - (popup_height // 2)
        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

        def close_popup(event=None):
                popup.destroy()
                self.root.unbind("<Return>")
                self.ent.focus_set()

        # Create content frame
        frame = Frame(popup, bg="#080808", padx=20, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Error message
        error_message = Label(frame, text=error_msg,
                            bg="#080808", fg="white", pady=24, font=("Arial", 12))
        error_message.pack()

        # OK button
        ok_button = Button(frame, text="OK", command=close_popup,
                        bg="#101010", fg="white", width=11,
                        activeforeground="white", activebackground="#212121",
                        bd=0, highlightthickness=0)
        ok_button.pack()

        ok_button.focus_set()
        # Bind Enter key to close the popup
        ok_button.bind("<Return>", close_popup)

    def submit(self, event=None):
        word = self.ent.get()
        card_type = self.drop.get()
        checkb = self.checkbox.get()
        if not word:
            return

        #check if ankiConnect is on
        if not is_anki_listening():
            self.error_window("Couldn't detect AnkiConnect.")
            return
        
        #store the definition
        result = get_definition(word)

        if isinstance(result, tuple):
            definition, mp3 = result
        else:
            definition, mp3 = result, None


        #check if there's no definition
        if definition is None:
            self.error_window("This word might not exist.")
            return

        # create a deck if not existed. Deck name : "vocabulary-auto"
        ensure_deck_exists()
        
        #upload based on checkbox
        if checkb == 1 and mp3:
            upload_anki(word, definition, card_type, mp3)
        else:
            upload_anki(word, definition, card_type)

        #show status (done) with a one-second delay.
        self.root.after(1000, self.show_status)


        #clear the entry box
        self.ent.delete(0, 'end')



 
