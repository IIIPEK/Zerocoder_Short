import tkinter as tk
from design import GameWindow



if __name__ == "__main__":
    size = 3
    side=size*90+30
    root = tk.Tk()
    root.title("Крестики-нолики")
    root.geometry(f"{side}x{side+80}")
    root.resizable(False, False)
    window = GameWindow(root, size = size)
    root.mainloop()