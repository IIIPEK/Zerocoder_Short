import tkinter as tk
from tkinter import messagebox as mb
import platform

class Field:
    def __init__(self, window, font=("Arial", 20),width=5, height=2, size=3, callback=None):
        self.size = size
        self.window = window
        self.btns = []
        self.font = font
        self.btn_width = width
        self.btn_height = height
        self.checked = 0
        self.sign = ["X", "O"]
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
            elif ver == self.sign[0] * self.size or hor == self.sign[1] * self.size:
                return ver[0],i,"Vertical"

        diag =  "".join([self.btns[j][j]["text"] for j in range(self.size)])
        if diag == self.sign[0] * self.size or diag == self.sign[1] * self.size:
            return diag[0],0,"LeftUp"
        diag =  "".join([self.btns[j][self.size-j-1]["text"] for j in range(self.size)])
        if diag == self.sign[0] * self.size or diag == self.sign[1] * self.size:
            return diag[0],0,"LeftDown"
        return None

    def on_click(self,r,c):
        print(self.pause)
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
        self.checked = 0
        for i in range(self.size):
            for j in range(self.size):
                if platform.system() == "Windows":
                    self.btns[i][j].config(bg="SystemButtonFace", activebackground="SystemButtonFace", text =" ")
                else:
                    self.btns[i][j].config(bg="lightgrey", activebackground="lightgrey")
                print("|"+self.btns[i][j]["text"], end="" )
            print("|")
        self.sign = [self.sign[1], self.sign[0]]
        self.window.update()

    def show_result(self):
        if self.result:
            if self.result[2] == "Horizontal":
                for i in range(self.size):
                    self.btns[result[1]][i]["bg"] = "red"
            elif self.result[2] == "Vertical":
                for i in range(self.size):
                    self.btns[i][result[1]]["bg"] = "red"
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
    def __init__(self, window = None, rounds = 10):
        self.window = window
        self.frm_scores = tk.Frame(self.window)
        self.scores = {"X":0,"O":0}
        self.round = 0
        self.rounds = rounds
        self.info = tk.Label(self.window,text=f"Счет X:{self.scores["X"]} O:{self.scores["O"]}" )
        self.info.pack()

    def scores_update(self,player = None):
        if player in ["X","O"]:
            self.scores[player]+=1
            self.info["text"] =f"Счет X:{self.scores["X"]} O:{self.scores["O"]}"




class GameWindow():
    def __init__(self,root, size=3):
        self.size = size
        self.root = root
        self.frm_header = Scores(self.root)
        self.frm_field = tk.Frame(root)
        self.field = Field(self.frm_field, size=self.size, callback=self.gameloop)
        self.frm_field.pack()
        self.frm_field.grid_rowconfigure(0, weight=1)
        self.frm_field.grid_columnconfigure(0, weight=1)
        self.field.field_fill()

    def gameloop(self, result):
        if result:
            print(result)
            msg = "Победа!", f"Победитель: {result[0]}"
            # if result[2] == "Horizontal":
            #     for i in range(self.size):
            #         self.field.btns[result[1]][i]["bg"] = "red"
            # elif result[2] == "Vertical":
            #     for i in range(self.size):
            #         self.field.btns[i][result[1]]["bg"] = "red"
            # elif result[2] == "LeftUp":
            #     for i in range(self.size):
            #         self.field.btns[i][i]["bg"] = "red"
            # elif result[2] == "LeftDown":
            #     for i in range(self.size):
            #         self.field.btns[i][self.size-i-1]["bg"] = "red"
            if result[2] == "Draw":
                msg = "Ничья!"
            self.field.pause = True
            self.field.show_result()
            self.frm_header.scores_update(result[0])
            self.root.update()
            mb.showinfo(msg)
            self.field.field_reset()
            #self.root.after(2000, self.field.field_reset)
            #sleep(2)




if __name__ == "__main__":
    root = tk.Tk()
    root.title("test")
    root.geometry("300x350")
    window = GameWindow(root)
    # field = Field(root)
    # field.field_fill()
    root.mainloop()
