import tkinter
import os
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *

class NotePad:
    # main window
    def __init__(self, root):
        # main window
        self.root = root
        root.title("notePad")
        window_width = 900
        window_height = 600

        # screen dimensions & center points
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_center = int(screen_width/2 - window_width / 2)
        y_center = int(screen_height/2 - window_height / 2)
        root.geometry(f'{window_width}x{window_height}+{x_center}+{y_center}') # centering window

        # text area 
        self.text = tkinter.Text(bg="black", fg="#39ff24", font=("TkFixedFont", 12), wrap=WORD, padx=9, pady=9)
        self.text.pack(expand=True, fill="both")

        # menu bar
        menu_bar = Menu(root, bg="black", fg="#39ff24", font=("TkFixedFont", 12))
        root.config(menu=menu_bar)

        # creating file menu section and adding it as a dropdown to the menu bar
        file_menu = Menu(menu_bar, bg="black", fg="#39ff24", activebackground="white")
        menu_bar.add_cascade(label="file", menu=file_menu)

        # "open file" button in the dropdown file menu
        file_menu.add_command(label='open file', command=self.open_file)

        # "save file" button in the dropdown file menu
        file_menu.add_command(label='save file', command=self.save_file)

        # adding info section to the menu bar
        menu_bar.add_command(label='about', command=self.about)

        # adding quitting option to the menu bar
        menu_bar.add_command(label='quit', command=self.closing)

    # information popup method
    def about(self):
        # popup "about" window
        about_window = Toplevel(self.root)
        about_window.title("about notePad")
        about_window.geometry("402x150")
        about_window.configure(bg="black")

        # "about" window's text
        info_label = Label(about_window, text="simple text editor made by using tkinter\n-bntly_hckpck", bg="black", fg="#39ff24", font=("TkFixedFont", 12), justify=CENTER)
        info_label.pack(expand=True, fill=BOTH, padx=9, pady=9)
        
        # "about" window's close button
        close_button = Button(about_window, text="ok", bg="black", fg="#39ff24", font=("TkFixedFont", 12), activebackground="white", command=about_window.destroy)
        close_button.pack(pady=(0, 18))

    # file opening method
    def open_file(self):
        file_path = askopenfilename(filetypes=[("text files", "*.txt*"), ("all files", "*.*")])
        if file_path:
            self.text.delete(1.0, END)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.text.insert(1.0, file.read())
            except Exception as error:
                showerror("error", f"unable to open file:\n{str(error)}")

    # file saving method
    def save_file(self):
        file_path = asksaveasfilename(defaultextension=".txt", filetypes=[("text files", "*.txt*"), ("all files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.text.get(1.0, END))
            except Exception as error:
                showerror("error", f"unable to save file:\n{str(error)}")
    
    # "x" button method
    def closing(self):
        if askyesno("quit", "discard unsaved changes?"):
            self.root.destroy()

# program startup
window = tkinter.Tk()
app = NotePad(window)
window.minsize(300, 300)
window.protocol("WM_DELETE_WINDOW", app.closing)
window.mainloop()
