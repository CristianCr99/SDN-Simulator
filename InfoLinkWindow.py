import tkinter as tk
import tkinter.ttk as ttk


class InfoLinkWindow(tk.Frame):
    def __init__(self, root, link_data, src_dst):
        self.root = root
        self.link_data = link_data
        self.src_dst = src_dst

    def initialize_user_interface(self):

        tk.Label(self.root, text=' ').grid(row=0, column=0)
        tk.Label(self.root, text='     ').grid(row=1, column=0)
        tk.Label(self.root, text='     ').grid(row=1, column=2)
        tk.Label(self.root, text='     ').grid(row=2, column=1)

        campos = tk.LabelFrame(self.root, text=' Parameters of Link [' + self.src_dst + '] ')
        campos.grid(row=1, column=1)

        tk.Label(campos, text=' ').grid(row=0, column=0)
        tk.Label(campos, text=' ').grid(row=4, column=0)
        tk.Label(campos, text="       Bandwidth:  ").grid(row=1, column=0, sticky='w')
        tk.Label(campos, text="       Distance:  ").grid(row=2, column=0, sticky='w')
        tk.Label(campos, text="       Propagation Speed:  ").grid(row=3, column=0, sticky='w')
        tk.Label(campos, text="       Mbps  ").grid(row=1, column=2, sticky='w')
        tk.Label(campos, text="       m  ").grid(row=2, column=2, sticky='w')
        tk.Label(campos, text="       m/s  ").grid(row=3, column=2, sticky='w')

        if 'bw' in self.link_data:
            tk.Label(campos, text=self.link_data['bw']).grid(row=1, column=1, sticky='w')
        if 'distance' in self.link_data:
            tk.Label(campos, text=self.link_data['distance']).grid(row=2, column=1, sticky='w')
        if 'propagation_speed' in self.link_data:
            tk.Label(campos, text=self.link_data['propagation_speed']).grid(row=3, column=1, sticky='w')
