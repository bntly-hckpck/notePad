import sys
import tkinter
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter import colorchooser

# to-do: "new tab"/"quit tab"/"save all"

if sys.platform == "darwin":
    modifier = "Command"
    accelerator = "Cmd"
else:
    modifier = "Control"
    accelerator = "Ctrl"

class NotePad:
    # main window
    def __init__(self, root):
        self.root = root
        root.title("notePad")
        window_width = 900
        window_height = 600
        self.status = Label(root, text="status: ready", anchor=W, bg="black", fg="#39ff24")
        self.status.pack(side=BOTTOM, fill=X)

        # track current filepath, empty if new/unsaved
        self.filename = ""
        self.fontsize = 12
        self.font= "DejaVu Sans Mono"

        # screen dimensions & center points
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_center = int(screen_width/2 - window_width/2)
        y_center = int(screen_height/2 - window_height/2)
        root.geometry(f'{window_width}x{window_height}+{x_center}+{y_center}') # centering window

        # text area
        self.text = tkinter.Text(undo=True, bg="black", fg="#39ff24", font=(self.font, self.fontsize), wrap=WORD, padx=9, pady=9) # black bg, green text, word wrap
        self.text.pack(side=LEFT, expand=True, fill="both") # fill entire window
        self.text.config(insertbackground="#39ff24", insertwidth=3) # make cursor visible

        # scrollbar
        self.scrollbar = tkinter.Scrollbar(self.root)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.text.config(yscrollcommand=self.scrollbar.set) # update slider position
        self.scrollbar.config(command=self.text.yview) # move content up/down

        # menu bar
        menu_bar = Menu(root, bg="black", fg="#39ff24", font=(self.font, 12)) # creation
        root.config(menu=menu_bar) # attach to window

        # file dropdown on menu bar
        file_menu = Menu(menu_bar, bg="black", fg="#39ff24", activebackground="white") # dropdown menu
        menu_bar.add_cascade(label="file", menu=file_menu) # add "file" to menu bar
        file_menu.add_command(label="new", command=self.new_file, accelerator=f"{accelerator} + N")
        file_menu.add_command(label="new tab", state=DISABLED)
        file_menu.add_separator()
        file_menu.add_command(label="open file", command=self.open_file, accelerator=f"{accelerator} + O") # "open" item
        file_menu.add_command(label="save file", command=self.save_current, accelerator=f"{accelerator} + S") # "save" in current file
        file_menu.add_command(label="save file as", command=self.save_as) # "save as" file
        file_menu.add_command(label="save all", state=DISABLED)
        file_menu.add_separator()
        file_menu.add_command(label="refresh", command=self.refresh)
        file_menu.add_command(label="quit tab", state=DISABLED)
        file_menu.add_command(label="quit", accelerator=f"{accelerator} + Q", command=self.closing)

        # edit dropdown on menu bar
        edit_menu = Menu(menu_bar, bg="black", fg="#39ff24", activebackground="white")
        menu_bar.add_cascade(label="edit", menu=edit_menu)
        edit_menu.add_command(label="select all", accelerator=f"{accelerator} + A", command=self.select_all)
        edit_menu.add_command(label="delete selection", accelerator="delete", command=self.delete_selection)
        edit_menu.add_command(label="cut", accelerator=f"{accelerator} + X", command=self.cut_text)
        edit_menu.add_command(label="copy", accelerator=f"{accelerator} + C", command=self.copy_text)
        edit_menu.add_command(label="paste", accelerator=f"{accelerator} + V", command=self.paste_text)
        edit_menu.add_separator()
        edit_menu.add_command(label="undo", accelerator=f"{accelerator} + Z", command=self.undoing)
        edit_menu.add_command(label="redo", accelerator=f"{accelerator} + Y", command=self.redoing)
        edit_menu.add_separator()
        edit_menu.add_command(label="zoom in", accelerator=f"{accelerator} + +", command=self.font_up)
        edit_menu.add_command(label="zoom out", accelerator=f"{accelerator} + -", command=self.font_down)
        edit_menu.add_command(label="reset zoom", accelerator=f"{accelerator} + 0", command=self.font_normal)

        # theme menu
        theme_menu = Menu(menu_bar, bg="black", fg="#39ff24", activebackground="white")
        menu_bar.add_cascade(label="theme", menu=theme_menu)
        theme_menu.add_command(label="terminal", command=self.terminal_theme)
        theme_menu.add_command(label="coffee", command=self.coffee_theme)
        theme_menu.add_command(label="ocean", command=self.ocean_theme)
        theme_menu.add_separator()
        theme_menu.add_command(label="custom text", command=self.text_color)
        theme_menu.add_command(label="custom background", command=self.bg_color)
        
        # other menu items
        menu_bar.add_command(label="about", command=self.about)  # "about" item

        # keyboard shortcuts
        self.root.bind(f"<{modifier}-s>", lambda event: self.save_current())
        self.root.bind(f"<{modifier}-a>", lambda event: self.select_all())
        self.text.bind(f"<{modifier}-z>", lambda event: self.undoing())
        self.text.bind(f"<{modifier}-y>", lambda event: self.redoing())
        self.root.bind(f"<{modifier}-q>", lambda event: self.closing())
        self.root.bind(f"<{modifier}-o>", lambda event: self.open_file())
        self.root.bind(f"<{modifier}-n>", lambda event: self.new_file())
        self.root.bind(f"<{modifier}-plus>", lambda event: self.font_up())
        self.root.bind(f"<{modifier}-minus>", lambda event: self.font_down())
        self.root.bind(f"<{modifier}-0>", lambda event: self.font_normal())


        # keyboard shortcuts already implemented by default tkinter
        # self.root.bind(f"<{modifier}-x>", lambda event: self.cut_text())
        # self.root.bind(f"<{modifier}-c>", lambda event: self.copy_text())
        # self.root.bind(f"<{modifier}-v>", lambda event: self.paste_text())

    # information popup method
    def about(self):
        about_window = Toplevel(self.root) # separate popup window
        about_window.title("about notePad")
        about_window.geometry("420x150")
        about_window.configure(bg="black")

        # "about" text
        info_label = Label(about_window, text="simple text editor made by using tkinter\n-bntly_hckpck", bg="black", fg="#39ff24", font=(self.font, 12), justify=CENTER)
        info_label.pack(expand=True, fill=BOTH, padx=9, pady=9)

        # "about" close button
        close_button = Button(about_window, text="ok", bg="black", fg="#39ff24", font=(self.font, 12), activebackground="white", command=about_window.destroy)
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
                self.status.config(text=f"status: opened -> {self.filename}")
                self.root.after(6000, lambda: self.status.config(text="status: ready"))
            except Exception as error: # error catching
                showerror("error", f"unable to open file:\n{str(error)}")  # show error popup

    # "save as", choose file path
    def save_as(self):
        file_path = asksaveasfilename(defaultextension=".txt", filetypes=[("text files", "*.txt"), ("all files", "*.*")])
        if file_path:
            try:                                            
                with open(file_path, 'w', encoding='utf-8') as file: # open file for writing
                    file.write(self.text.get(1.0, END)) # write editor content to file
                self.filename = file_path
                self.text.edit_modified(False) # saved = no unsaved changes
                self.status.config(text=f"status: saved as -> {self.filename}")
                self.root.after(6000, lambda: self.status.config(text="status: ready"))
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
                self.status.config(text=f"status: saved current -> {self.filename}")
                self.root.after(6000, lambda: self.status.config(text="status: ready"))
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

    # copy selected text
    def copy_text(self):
        text = self.text.get("sel.first", "sel.last")
        self.root.clipboard_clear()
        self.root.clipboard_append(text)

    # paste copied text
    def paste_text(self):
        text = self.root.clipboard_get()
        self.text.insert("insert", text)

    # cut selected text
    def cut_text(self):
        text = self.text.get("sel.first", "sel.last")
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.text.delete("sel.first", "sel.last")

    # undo last modification
    def undoing(self):
        try:  
            self.text.edit_undo()
        except tkinter.TclError:
            pass  
        return "break"

    # redo last modification
    def redoing(self):
        try:
            self.text.edit_redo()
        except tkinter.TclError:
            pass
        return "break"

    # refresh file
    def refresh(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                self.text.delete(1.0, END)
                self.text.insert(1.0, file.read())
            self.text.edit_modified(False)
            self.status.config(text=f"status: refreshed file")
            self.root.after(6000, lambda: self.status.config(text="status: ready"))
        except Exception as error:
            showerror("error", f"unable to refresh:\n{str(error)}")
    
    # new file
    def new_file(self):
        if not self.text.edit_modified():
            self.text.delete(1.0, END)
            self.filename = ""
        elif askyesno("new file", "discard unsaved changes?"):
            self.text.delete(1.0, END)
            self.filename = ""
        self.status.config(text=f"status: created new file")
        self.root.after(6000, lambda: self.status.config(text="status: ready"))

    # make font bigger
    def font_up(self):
        if (self.fontsize + 3) <= 42:
            self.fontsize += 3
            self.text.config(font=(self.font, self.fontsize))

    # make font smaller
    def font_down(self):
        if (self.fontsize - 3) >= 6:
            self.fontsize -= 3
            self.text.config(font=(self.font, self.fontsize))

    # return font to normal
    def font_normal(self):
        self.fontsize = 12
        self.text.config(font=(self.font, self.fontsize))

    # delete selected text
    def delete_selection(self):
        try:  
            self.text.delete("sel.first", "sel.last")
        except tkinter.TclError:
            pass  
        return "break"

    # change typing color
    def text_color(self):
        color = colorchooser.askcolor(title="choose text color")
        if color[1]:
            self.text.config(fg=color[1], insertbackground=color[1])
        self.status.config(text=f"status: changed text color")
        self.root.after(6000, lambda: self.status.config(text="status: ready"))

    # change background color
    def bg_color(self):
        color = colorchooser.askcolor(title="choose background color")
        if color[1]:
            self.text.config(bg=color[1])
        self.status.config(text=f"status: changed background color")
        self.root.after(6000, lambda: self.status.config(text="status: ready"))

    # themes
    def terminal_theme(self):
        self.text.config(bg="black", fg="#39ff24", insertbackground="#39ff24")
        self.status.config(text=f"status: using terminal theme")
        self.root.after(6000, lambda: self.status.config(text="status: ready"))
    def coffee_theme(self):
        self.text.config(bg="#5d4037", fg="#e1ddd6", insertbackground="#e1ddd6")
        self.status.config(text=f"status: using coffee theme")
        self.root.after(6000, lambda: self.status.config(text="status: ready"))
    def ocean_theme(self):
        self.text.config(bg="#003459", fg="#ade8f4", insertbackground="#ade8f4")
        self.status.config(text=f"status: using ocean theme")
        self.root.after(6000, lambda: self.status.config(text="status: ready"))

# program startup
window = tkinter.Tk()
app = NotePad(window)
window.minsize(300, 300)
window.protocol("WM_DELETE_WINDOW", app.closing)
window.mainloop()
