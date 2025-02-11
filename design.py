import tkinter as tk


class Field:
    def __init__(self,window, font=("Arial", 20),width=5, height=2, size=3):
        self.size = size
        self.window = window
        self.btns = []
        self.font = font
        self.btn_width = width
        self.btn_height = height
        self.checked = 0
        self.sign = ["X", "O"]
        self.winner = None
        self.

    def check_winner(self):
        for i in range(3):
            hor = "".join([char["text"] for char in self.btns[i][:]])
            ver = "".join([self.btns[j][i]["text"] for j in range(3)])
            if hor == self.sign[0] * self.size or hor == self.sign[1] * self.size:
                return hor[0],i,"Horizontal"
            if ver == self.sign[0] * self.size or hor == self.sign[1] * self.size:
                return ver[0],i,"Vertical"
        dlu =  "".join([self.btns[j][j]["text"] for j in range(self.size)])
        if dlu == self.sign[0] * self.size or dlu == self.sign[1] * self.size:
            return dlu[0],0,"LeftUp"
        dld =  "".join([self.btns[j][self.size-j]["text"] for j in range(self.size)])
        if dld == self.sign[0] * self.size or dld == self.sign[1] * self.size:
            return dld[0],0,"LeftDown"
        return None

    def on_click(self,r,c):
        if self.btns[r][c]["text"] != " ":
            return
        self.btns[r][c]["text"] = self.sign[0]
        self.sign = [self.sign[1], self.sign[0]]
        self.checked += 1
        result = self.check_winner()
        if result:
            self.winner = result[0]
        else:
            if self.checked>=9:





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
        self.btns = []
        self.sign = [self.sign[1], self.sign[0]]
        self.field_fill()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("test")
    root.geometry("300x350")
    field = Field(root)
    field.field_fill()
    root.mainloop()
