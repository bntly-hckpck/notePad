import tkinter
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *

# to-do: 'new tab', finish 'edit' menu.

class NotePad:
    # main window
    def __init__(self, root):
        self.root = root
        root.title("notePad")
        window_width = 900
        window_height = 600

        # track current filepath, empty if new/unsaved
        self.filename = ""

        # screen dimensions & center points
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_center = int(screen_width/2 - window_width/2)
        y_center = int(screen_height/2 - window_height/2)
        root.geometry(f'{window_width}x{window_height}+{x_center}+{y_center}') # centering window

        # text area
        self.text = tkinter.Text(bg="black", fg="#39ff24", font=("TkFixedFont", 12), wrap=WORD, padx=9, pady=9) # black bg, green text, word wrap
        self.text.pack(expand=True, fill="both") # fill entire window
        self.text.config(insertbackground="#39ff24", insertwidth=3) # make cursor visible

        # menu bar
        menu_bar = Menu(root, bg="black", fg="#39ff24", font=("TkFixedFont", 12)) # creation
        root.config(menu=menu_bar) # attach to window

        # file dropdown on menu bar
        file_menu = Menu(menu_bar, bg="black", fg="#39ff24", activebackground="white") # dropdown menu
        menu_bar.add_cascade(label="file", menu=file_menu) # add "file" to menu bar
        file_menu.add_command(label="new tab")
        file_menu.add_command(label="open file", command=self.open_file) # "open" item
        file_menu.add_command(label="save file", command=self.save_current, accelerator="Ctrl+S") # "save" in current file
        file_menu.add_command(label="save file as", command=self.save_as) # "save as" file

        # edit dropdown on menu bar
        edit_menu = Menu(menu_bar, bg="black", fg="#39ff24", activebackground="white")
        menu_bar.add_cascade(label="edit", menu=edit_menu)
        edit_menu.add_command(label="select all", accelerator="Ctrl+A", command=self.select_all)
        edit_menu.add_command(label="cut", accelerator="Ctrl+X")
        edit_menu.add_command(label="copy", accelerator="Ctrl+C")
        edit_menu.add_command(label="paste", accelerator="Ctrl+V")
        edit_menu.add_command(label="undo", accelerator="Ctrl+Z")
        edit_menu.add_command(label="redo", accelerator="Ctrl+Y")
        
        # other menu items
        menu_bar.add_command(label="about", command=self.about)  # "about" item
        menu_bar.add_command(label="quit", command=self.closing) # "quit" item

        # keyboard shortcuts
        self.root.bind("<Control-s>", lambda event: self.save_current())
        self.root.bind("<Control-a>", lambda event: self.select_all())

    # information popup method
    def about(self):
        about_window = Toplevel(self.root) # separate popup window
        about_window.title("about notePad")
        about_window.geometry("402x150")
        about_window.configure(bg="black")

        # "about" text
        info_label = Label(about_window, text="simple text editor made by using tkinter\n-bntly_hckpck", bg="black", fg="#39ff24", font=("TkFixedFont", 12), justify=CENTER)
        info_label.pack(expand=True, fill=BOTH, padx=9, pady=9)

        # "about" close button
        close_button = Button(about_window, text="ok", bg="black", fg="#39ff24", font=("TkFixedFont", 12), activebackground="white", command=about_window.destroy)
        close_button.pack(pady=(0, 18))

    # file opening method
    def open_file(self):
        file_path = askopenfilename(filetypes=[("text files", "*.txt"), ("all files", "*.*")]) # open dialog with file filters
        if file_path: # if user picks file
            try: # try executing code
                with open(file_path, 'r', encoding='utf-8') as file: # open file for reading
                    self.text.delete(1.0, END) # clear editor
                    self.text.insert(1.0, file.read()) # load file into editor
                    self.filename = file_path
                self.text.edit_modified(False) # loaded = no unsaved changes
            except Exception as error: # error catching
                showerror("error", f"unable to open file:\n{str(error)}")  # show error popup

    # "save as", choose file path
    def save_as(self):
        file_path = asksaveasfilename(defaultextension=".txt", filetypes=[("text files", "*.txt"), ("all files", "*.*")])
        if file_path:
            try:                                            
                with open(file_path, 'w', encoding='utf-8') as file: # open file for writing
                    file.write(self.text.get(1.0, END)) # write editor content to file
                self.text.edit_modified(False) # saved = no unsaved changes
            except Exception as error:
                showerror("error", f"unable to save file:\n{str(error)}")
    
    # "save" current file, overwriting existing one
    def save_current(self):
        if not self.filename: # if there is no file saved yet, ask how to save it as
            self.save_as()
            return
        if self.filename: # check if self.filename has value
            try:
                with open(self.filename, 'w', encoding='utf-8') as file:
                    file.write(self.text.get(1.0, END)) # try to overwrite it
                self.text.edit_modified(False)
            except Exception as error:
                showerror("error", f"unable to save file:\n{str(error)}")

    # "x" button / quit method
    def closing(self):
        if not self.text.edit_modified(): # if no unsaved changes
            self.root.destroy() # quit
        elif askyesno("quit", "discard unsaved changes?"): # else if present changes but user confirms quitting
            self.root.destroy() # quit

    # select all written text
    def select_all(self):
        self.text.tag_add(SEL, "1.0", "end-1c") # highlight all written text (excluding space after)
        self.text.mark_set(INSERT, "1.0") # move cursor to beginning
        self.text.see(INSERT) # make selection visible
        return 'break' # prevent default tkinter behavior

# program startup
window = tkinter.Tk()
app = NotePad(window)
window.minsize(300, 300)
window.protocol("WM_DELETE_WINDOW", app.closing)
window.mainloop()
