import tkinter as tk
from gui import AnkiGUI


def main():
    """Create the main Tkinter window and start the GUI loop."""
    root = tk.Tk()
    AnkiGUI(root)
    root.mainloop()



if __name__ == "__main__":
    main() #run the app
