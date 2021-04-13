import json
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox

from networkx.readwrite import json_graph


class Application(tk.Frame):
    def __init__(self, root):
        self.root = root
        self.initialize_user_interface()

    def edit(self, mac_src, mac_dst, ip_src, ip_dst, sport, dport):
        selected_item = self.treeview.selection()[0]
        self.treeview.item(selected_item, values=(mac_src, mac_dst, ip_src, ip_dst, sport, dport))

    def delete(self):
        selected_item = self.treeview.selection()[0]
        self.treeview.delete(selected_item)

    def initialize_user_interface(self):

        # Set the treeview
        self.tree = ttk.Treeview(self.root, columns=('Num Packet', 'MAC Source', 'MAC Destination', 'IP Source', 'IP Destination', 'Port Source', 'Port Destination'))
        # Set the heading (Attribute Names)
        self.tree.heading('#0', text='Num Packet')
        self.tree.heading('#1', text='MAC Source')
        self.tree.heading('#2', text='MAC Destination')
        self.tree.heading('#3', text='IP Source')
        self.tree.heading('#4', text='IP Destination')
        self.tree.heading('#5', text='Port Source')
        self.tree.heading('#6', text='Port Destination')
        # Specify attributes of the columns (We want to stretch it!)
        self.tree.column('#0', stretch=tk.YES)
        self.tree.column('#1', stretch=tk.YES)
        self.tree.column('#2', stretch=tk.YES)
        self.tree.column('#3', stretch=tk.YES)
        self.tree.column('#4', stretch=tk.YES)
        self.tree.column('#5', stretch=tk.YES)
        self.tree.column('#6', stretch=tk.YES)
        self.tree.grid(row=1, columnspan=1)
        self.treeview = self.tree

        tk.Button(self.root, text="del", command=self.delete).grid(row=2, columnspan=1)
        tk.Button(self.root, text="edit", command=self.edit).grid(row=3, columnspan=2)
        for i in range(0, 100):
            self.treeview.insert('', 'end', text=i, values=('hola1', 'hola2', 'hola3', 'hola4', 'hola5', 'hola6'))

    def load_packages(self):
        # Seleccionamos el fichero
        try:
            path = filedialog.askopenfile(title='Load Graph', initialdir='./Packages', filetypes=(('Files .pcap', '*.pcap'), (('All Files', '*.*'))))

        except Exception as er:
            messagebox.showwarning(er)
        #self.verInformacionGrafo(G)
        #except Exception as er:
        #    print(er)

    def insert_data(self):
        self.treeview.insert('', 'end', values=('hola', 'hola'))

app = Application(tk.Tk())
app.root.mainloop()