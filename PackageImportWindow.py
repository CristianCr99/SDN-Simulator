import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox

from scapy.layers.inet import *
from scapy.layers.l2 import Ether
from scapy.utils import rdpcap


class PackageImportWindow(tk.Frame):
    def __init__(self, root):
        self.port_dst = tk.StringVar()
        self.port_src = tk.StringVar()
        self.ip_dst = tk.StringVar()
        self.ip_src = tk.StringVar()
        self.mac_dst = tk.StringVar()
        self.mac_src = tk.StringVar()
        self.root = root
        self.initialize_user_interface()
        self.list_packets = []

    def edit(self,selected_item ,mac_src, mac_dst, ip_src, ip_dst, sport, dport):
        selected_item = self.tree.selection()[0]
        self.tree.item(selected_item, values=(mac_src, mac_dst, ip_src, ip_dst, sport, dport))

    def delete(self):
        if len(self.tree.selection()) > 0:
            selected_item = self.tree.selection()[0]
            # print(self.tree.item(selected_item))
            # self.tree.delete(selected_item)

            item_chain = str(selected_item)[1:]  # Eliminamos la I de la cadena I009 -> 009
            for i in item_chain:
                if i == '0':
                    item_chain = item_chain[1:]
                else:
                    break
            print('item seleccionado',item_chain)
            print('log de la lista de paquetes:',len(self.list_packets))
            self.list_packets.pop(int(item_chain, 16)-1)
            new_list = []
            for i in self.tree.get_children():
                self.tree.delete(i)

            self.tree.configure(yscrollcommand=self.scroll.set)
            self.tree = ttk.Treeview(self.root)
            self.tree.configure(yscrollcommand=self.scroll.set)

            self.tree['show'] = 'headings'
            self.tree["columns"] = ("1", "2", "3", "4", "5", "6", "7")
            # Set the heading (Attribute Names)
            self.tree.heading('1', text='Num Packet')
            self.tree.heading('2', text='MAC Source')
            self.tree.heading('3', text='MAC Destination')
            self.tree.heading('4', text='IP Source')
            self.tree.heading('5', text='IP Destination')
            self.tree.heading('6', text='Port Source')
            self.tree.heading('7', text='Port Destination')
            # Specify attributes of the columns (We want to stretch it!)
            self.tree.column('1', minwidth=120, width=120, stretch=False)
            self.tree.column('2', minwidth=120, width=120, stretch=False)
            self.tree.column('3', minwidth=120, width=120, stretch=False)
            self.tree.column('4', minwidth=120, width=120, stretch=False)
            self.tree.column('5', minwidth=120, width=120, stretch=False)
            self.tree.column('6', minwidth=120, width=120, stretch=False)
            self.tree.column('7', minwidth=120, width=120, stretch=False)
            self.tree.grid(row=0)
            i = 1
            for packet in self.list_packets:
                if 'MAC' in packet and 'IP' in packet and 'TCP' in packet or 'UDP' in packet:
                    new_list.append(packet)
                    if 'TCP' in packet:
                        inf = 'TCP'
                    else:
                        inf = 'UDP'

                    self.tree.insert('', 'end', values=(
                        i, packet[Ether].src, packet[Ether].dst, packet[IP].src, packet[IP].dst, packet[inf].sport,
                        packet[inf].dport))
                    i += 1

            self.list_packets = new_list

    def load_values(self):
        print('hola')
        if len(self.tree.selection()) > 0:
            print('holaas')
            selected_item = self.tree.selection()[0]
            print(self.tree.item(selected_item)['values'][1])
            self.mac_src.set(self.tree.item(selected_item)['values'][1])
            self.mac_dst.set(self.tree.item(selected_item)['values'][2])
            self.ip_src.set(self.tree.item(selected_item)['values'][3])
            self.ip_dst.set(self.tree.item(selected_item)['values'][4])
            self.port_src.set(self.tree.item(selected_item)['values'][5])
            self.port_dst.set(self.tree.item(selected_item)['values'][6])

    def apply_changes(self):
        if len(self.tree.selection()) > 0:
            selected_item = self.tree.selection()[0]
            item_chain = str(selected_item)[1:]     # Eliminamos la I de la cadena I009 -> 009
            for i in item_chain:
                if i == '0':
                    item_chain = item_chain[1:]
                else:
                    break
            print(int(item_chain,16))
            # try:
            self.list_packets[int(item_chain, 16) - 1][Ether].src = self.mac_src.get()
            self.list_packets[int(item_chain, 16) - 1][Ether].dst = self.mac_dst.get()
            self.list_packets[int(item_chain,16)-1][IP].src = self.ip_src.get()
            self.list_packets[int(item_chain, 16) - 1][IP].dst = self.ip_dst.get()
            if 'TCP' in self.list_packets[int(item_chain, 16) - 1]:
                transport_protocol = 'TCP'
            else:
                transport_protocol = 'UDP'

            print(transport_protocol, self.port_src.get())

            self.list_packets[int(item_chain, 16) - 1][transport_protocol].sport = int(self.port_src.get())
            self.list_packets[int(item_chain, 16) - 1][transport_protocol].dport = int(self.port_dst.get())

            self.tree.item(selected_item, values=(self.tree.item(selected_item)['values'][0], self.mac_src.get(), self.mac_dst.get(), self.ip_src.get(), self.ip_dst.get(), self.port_src.get(), self.port_dst.get()))

            print('Cambio Correcto')
            # except OSError as error:
            #     print("Error:", error)

            # except:
            #
            #     for i in sys.exc_info():
            #         print(i)
                # print("Unexpected error:", sys.exc_info()[2])

            # j = 1
            # for packet in self.list_packets:
            #     if 'MAC' in packet and 'IP' in packet and 'TCP' in packet or 'UDP' in packet:
            #         # self.list_packets.append(packet)
            #         if 'TCP' in packet:
            #             inf = 'TCP'
            #         else:
            #             inf = 'UDP'
            #         print(j, 'src MAC:', packet[Ether].src, 'dst MAC', packet[Ether].dst, 'src:', packet[IP].src, 'dst:',
            #               packet[IP].dst, 'sport:', packet[inf].sport, 'dport:', packet[inf].dport)
            #         # self.tree.insert('', 'end', values=(
            #         # i, packet[Ether].src, packet[Ether].dst, packet[IP].src, packet[IP].dst, packet[inf].sport,
            #         # packet[inf].dport))
            #         j += 1


    def load_packages(self):
        # Seleccionamos el fichero
        try:
            path = filedialog.askopenfile(title='Load Graph', initialdir='./Packages',
                                          filetypes=(('Files .pcap', '*.pcap'), (('All Files', '*.*'))))
            print(path.name)
            scapy_cap = rdpcap(path.name)
            i = 1
            for packet in scapy_cap:
                if 'MAC' in packet and 'IP' in packet and 'TCP' in packet or 'UDP' in packet:
                    self.list_packets.append(packet)
                    if 'TCP' in packet:
                        inf = 'TCP'
                    else:
                        inf = 'UDP'
                    print('src MAC:', packet[Ether].src, 'dst MAC', packet[Ether].dst, 'src:', packet[IP].src, 'dst:',
                          packet[IP].dst, 'sport:', packet[inf].sport, 'dport:', packet[inf].sport)
                    self.tree.insert('', 'end', values=(
                    i, packet[Ether].src, packet[Ether].dst, packet[IP].src, packet[IP].dst, packet[inf].sport,
                    packet[inf].dport))
                    i += 1

        except Exception as er:
            messagebox.showwarning(er)

    def initialize_user_interface(self):

        # Set the treeview
        self.tree = ttk.Treeview(self.root)

        self.scroll = tk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.scroll.grid(column=1, sticky='nsew')
        self.tree.configure(yscrollcommand=self.scroll.set)

        self.tree['show'] = 'headings'
        self.tree["columns"] = ("1", "2", "3", "4", "5", "6", "7")
        # Set the heading (Attribute Names)
        self.tree.heading('1', text='Num Packet')
        self.tree.heading('2', text='MAC Source')
        self.tree.heading('3', text='MAC Destination')
        self.tree.heading('4', text='IP Source')
        self.tree.heading('5', text='IP Destination')
        self.tree.heading('6', text='Port Source')
        self.tree.heading('7', text='Port Destination')
        # Specify attributes of the columns (We want to stretch it!)
        self.tree.column('1', minwidth=120, width=120, stretch=False)
        self.tree.column('2', minwidth=120, width=120, stretch=False)
        self.tree.column('3', minwidth=120, width=120, stretch=False)
        self.tree.column('4', minwidth=120, width=120, stretch=False)
        self.tree.column('5', minwidth=120, width=120, stretch=False)
        self.tree.column('6', minwidth=120, width=120, stretch=False)
        self.tree.column('7', minwidth=120, width=120, stretch=False)
        self.tree.grid(row=0)
        # self.treeview = self.tree

        tk.Label(self.root, text=' ').grid(row=1)

        campos = tk.LabelFrame(self.root, text="Parameters to change of the selected package")
        campos.grid(row=2)

        tk.Label(campos, text=' ').grid(row=0, column=0)
        tk.Label(campos, text="       MAC src:  ").grid(row=1, column=0)
        tk.Label(campos, text="       MAC dst:  ").grid(row=2, column=0)
        tk.Label(campos, text="       IP src:  ").grid(row=1, column=2)
        tk.Label(campos, text="       IP dst:  ").grid(row=2, column=2)
        tk.Label(campos, text="       Port src:  ").grid(row=1, column=4)
        tk.Label(campos, text="       Port dst:  ").grid(row=2, column=4)

        tk.Entry(campos, textvariable=self.mac_src, width=18).grid(row=1, column=1, sticky='w')
        tk.Entry(campos, textvariable=self.mac_dst, width=18).grid(row=2, column=1, sticky='w')
        tk.Entry(campos, textvariable=self.ip_src, width=16).grid(row=1, column=3, sticky='w')
        tk.Entry(campos, textvariable=self.ip_dst, width=16).grid(row=2, column=3, sticky='w')
        tk.Entry(campos, textvariable=self.port_src, width=10).grid(row=1, column=5, sticky='w')
        tk.Entry(campos, textvariable=self.port_dst, width=10).grid(row=2, column=5, sticky='w')

        tk.Label(campos, text='     ').grid(row=3, column=6)

        tk.Button(campos, text="Load values", command=self.load_values).grid(row=4, column=7)
        tk.Button(campos, text="Apply changes", command=self.apply_changes).grid(row=4, column=8)
        tk.Label(campos, text=' ').grid(row=2, column=0)

        tk.Label(self.root, text=' ').grid(row=3)

        botones = tk.LabelFrame(self.root, height=1000)
        botones.grid(row=4, sticky='N')

        tk.Button(botones, text="Delete Selected Packet", command=self.delete).grid(row=0, column=0)
        #tk.Label(botones, text='       ').grid(row=0, column=1)
        tk.Button(botones, text="Load Packages from...", command=self.load_packages).grid(row=0, column=2)
        # for i in range(0, 100):
        #     self.treeview.insert('', 'end', text=i, values=('hola1', 'hola2', 'hola3', 'hola4', 'hola5', 'hola6'))

        # if len(self.tree.selection()) > 0:
        #     mac_src = self.tree.item(self.tree.selection()[0])['values'][1]
        #     print(mac_src)

    def insert_data(self):
        self.tree.insert('', 'end', values=('hola', 'hola'))


app = PackageImportWindow(tk.Tk())
app.root.resizable(False, False)
app.root.mainloop()
