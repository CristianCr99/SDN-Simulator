import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox

from scapy.layers.inet import *
from scapy.layers.l2 import Ether
from scapy.utils import rdpcap


class PackageImportWindow(tk.Frame):
    def __init__(self, root, master, host, **kw):
        super().__init__(master, **kw)
        self.port_dst = tk.StringVar()
        self.port_src = tk.StringVar()
        self.ip_dst = tk.StringVar()
        self.ip_src = tk.StringVar()
        self.mac_dst = tk.StringVar()
        self.mac_src = tk.StringVar()
        self.protocol = tk.StringVar()
        self.number_packets = tk.IntVar()
        self.root = root
        self.host = host
        self.list_packets = []
        self.master = master
        self.index = 1
        self.initialize_user_interface()

    def get_list_packets(self):
        return self.list_packets

    def edit(self, mac_src, mac_dst, ip_src, ip_dst, sport, dport, protocol):
        selected_item = self.tree.selection()[0]
        self.tree.item(selected_item, values=(mac_src, mac_dst, ip_src, ip_dst, sport, dport, protocol))

    def delete(self):
        if len(self.tree.selection()) > 0:
            indexes_to_delete = []
            # print('IDs de las tuplas que se van a eliminar: ', self.tree.selection())
            for selected_packet in self.tree.selection():
                indexes_to_delete.append(int(selected_packet, 10) - 1)  # Guardamos el valor del índice en entero
            indexes_to_delete = sorted(indexes_to_delete,
                                       reverse=True)  # Ordenamos los índices de mayor a menor antes de borrar
            # print('Índices que se van a borrar de la lista : ', indexes_to_delete)
            for index in indexes_to_delete:
                self.list_packets.pop(index)  # Borramos de la lista local los paquetes indicados
                self.index -= 1

            for child in self.tree.get_children():
                self.tree.delete(child)  # Vaciamos el árbol

            i = 1
            for packet in self.list_packets:
                if ('MAC' in packet or 'Ethernet' in packet) and 'IP' in packet and ('TCP' in packet or 'UDP' in packet):
                    if 'TCP' in packet:
                        protocol = 'TCP'
                    else:
                        protocol = 'UDP'
                    # Reinsertamos los paquetes actualizados
                    self.tree.insert('', 'end', iid=i, values=(
                        i, packet[Ether].src, packet[Ether].dst, packet[IP].src, packet[IP].dst,
                        packet[protocol].sport,
                        packet[protocol].dport, protocol))
                    i += 1


    def load_values(self):
        # print('hola')
        if len(self.tree.selection()) > 0:
            # print('holaas')
            selected_item = self.tree.selection()[0]
            # print(self.tree.item(selected_item)['values'][1])
            self.mac_src.set(self.tree.item(selected_item)['values'][1])
            self.mac_dst.set(self.tree.item(selected_item)['values'][2])
            self.ip_src.set(self.tree.item(selected_item)['values'][3])
            self.ip_dst.set(self.tree.item(selected_item)['values'][4])
            self.port_src.set(self.tree.item(selected_item)['values'][5])
            self.port_dst.set(self.tree.item(selected_item)['values'][6])
            self.protocol.set(self.tree.item(selected_item)['values'][7])
            #

    def apply_changes(self):
        if len(self.tree.selection()) > 0:
            selected_item = int(self.tree.selection()[0])
            # item_chain = str(selected_item)[1:]  # Eliminamos la I de la cadena I009 -> 009
            # for i in item_chain:
            #     if i == '0':
            #         item_chain = item_chain[1:]
            #     else:
            #         break
            # item_chain = int(selected_item)
            # print(item_chain)
            # try:
            self.list_packets[selected_item][Ether].src = self.mac_src.get()
            self.list_packets[selected_item][Ether].dst = self.mac_dst.get()
            self.list_packets[selected_item][IP].src = self.ip_src.get()
            self.list_packets[selected_item][IP].dst = self.ip_dst.get()
            if 'TCP' in self.list_packets[selected_item]:
                transport_protocol = 'TCP'
            else:
                transport_protocol = 'UDP'

            # print(transport_protocol, self.port_src.get())

            self.list_packets[selected_item][transport_protocol].sport = int(self.port_src.get())
            self.list_packets[selected_item][transport_protocol].dport = int(self.port_dst.get())

            self.tree.item(selected_item, values=(
                self.tree.item(selected_item)['values'][0], self.mac_src.get(), self.mac_dst.get(), self.ip_src.get(),
                self.ip_dst.get(), self.port_src.get(), self.port_dst.get(), self.protocol.get()))

            # print('Cambio Correcto')
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
            # print(path.name)
            scapy_cap = rdpcap(path.name)

            for packet in scapy_cap:
                if ('MAC' in packet or 'Ethernet' in packet) and 'IP' in packet and ('TCP' in packet or 'UDP' in packet):
                    self.list_packets.append(packet)
                    packet.show()
                    if 'TCP' in packet:
                        protocol = 'TCP'
                    else:
                        protocol = 'UDP'
                    # print('src MAC:', packet[Ether].src, 'dst MAC', packet[Ether].dst, 'src:', packet[IP].src, 'dst:',
                    #      packet[IP].dst, 'sport:', packet[protocol].sport, 'dport:', packet[protocol].sport, 'protocol:', protocol)
                    self.tree.insert('', 'end', iid=self.index, values=(
                        self.index, packet[Ether].src, packet[Ether].dst, packet[IP].src, packet[IP].dst,
                        packet[protocol].sport,
                        packet[protocol].dport, protocol))
                    self.index += 1

        except Exception as er:
            messagebox.showwarning(er)

    def add_packets(self):
        if self.number_packets.get() > 0:
            for i in range(1, self.number_packets.get() + 1):

                if self.protocol.get() == 'TCP':
                    p = Ether(src=self.mac_src.get(), dst=self.mac_dst.get()) / IP(src=self.ip_src.get(),
                                                                                   dst=self.ip_dst.get()) / TCP(
                        sport=int(self.port_src.get()), dport=int(self.port_dst.get()))
                else:
                    p = Ether(src=self.mac_src.get(), dst=self.mac_dst.get()) / IP(src=self.ip_src.get(),
                                                                                   dst=self.ip_dst.get()) / UDP(
                        sport=int(self.port_src.get()), dport=int(self.port_dst.get()))
                self.list_packets.append(p)
                self.tree.insert('', 'end', iid=self.index, values=(
                    self.index, p[Ether].src, p[Ether].dst, p[IP].src, p[IP].dst,
                    p[self.protocol.get()].sport,
                    p[self.protocol.get()].dport, self.protocol.get()))
                self.index += 1

    def initialize_user_interface(self):
        # Set the treeview
        self.tree = ttk.Treeview(self.root)

        self.scroll = tk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.scroll.grid(column=1, sticky='nsew')
        self.tree.configure(yscrollcommand=self.scroll.set)

        self.tree['show'] = 'headings'
        self.tree["columns"] = ("1", "2", "3", "4", "5", "6", "7", '8')
        # Set the heading (Attribute Names)
        self.tree.heading('1', text='Num Packet')
        self.tree.heading('2', text='MAC Source')
        self.tree.heading('3', text='MAC Destination')
        self.tree.heading('4', text='IP Source')
        self.tree.heading('5', text='IP Destination')
        self.tree.heading('6', text='Port Source')
        self.tree.heading('7', text='Port Destination')
        self.tree.heading('8', text='Transport Protocol')
        # Specify attributes of the columns (We want to stretch it!)
        self.tree.column('1', minwidth=120, width=120, stretch=False)
        self.tree.column('2', minwidth=120, width=120, stretch=False)
        self.tree.column('3', minwidth=120, width=120, stretch=False)
        self.tree.column('4', minwidth=120, width=120, stretch=False)
        self.tree.column('5', minwidth=120, width=120, stretch=False)
        self.tree.column('6', minwidth=120, width=120, stretch=False)
        self.tree.column('7', minwidth=120, width=120, stretch=False)
        self.tree.column('8', minwidth=120, width=120, stretch=False)
        self.tree.grid(row=0)
        # self.treeview = self.tree

        tk.Label(self.root, text=' ').grid(row=1)

        campos = tk.LabelFrame(self.root, text="Parameters to change of the selected package")
        campos.grid(row=2)

        tk.Label(campos, text=' ').grid(row=0, column=0)
        tk.Label(campos, text="       MAC src:  ").grid(row=1, column=0, sticky='w')
        tk.Label(campos, text="       MAC dst:  ").grid(row=2, column=0, sticky='w')
        tk.Label(campos, text="       IP src:  ").grid(row=1, column=2, sticky='w')
        tk.Label(campos, text="       IP dst:  ").grid(row=2, column=2, sticky='w')
        tk.Label(campos, text="       Port src:  ").grid(row=1, column=4, sticky='w')
        tk.Label(campos, text="       Port dst:  ").grid(row=2, column=4, sticky='w')
        tk.Label(campos, text="       Pransport protocol:  ").grid(row=1, column=6, sticky='w')
        tk.Label(campos, text="       Nº of packages to add:  ").grid(row=2, column=6, sticky='w')

        tk.Entry(campos, textvariable=self.mac_src, width=18).grid(row=1, column=1, sticky='w')
        tk.Entry(campos, textvariable=self.mac_dst, width=18).grid(row=2, column=1, sticky='w')
        tk.Entry(campos, textvariable=self.ip_src, width=16).grid(row=1, column=3, sticky='w')
        tk.Entry(campos, textvariable=self.ip_dst, width=16).grid(row=2, column=3, sticky='w')
        tk.Entry(campos, textvariable=self.port_src, width=10).grid(row=1, column=5, sticky='w')
        tk.Entry(campos, textvariable=self.port_dst, width=10).grid(row=2, column=5, sticky='w')
        tk.Entry(campos, textvariable=self.protocol, width=10).grid(row=1, column=7, sticky='w')
        tk.Entry(campos, textvariable=self.number_packets, width=10).grid(row=2, column=7, sticky='w')

        tk.Label(campos, text='     ').grid(row=3, column=6)
        tk.Label(campos, text='     ').grid(row=1, column=8)
        tk.Label(campos, text='     ').grid(row=2, column=8)
        tk.Label(campos, text='     ').grid(row=3, column=8)

        tk.Button(campos, text=" Load values ", command=self.load_values, height=1, width=15).grid(row=1, column=9,
                                                                                                   sticky='E')
        tk.Button(campos, text="Apply changes", command=self.apply_changes, height=1, width=15).grid(row=2, column=9,
                                                                                                     sticky='E')
        tk.Button(campos, text="Add as new package", command=self.add_packets, height=1, width=15).grid(row=3, column=9,
                                                                                                        sticky='E')
        tk.Label(campos, text=' ').grid(row=2, column=0)

        tk.Label(self.root, text=' ').grid(row=3)

        botones = tk.LabelFrame(self.root, height=1000)
        botones.grid(row=4, sticky='N')

        tk.Button(botones, text="Delete Selected Packet", command=self.delete).grid(row=0, column=0)
        tk.Label(botones, text=' ').grid(row=0, column=1)
        tk.Button(botones, text="Load Packages from...", command=self.load_packages).grid(row=0, column=2)
        tk.Label(botones, text=' ').grid(row=0, column=3)
        tk.Button(botones, text="Save Packets", command=self.return_list_packets).grid(row=0, column=4)

        # if len(self.tree.selection()) > 0:
        #     mac_src = self.tree.item(self.tree.selection()[0])['values'][1]
        #     print(mac_src)
        # print(len(self.master.info_window_import) > 0 and len(self.master.info_window_import[self.host]) > 0)
        if len(self.master.info_window_import) > 0 and len(self.master.info_window_import[self.host]) > 0:
            # self.list_packets = self.master.info_window_import[self.host]
            # print(len(self.list_packets))
            # list = self.master.info_window_import[self.host]
            # for i in range(1,len(self.master.info_window_import[self.host])):
            #     self.master.info_window_import[self.host][i].show()
            # print(list)
            print(self.list_packets)
            for i in range(1, len(self.master.info_window_import[self.host])):
                packet = self.master.info_window_import[self.host][i]
                packet.show()
                print('MAC' in packet, 'Ethernet' in packet, 'IP' in packet, 'TCP' in packet, 'UDP' in packet)
                if ('MAC' in packet or 'Ethernet' in packet) and 'IP' in packet and ('TCP' in packet or 'UDP' in packet):
                    if 'TCP' in packet:
                        protocol = 'TCP'
                    else:
                        protocol = 'UDP'
                    self.list_packets.append(packet)
                    self.tree.insert('', 'end', iid=self.index, values=(
                        self.index, packet[Ether].src, packet[Ether].dst, packet[IP].src, packet[IP].dst,
                        packet[protocol].sport,
                        packet[protocol].dport, protocol))
                    self.index += 1

    def return_list_packets(self):
        # TODO Estas dos líneas de abajo pueden ser muy útiles
        # self.root.deiconify()
        # self.root.wait_window()
        print('HELLO')
        self.master.info_window_import[self.host] = self.list_packets
        self.root.destroy()
        # print(self.list_packets)
        # return self.list_packets

# if __name__ == '__main__':
#     app = PackageImportWindow(tk.Tk())
#     app.root.resizable(False, False)
#     app.root.mainloop()
