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

    def on_click(self,r,c):
        if self.btns[r][c]["text"] != " ":
            return
        self.btns[r][c]["text"] = self.sign[0]
        self.sign = [self.sign[1], self.sign[0]]
        self.checked += 1
        pass


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


if __name__ == "__main__":
    root = tk.Tk()
    root.title("test")
    root.geometry("300x350")
    field = Field(root)
    field.field_fill()
    root.mainloop()
