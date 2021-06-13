# import matplotlib.pyplot as plt
#
# # x axis values
# y = [1000, 230, 1000, 2323, 200, 2231]
# # corresponding y axis values
# x = [1, 2, 3, 4, 5, 6]
#
# # plotting the points
# plt.plot(x, y, color='#80cbcf', linestyle='dashed', linewidth=2,
#          marker='o', markerfacecolor='#9aca64', markersize=12)
#
# # setting x and y axis range
# plt.ylim(0, 4000)
# plt.xlim(1, len(x))
#
# # naming the x axis
# plt.xlabel('Packet (number)')
# # naming the y axis
# plt.ylabel('Delay (ms)')
#
# # giving a title to my graph
# plt.title('Delay per Packet')
#
# # function to show the plot
# plt.show()

# import tkinter as tk
#
#
# def on_configure(event):
#     # update scrollregion after starting 'mainloop'
#     # when all widgets are in canvas
#     canvas.configure(scrollregion=canvas.bbox('all'))
#
#
# root = tk.Tk()
#
# # --- create canvas with scrollbar ---
#
# canvas = tk.Canvas(root)
# canvas.pack(side=tk.LEFT)
#
# scrollbar = tk.Scrollbar(root, command=canvas.yview)
# scrollbar.pack(side=tk.LEFT, fill='y')
#
# canvas.configure(yscrollcommand = scrollbar.set)
#
# # update scrollregion after starting 'mainloop'
# # when all widgets are in canvas
# canvas.bind('<Configure>', on_configure)
#
# # --- put frame in canvas ---
#
# frame = tk.Frame(canvas)
# canvas.create_window((0,0), window=frame, anchor='nw')
#
# # # --- add widgets in frame ---
# #
# # l = tk.Label(frame, text="Hello", font="-size 50")
# # l.pack()
# #
# # l = tk.Label(frame, text="World", font="-size 50")
# # l.pack()
# #
# # l = tk.Label(frame, text="Test text 1\nTest text 2\nTest text 3\nTest text 4\nTest text 5\nTest text 6\nTest text 7\nTest text 8\nTest text 9", font="-size 20")
# # l.pack()
#
# # --- start program ---
#
# root.mainloop()

import tkinter as tk

class Example(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)

        self.menubar = tk.Menu()
        self.test1Menu = tk.Menu()
        self.test2Menu = tk.Menu()
        self.menubar.add_cascade(label="Test1", menu=self.test1Menu)
        self.menubar.add_cascade(label="Test2", menu=self.test2Menu)

        self.test1Menu.add_command(label="Enable Test2", command=self.enable_menu)
        self.test1Menu.add_command(label="Disable Test2", command=self.disable_menu)
        self.test2Menu.add_command(label="One")
        self.test2Menu.add_command(label="Two")
        self.test2Menu.add_command(label="Three")
        self.test2Menu.add_separator()
        self.test2Menu.add_command(label="Four")
        self.test2Menu.add_command(label="Five")

        root.configure(menu=self.menubar)

    def enable_menu(self):
        self.menubar.entryconfig("Test2", state="normal")

    def disable_menu(self):
        self.menubar.entryconfig("Test2", state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x500")
    app = Example(root)
    app.pack(fill="both", expand=True)
    root.mainloop()