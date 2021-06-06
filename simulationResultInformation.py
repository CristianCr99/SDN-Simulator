import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *

from scapy.layers.inet import IP

import Utilities as utilities


class ResultInformation(tk.Frame):
    def __init__(self, root, graph, list_flow, **kw):
        super().__init__(**kw)
        self.root = root
        self.graph = graph
        self.list_flow = list_flow

        self.initialize_user_interface()

    def on_configure(self, event):
        # update scrollregion after starting 'mainloop'
        # when all widgets are in canvas
        self.canvas.configure(scrollregion=self.canvas.bbox('all'), width=1500, height=500)

    def load_graph(self):

        if len(self.tree.selection()) > 0:
            selected_item = self.tree.selection()[0]
            host_flow = self.tree.item(selected_item)['values'][0]
            print('host_flow', host_flow)
            self.img = PhotoImage(file='./GraphsImages/' + host_flow + '.png')
            self.canvas_img.create_image(0, 0, anchor=NW, image=self.img)


    def initialize_user_interface(self):

        # --- create canvas with scrollbar ---

        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(side=tk.LEFT)
        scrollbar = tk.Scrollbar(self.root, command=self.canvas.yview)
        scrollbar.pack(side=tk.LEFT, fill='y')
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', self.on_configure)
        frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=frame)

        self.campos = tk.LabelFrame(self.canvas) #  text='host flows'
        self.campos.pack()

        self.tree = ttk.Treeview(self.campos, height=18)
        self.tree['show'] = 'headings'
        self.tree["columns"] = ("1", "2", "3", "4", "5", "6")
        self.tree.heading('1', text='Flow')
        self.tree.heading('2', text='Src IP')
        self.tree.heading('3', text='Dst IP')
        self.tree.heading('4', text='Src Port')
        self.tree.heading('5', text='Dst Port')
        self.tree.heading('6', text='Transp. Protocol')
        self.tree.column('1', minwidth=120, width=120, stretch=False)
        self.tree.column('2', minwidth=120, width=120, stretch=False)
        self.tree.column('3', minwidth=120, width=120, stretch=False)
        self.tree.column('4', minwidth=120, width=120, stretch=False)
        self.tree.column('5', minwidth=120, width=120, stretch=False)
        self.tree.column('6', minwidth=120, width=120, stretch=False)

        self.tree.grid(row=0, column=0)

        tk.Button(self.canvas, text=" Load Graph ", command=self.load_graph, height=1, width=15).pack(side = BOTTOM)

        for node in self.graph.get_graph().nodes:
            if node[0] == 'h' and node in self.list_flow:
                i = 1
                for flow in self.list_flow[node].items():
                    packet_delay_list = flow[1].get_packet_delay_list()
                    # print('Flujo', flow[0], ':', packet_delay_list)

                    list_delays = [i[0] for i in packet_delay_list]
                    util = utilities.Utilities()
                    packet = flow[1].get_packet()

                    if 'TCP' in packet:
                        protocol = 'TCP'
                    else:
                        protocol = 'UDP'

                    self.tree.insert('', 'end', iid=node + '_' + str(i), values=(
                        node + '_' + str(i), packet[IP].src, packet[IP].dst, packet[protocol].sport,
                        packet[protocol].dport, protocol))

                    util.create_graph(y=list_delays, x=list(range(1, len(list_delays) + 1)),
                                      x_label='Packet (number)', y_label='Delay (ms)',
                                      title_graph='Delay per Packet - Node: ' + node + ' Flow: ' + str(i), name=node + '_' + str(i) + '.png',
                                      dpi=80, bbox_inches='tight')

                    i += 1


        self.canvas_img = Canvas(self.campos, width=500, height=390)  # width=400, height=350
        self.canvas_img.grid(row=0, column=1)