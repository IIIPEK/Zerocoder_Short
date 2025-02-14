import tkinter as tk
from tkinter import messagebox as mb
import platform

class Field:
    def __init__(self, window, font=("Arial", 20),width=5, height=2, size=3, callback=None, order = ["X", "O"]):
        self.size = size
        self.window = window
        self.btns = []
        self.font = font
        self.btn_width = width
        self.btn_height = height
        self.checked = 0
        self.sign = order
        self.winner = None
        self.callback = callback
        self.result = None
        self.pause = None


    def check_winner(self):
        for i in range(3):
            hor = "".join([char["text"] for char in self.btns[i][:]])
            ver = "".join([self.btns[j][i]["text"] for j in range(3)])
            if hor == self.sign[0] * self.size or hor == self.sign[1] * self.size:
                return hor[0],i,"Horizontal"
            elif ver == self.sign[0] * self.size or ver == self.sign[1] * self.size:
                return ver[0],i,"Vertical"

        diag =  "".join([self.btns[j][j]["text"] for j in range(self.size)])
        if diag == self.sign[0] * self.size or diag == self.sign[1] * self.size:
            return diag[0],0,"LeftUp"
        diag =  "".join([self.btns[j][self.size-j-1]["text"] for j in range(self.size)])
        if diag == self.sign[0] * self.size or diag == self.sign[1] * self.size:
            return diag[0],0,"LeftDown"
        return None

    def on_click(self,r,c):
        if self.pause:
            return
        if self.btns[r][c]["text"] != " ":
            return
        self.btns[r][c]["text"] = self.sign[0]
        self.sign = [self.sign[1], self.sign[0]]
        self.checked += 1
        result = self.check_winner()
        if result:
            self.result = result
            self.winner = result[0]
        else:
            if self.checked>=9:
                self.result = ["-",0,"Draw"]
                self.winner = "-"
        if self.callback and self.result:
            self.callback(self.result)





    def btn(self,row,column):
        return tk.Button(self.window, text=" ", font=self.font, width=self.btn_width, height=self.btn_height, command=lambda r = row, c = column: self.on_click(r,c))

    def field_fill(self):
        for i in range(self.size):
            row = []
            for j in range(self.size):
                btn =self.btn(i,j)
                btn.grid(row=i, column=j)
                row.append(btn)
            self.btns.append(row)

    def field_reset(self):
        self.pause = None
        self.result = None
        if self.checked % 2 == 0:
            self.sign = [self.sign[1], self.sign[0]]
        self.checked = 0
        for i in range(self.size):
            for j in range(self.size):
                if platform.system() == "Windows":
                    self.btns[i][j].config(bg="SystemButtonFace", activebackground="SystemButtonFace", text =" ")
                else:
                    self.btns[i][j].config(bg="lightgrey", activebackground="lightgrey")

        self.window.update()

    def show_result(self):
        if self.result:
            if self.result[2] == "Horizontal":
                for i in range(self.size):
                    self.btns[self.result[1]][i]["bg"] = "red"
            elif self.result[2] == "Vertical":
                for i in range(self.size):
                    self.btns[i][self.result[1]]["bg"] = "red"
            elif self.result[2] == "LeftUp":
                for i in range(self.size):
                    self.btns[i][i]["bg"] = "red"
            elif self.result[2] == "LeftDown":
                for i in range(self.size):
                    self.btns[i][self.size - i - 1]["bg"] = "red"
            elif self.result[2] == "Draw":
                for i in range(self.size):
                    for j in range(self.size):
                        self.btns[i][j]["bg"] = "yellow"


