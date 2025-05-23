from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror
import random

class Cell:
    cell_size = 40
    def __init__(self, is_bomb, x, y, master, text=" "):
        self.__is_bomb = is_bomb
        self.__flag = StringVar(value=text)
        self.label = ttk.Label(master=master, text=f"{'*' if self.__is_bomb else ' '}")
        self.label.grid(row=y, column=x)
        self.btn = ttk.Button(master=master, textvariable=self.__flag, command=self.open)
        self.btn.grid(row=y, column=x, sticky='nsew')
        self.btn.bind('<Button-3>', self.change_flag)

    # Вскрывает клетку
    def open(self):
        self.btn.grid_forget()
        if self.__is_bomb:
            root.GG_WP()

    def change_flag(self, event):
        if self.__flag.get() == " ": self.__flag.set("!")
        elif self.__flag.get() == "!": self.__flag.set("?")
        elif self.__flag.get() == "?": self.__flag.set(" ")
        else: log_print("Неизвестный флаг у Cell", is_error=True)

    def forget(self):
        self.btn.grid_remove()
        self.label.grid_remove()

class Window(Tk):
    def __init__(self, x="400", y="400"):
        super().__init__()
        self.title = "Сапёр"
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry(f'{x}x{y}+{width//2}+{height//2}')
        self.resizable(False, False)

        # виджеты окна
        self.main_menu_widgets = dict()
        modes = ["Легко", "Средне", "Сложно"]
        self.mode = StringVar(value=modes[1])
        self.main_menu_widgets["title_label"] = ttk.Label(text="Сапёр. Просто сапёр.", font=('Times New Roman', 15))
        self.main_menu_widgets["start_game_button"] = ttk.Button(text="Начать игру", command=choose_mode)
        self.main_menu_widgets["choose_mode"] = ttk.Combobox(state='readonly', values=modes, textvariable=self.mode)

        self.cells = []

    def drawGameDesk(self, width, height):
        pass

    def drawMainMenu(self):
        for key in self.main_menu_widgets:
            if key == "choose_mode":
                self.main_menu_widgets[key].pack(pady=10)
                continue
            self.main_menu_widgets[key].pack(pady=10, ipady=15)

    def restartAllWidgets(self):
        for key in self.main_menu_widgets:
            self.main_menu_widgets[key].pack_forget()

        for cell in self.cells:
            cell.label.grid_forget()
            cell.btn.grid_forget()
            self.cells.remove(cell)

    # Заканчивает игру (проигрыш)
    def GG_WP(self):
        showerror(title="GAME OVER", message="Вы проиграли.")
        self.restartAllWidgets()
        self.drawMainMenu()

    # Заканчивает игру (выигрыш)
    def ura_ura_ura(self):
        showinfo(title="URA POBEDA", message="Вы выиграли.")
        self.restartAllWidgets()
        self.drawMainMenu()

def choose_mode():
    root.restartAllWidgets()
    cell_size = 10
    match root.mode.get():
        case "Легко": pass
        case "Средне": cell_size = 15
        case "Сложно": cell_size = 20

    start_game(cell_size)

def start_game(cell_size):
    for c in range(cell_size): root.columnconfigure(c, weight=1)
    for r in range(cell_size): root.rowconfigure(r, weight=1)
    root.geometry(f"{Cell.cell_size * cell_size}x{Cell.cell_size * cell_size}")

    cords = [] # координаты всех клеток
    for y in range(cell_size):
        for x in range(cell_size):
            cords.append((x, y))
    bomb_cords = [] # координаты всех бомб (сразу без повторений)
    for i in range(cell_size):
        bomb_cord = random.choice(cords)
        bomb_cords.append(bomb_cord)
        cords.remove(bomb_cord)
    for y in range(cell_size):
        result = []
        for x in range(cell_size):
            is_bomb = True if (x, y) in bomb_cords else False
            result.append(Cell(is_bomb, x, y, master=root))
        root.cells.append(result)
    for i in range(len(root.cells)):
        for j in range(len(root.cells)):
            if root.cells[i][j] == '*': pass
            elif root.cells[i][j].label["text"] == ' ':
                # print(root.cells[i][j].label["text"])
                result = 0
                try:
                    if root.cells[i][j+1].label["text"] == '*': result += 1
                except: pass
                try:
                    if root.cells[i][j-1].label["text"] == '*': result += 1
                except: pass
                try:
                    if root.cells[i+1][j].label["text"] == '*': result += 1
                except: pass
                try:
                    if root.cells[i-1][j].label["text"] == '*': result += 1
                except: pass
                try:
                    if root.cells[i+1][j+1].label["text"] == '*': result += 1
                except: pass
                try:
                    if root.cells[i+1][j-1].label["text"] == '*': result += 1
                except: pass
                try:
                    if root.cells[i-1][j-1].label["text"] == '*': result += 1
                except: pass
                try:
                    if root.cells[i-1][j+1].label["text"] == '*': result += 1
                except: pass
                if result != 0: root.cells[i][j].label["text"] = result

def log_print(message, is_error=False, is_warning=False, is_info=False):
    if is_error: print("[ERROR]", message + "!")
    elif is_warning: print("[WARNING]", message + "?")
    elif is_info: print("[INFO]", message + ".")
    else: log_print("Неизвестный флаг log_print", is_error=True)

if __name__ == "__main__":
    root = Window()
    root.drawMainMenu()

    root.mainloop()