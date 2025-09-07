
from tkinter import *
from fetch_definition import get_definition
from upload_to_anki import upload_anki, is_anki_listening

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
        options = ["Basic", "Basic (and reversed card)+"]
        self.drop.set(options[1])
        dropbox = OptionMenu(root, self.drop, *options)
        dropbox.config(bg="#101010", fg="white", width=29,
                       activebackground="#212121", activeforeground="white",
                       bd=0, font=("Arial", 15), highlightthickness=0)
        dropbox["menu"].config(bg="#101010", fg="white",
                               activebackground="#212121", activeforeground="white",
                               bd=0, font=("Arial", 15), border=0)
        # Calculate center x for dropbox
        dropbox.update_idletasks()
        drop_width = dropbox.winfo_reqwidth()
        center_x_dropbox = (window_width // 2) - (drop_width // 2)

        # Place the dropbox
        dropbox.place(x=center_x_dropbox, y=250)


        # ==== Entry box ====
        self.ent = Entry(root)
        self.ent.config(width=29, background="#101010", foreground="white",
                        borderwidth=0, bd=0, font=("Arial", 25), justify="center")
        self.ent.focus_set()

        # Calculate centered x position
        self.ent.update_idletasks()
        entry_width = self.ent.winfo_reqwidth()
        center_x_entry = (window_width // 2) - (entry_width // 2)

        # Place the entry box
        self.ent.place(x=center_x_entry, y=400)


        # ==== Checkbox ====
        self.checkbox = IntVar()
        self.checkbox.set(1)
        cb = Checkbutton(root, text="Include pronunciation", variable=self.checkbox)
        cb.config(background="black", foreground="white",
                  selectcolor="#212121", bd=0, highlightthickness=0,
                  activebackground="#101010", activeforeground="white", font=("Arial", 12))

        # Calculate centered x position
        cb.update_idletasks()  # Make sure size is calculated
        entry_width = cb.winfo_reqwidth()  # Get required width in pixels
        center_x_cb = (window_width // 2) - (entry_width // 2)

        # Place the checkbox
        cb.place(x=center_x_cb, y=470)  # Adjust y as needed


        # ==== Status bar ====
        self.status = Label(root, text="", bd=1, anchor="w", font=("Arial", 19))
        self.status.grid(column=1, columnspan=1, row=6, sticky="w")

        # ==== Submit button ====
        submit_button = Button(root, command=self.submit, text="Submit",
                               bg="#101010", fg="white", height=2, width=30,
                               activeforeground="white", activebackground="#212121",
                               bd=0, highlightthickness=0)
        submit_button.grid(row=20, column=1, columnspan=2, pady=(15, 70))

        # Calculate centered x position
        submit_button.update_idletasks()
        entry_width = submit_button.winfo_reqwidth()
        center_x_sb = (window_width // 2) - (entry_width // 2)

        # Place the S button
        submit_button.place(x=center_x_sb, y=550)

        # Bind Enter key
        self.ent.bind("<Return>", self.submit)

    def show_status(self, duration=3000):
        self.status.config(text="Done!", fg="white", bg="black")
        self.root.after(duration, lambda: self.status.config(text=""))

    def error_window(self, error_msg):
        popup_width = 350
        popup_height = 150
        popup = Toplevel()
        popup.title("Error")
        popup.geometry(f"{popup_width}x{popup_height}")
        popup.config(bg="#080808")

        # Get screen size
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()

        # Calculate x and y coordinates to center the popup
        x = (screen_width // 2) - (popup_width // 2)
        y = (screen_height // 2) - (popup_height // 2)

        # Set popup size and position
        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

        frame = Frame(popup, bg="#080808", padx=20, pady=20)
        frame.pack()
        error_message = Label(frame, text=error_msg,
                              bg="#080808", fg="white", pady=24, font=("Arial", 12))
        error_message.pack()
        ok_button = Button(frame, text="OK", command=popup.destroy,
                           bg="#101010", fg="white", width=11,
                           activeforeground="white", activebackground="#212121",
                           bd=0, highlightthickness=0)
        ok_button.pack()

    def submit(self, event=None):
        word = self.ent.get()
        card_type = self.drop.get()
        checkb = self.checkbox.get()
        if not word:
            return

        #store the definition
        definition, mp3 = get_definition(word)

        #check if ankiConnect is on
        if not is_anki_listening():
            self.error_window("Couldn't detect AnkiConnect.")
            return

        #check if there's no definition
        if definition is None:
            self.error_window("This word might not exist.")
            return

        #upload based on checkbox
        if checkb == 1:
            upload_anki(word, definition, card_type, mp3)
        else:
            upload_anki(word, definition, card_type)

        #show status (done) with a one-second delay.
        self.root.after(1000, self.show_status)


        #clear the entry box
        self.ent.delete(0, 'end')