class  Scores():
    def __init__(self, window = None, rounds = 2, reset_callback = None):
        self.window = window
        self.frm_scores = tk.Frame(self.window)
        self.scores = {"X":0,"O":0}
        self.round = 1
        self.rounds = rounds
        self.reset_callback = reset_callback
        self.lbl_info = tk.Label(self.window,text=f"Счет X:{self.scores["X"]}  😎  O:{self.scores["O"]}",  font=("Arial", 12) )
        self.lbl_info.pack()
        self.lbl_rounds = tk.Label(self.window, text=f"Раунд {self.round} из {self.rounds}", font=("Arial", 12) )
        self.lbl_rounds.pack()
        self.btn_reset = tk.Button(self.window, text="🔄 Сброс игры 🔄 ", font=("Arial", 12), command=self.reset)
        self.btn_reset.pack(pady=10)

    def reset(self):
        self.scores = {"X":0,"O":0}
        self.round = 0
        self.scores_update()
        self.window.update()
        self.reset_callback()




    def scores_update(self,player = None):
        if player in ["X","O"]:
            self.scores[player]+=1
        self.lbl_info["text"] = f"Счет X:{self.scores['X']}  😎  O:{self.scores['O']}"
        self.round += 1
        self.lbl_rounds["text"] = f"Раунд {self.round} из {self.rounds}"


class ResultWindow():
    def __init__(self, window=None, msg=None, geometry = "300x150", font=("Arial", 18)):
        self.wnd_result = tk.Toplevel(window)
        self.wnd_result.title(msg[0])
        self.geometry = geometry
        self.font = font
        self.wnd_result.geometry(self.geometry)
        self.message = msg[1]
        self.wnd_result.resizable(False, False)
        self.lbl = tk.Label(self.wnd_result, text=self.message, font=self.font)
        self.lbl.pack(pady=20)
        btn_ok = tk.Button(self.wnd_result, text="OK", command=self.wnd_result.destroy, font=self.font )
        btn_ok.pack()
        self.wnd_result.transient(window)  # Привязываем к главному окну
        self.wnd_result.grab_set()  # Блокируем события для главного окна
        self.wnd_result.focus_set()  # Фокус на модальном окне
        self.wnd_result.update_idletasks()
        root_x = window.winfo_x()
        root_y = window.winfo_y()
        root_w = window.winfo_width()
        root_h = window.winfo_height()
        self.x = root_x + (root_w // 2) - (self.wnd_result.winfo_width() // 2)
        self.y = root_y # + (root_h // 2) - (self.wnd_result.winfo_height() // 2)
        self.wnd_result.geometry(f"+{self.x}+{self.y}")
        self.wnd_result.wait_window()



class GameWindow():
    def __init__(self,root, size=3, rounds=10, icon="./img/ttt-67px.png"):
        self.size = size
        self.root = root
        self.rounds = rounds
        self.frm_header = Scores(self.root, reset_callback=self.reset_game, rounds=self.rounds)
        self.frm_field = tk.Frame(root)
        self.icon = icon
        self.field = Field(self.frm_field, size=self.size, callback=self.gameloop)
        self.frm_field.pack()
        self.frm_field.grid_rowconfigure(0, weight=1)
        self.frm_field.grid_columnconfigure(0, weight=1)
        self.field.field_fill()
        self.root.iconphoto(True, tk.PhotoImage(file=self.icon))

    def gameloop(self, result):
        if result:
            msg = "🥳 Победа! ", f"🎉 Победитель: {result[0]} 👏"
            if result[2] == "Draw":
                msg = "Ничья! 🤔","🔥 Ничья! 🔥"
            self.field.pause = True
            self.field.show_result()
            self.frm_header.scores_update(result[0])
            self.root.update()
            result_window = ResultWindow(self.root,msg)
            if self.frm_header.round > self.frm_header.rounds:
                if self.frm_header.scores["X"] > self.frm_header.scores["O"]:
                   text = f"🎉 Победил X : {result[0]} :{result[1]} : O 👏"
                elif self.frm_header.scores["X"] < self.frm_header.scores["O"]:
                   text = f"🎉 Победил O : {result[1]} : {result[0]} : X 👏"
                else:
                   text = f"🎉 Ничья X : {result[0]} :{result[1]} : O 👏"
                msg = "🥳 Игра окончена! ", text
                result_window = ResultWindow(self.root,msg)
                self.frm_header.reset()

            self.field.field_reset()

    def reset_game(self):
        self.field.field_reset()
        self.field.pause = False





if __name__ == "__main__":
    root = tk.Tk()
    root.title("Крестики-нолики")
    root.geometry("300x380")
    root.resizable(False, False)
    window = GameWindow(root)
    # field = Field(root)
    # field.field_fill()
    root.mainloop()
