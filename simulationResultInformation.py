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
            # print('host_flow', host_flow)
            self.img = PhotoImage(file='./GraphsImages/' + host_flow + '.png')
            self.canvas_img.create_image(0, 0, anchor=NW, image=self.img)

        if self.n != '':
            self.img_2 = PhotoImage(file='./GraphsImages/Link_Load_' + self.n.get() + '.png')
            self.canvas_img_2.create_image(0, 0, anchor=NW, image=self.img_2)

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

        self.campos = tk.LabelFrame(self.canvas, text= 'Information on the delay of each flow')  # text='host flows'
        self.campos.pack(padx=10, pady=10)

        self.tree = ttk.Treeview(self.campos, height=18)
        self.tree['show'] = 'headings'
        self.tree["columns"] = ("1", "2", "3", "4", "5", "6")
        self.tree.heading('1', text='Flow')
        self.tree.heading('2', text='Src IP')
        self.tree.heading('3', text='Dst IP')
        self.tree.heading('4', text='Src Port')
        self.tree.heading('5', text='Dst Port')
        self.tree.heading('6', text='Transp. Protocol')
        self.tree.column('1', minwidth=50, width=50, stretch=False)
        self.tree.column('2', minwidth=110, width=110, stretch=False)
        self.tree.column('3', minwidth=110, width=110, stretch=False)
        self.tree.column('4', minwidth=70, width=70, stretch=False)
        self.tree.column('5', minwidth=70, width=70, stretch=False)
        self.tree.column('6', minwidth=90, width=90, stretch=False)

        self.tree.grid(row=0, column=0, padx=10, pady=10)

        tk.Button(self.canvas, text=" Load Graph ", command=self.load_graph, height=1, width=15).pack(side=BOTTOM)

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
                                      title_graph='Delay per Packet - Node: ' + node + ' Flow: ' + str(i),
                                      name=node + '_' + str(i) + '.png',
                                      dpi=80, bbox_inches='tight', x_range_min=1, is_delay=True)

                    i += 1

        self.campos_load = tk.LabelFrame(self.canvas, text='Loading information for each link')  # text='host flows'
        self.campos_load.pack(padx=10, pady=10)

        ttk.Label(self.campos_load, text="Select the Link :").grid(row=1, column=0, sticky='NW', padx=10, pady=10)

        # Combobox creation
        self.n = tk.StringVar()
        # monthchoosen = ttk.OptionMenu(self.campos_load, textvariable=self.n)


        # Adding combobox drop down list
        links_list = []

        for link in self.graph.get_graph().edges(data=True):

            if 'load' in link[2]:
                print(link[0], link[1], link[2]['load'])


                lista = (link[2]['load']).copy()
                lista.reverse()
                seen = set()
                Output = [(a, b) for a, b in lista
                          if not (a in seen or seen.add(a))]
                Output.reverse()
                print(Output)
                # x = [j[0] for j in Output]
                # y = [i[1] for i in Output]

                x = []
                y = []
                for data in Output:
                    x.append(data[0])
                    y.append(data[1])

                if 0 < len(x) == len(y) > 0:
                    links_list.append('[' + link[0] + ',' + link[1] + ']')
                    util.create_graph(y=y, x_label='Time',
                                      x=x, y_label='Load (Bytes)',
                                      title_graph='Link Load: [' + link[0] + ',' + link[1] + ']',
                                      name='Link_Load_[' + link[0] + ',' + link[1] + ']' + '.png',
                                      dpi=80, bbox_inches='tight', x_range_min=0, is_delay=False)

        # util.create_graph_multiple(list_edges=self.graph.get_graph().edges(data=True), x_label='Time',
        #                            y_label='Load (Bytes)',
        #                            name='Links_Load.png', title_graph='Links Load', dpi=80, bbox_inches='tight')

        # monthchoosen['values'] = tuple(links_list)
        self.showHostsOption = tk.OptionMenu(self.campos_load, self.n, *links_list)
        self.showHostsOption.grid( row=0, column=0, sticky='NW', padx=10, pady=10)
        self.canvas_img = Canvas(self.campos, width=500, height=390)  # width=400, height=350
        self.canvas_img.grid(row=0, column=1,padx=10, pady=10)

        # monthchoosen.grid(column=1, row=1, sticky='NW')
        # monthchoosen.current()
        # ttk.Label(self.campos_load, text='      ').grid(column=0, row=0)
        # ttk.Label(self.campos_load, text='      ').grid(column=1, row=0)

        # ttk.Label(self.campos, text='      ').grid(column=0, row=0)
        # ttk.Label(self.campos, text='      ').grid(column=2, row=0)
        # ttk.Label(self.campos, text='      ').grid(column=0, row=2)
        # ttk.Label(self.campos, text='      ').grid(column=4, row=0)

        self.canvas_img_2 = Canvas(self.campos_load, width=700, height=390)  # width=400, height=350
        self.canvas_img_2.grid(row=1, column=3, padx=10, pady=10)