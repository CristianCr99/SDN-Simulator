import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox

from scapy.layers.inet import *
from scapy.layers.l2 import Ether
from scapy.utils import rdpcap

from Utilities import Utilities


class PacketImportWindow(tk.Frame):
    def __init__(self, root, master, host, graph, **kw):
        super().__init__(master, **kw)
        self.port_dst = tk.StringVar()
        self.port_src = tk.StringVar()
        self.ip_dst = tk.StringVar()
        self.ip_src = tk.StringVar()
        self.mac_dst = tk.StringVar()
        self.mac_src = tk.StringVar()
        self.protocol = tk.StringVar()
        self.protocol.set('TCP')
        self.number_packets = tk.IntVar()
        self.host_src = tk.StringVar()
        self.host_dst = tk.StringVar()
        self.root = root
        self.host = host
        self.list_packets = []
        self.master = master
        self.index = 1
        self.graph = graph
        self.showProtocolsOption = None
        self.time_spawn = tk.StringVar()
        self.time_spawn.set('0.0')
        self.initialize_user_interface()

    def get_list_packets(self):
        return self.list_packets

    def edit(self, mac_src, mac_dst, ip_src, ip_dst, sport, dport, protocol, time_spawn):
        selected_item = self.tree.selection()[0]
        self.tree.item(selected_item, values=(mac_src, mac_dst, ip_src, ip_dst, sport, dport, protocol, time_spawn))

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
                if ('MAC' in packet[0] or 'Ethernet' in packet[0]) and 'IP' in packet[0] and (
                        'TCP' in packet[0] or 'UDP' in packet[0]):
                    if 'TCP' in packet[0]:
                        protocol = 'TCP'
                    else:
                        protocol = 'UDP'
                    # Reinsertamos los paquetes actualizados
                    self.tree.insert('', 'end', iid=i, values=(
                        i, packet[0][Ether].src, packet[0][Ether].dst, packet[0][IP].src, packet[0][IP].dst,
                        packet[0][protocol].sport,
                        packet[0][protocol].dport, protocol, packet[1]))
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
            self.time_spawn.set(self.tree.item(selected_item)['values'][8])
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
            # print(len(self.list_packets))
            self.list_packets[selected_item - 1][0][Ether].src = self.mac_src.get()
            self.list_packets[selected_item - 1][0][Ether].dst = self.mac_dst.get()
            self.list_packets[selected_item - 1][0][IP].src = self.ip_src.get()
            self.list_packets[selected_item - 1][0][IP].dst = self.ip_dst.get()
            if 'TCP' in self.list_packets[selected_item - 1][0]:
                transport_protocol = 'TCP'
            else:
                transport_protocol = 'UDP'

            # print(transport_protocol, self.port_src.get())

            self.list_packets[selected_item - 1][0][transport_protocol].sport = int(self.port_src.get())
            self.list_packets[selected_item - 1][0][transport_protocol].dport = int(self.port_dst.get())

            self.tree.item(selected_item, values=(
                self.tree.item(selected_item)['values'][0], self.mac_src.get(), self.mac_dst.get(), self.ip_src.get(),
                self.ip_dst.get(), self.port_src.get(), self.port_dst.get(), self.protocol.get(),
                float(self.time_spawn.get())))

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

    def load_packets(self):
        # Seleccionamos el fichero
        try:
            path = filedialog.askopenfile(title='Load Graph', initialdir='./Packets',
                                          filetypes=(('Files .pcap', '*.pcap'), (('All Files', '*.*'))))
            # print(path.name)
            scapy_cap = rdpcap(path.name)

            for packet in scapy_cap:
                if ('MAC' in packet or 'Ethernet' in packet) and 'IP' in packet and (
                        'TCP' in packet or 'UDP' in packet):
                    packet[Ether].src = self.mac_src.get()
                    packet[Ether].dst = self.mac_dst.get()
                    packet[IP].src = self.ip_src.get()
                    packet[IP].dst = self.ip_dst.get()
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
        utilities = Utilities()
        if self.number_packets.get() > 0 and float(self.time_spawn.get()) >= 0.0:
            if utilities.port_check(self.port_src.get()) and utilities.port_check(self.port_dst.get()):
                for i in range(1, self.number_packets.get() + 1):

                    if self.protocol.get() == 'TCP':
                        p = Ether(src=self.mac_src.get(), dst=self.mac_dst.get()) / IP(src=self.ip_src.get(),
                                                                                       dst=self.ip_dst.get()) / TCP(
                            sport=int(self.port_src.get()), dport=int(self.port_dst.get()))
                    else:
                        p = Ether(src=self.mac_src.get(), dst=self.mac_dst.get()) / IP(src=self.ip_src.get(),
                                                                                       dst=self.ip_dst.get()) / UDP(
                            sport=int(self.port_src.get()), dport=int(self.port_dst.get()))

                    self.list_packets.append((p, float(self.time_spawn.get())))
                    self.tree.insert('', 'end', iid=self.index, values=(
                        self.index, p[Ether].src, p[Ether].dst, p[IP].src, p[IP].dst,
                        p[self.protocol.get()].sport,
                        p[self.protocol.get()].dport, self.protocol.get(), float(self.time_spawn.get())))
                    self.index += 1
            else:
                message = ''
                # TODO esto no va bien :)
                if utilities.port_check(self.port_src.get()):
                    message += self.port_src.get()
                if utilities.port_check(self.port_dst.get()):
                    message += self.port_dst.get()

                message_final = 'Error, (' + message + ') values are not valid. \n\no   Port must be a value between 1 and 65535.'
                messagebox.showerror("Error", message_final)
        else:
            messagebox.showerror("Error", 'The number of packets to insert must be greater than 0 and the packet spawn time must be greater than 0.')

    def update_values_hosts(self, event):
        # print(self.showHostsOption)
        self.mac_dst.set(self.graph.get_graph().nodes[self.showHosts.get()]['mac'])
        self.ip_dst.set(self.graph.get_graph().nodes[self.showHosts.get()]['ip'])

    def update_values_protocols(self, event):
        self.protocol.set(self.showProtocols.get())

    def initialize_user_interface(self):
        # Set the treeview
        self.tree = ttk.Treeview(self.root)

        self.scroll = tk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.scroll.grid(column=1, sticky='nsew')
        self.tree.configure(yscrollcommand=self.scroll.set)

        self.tree['show'] = 'headings'
        self.tree["columns"] = ("1", "2", "3", "4", "5", "6", "7", '8', '9')
        # Set the heading (Attribute Names)
        self.tree.heading('1', text='Packet')
        self.tree.heading('2', text='Source MAC')
        self.tree.heading('3', text='Destination MAC')
        self.tree.heading('4', text='Source IP')
        self.tree.heading('5', text='Destination IP')
        self.tree.heading('6', text='Source Port')
        self.tree.heading('7', text='Destination Port')
        self.tree.heading('8', text='Transport Protocol')
        self.tree.heading('9', text='Spawn Time')
        # Specify attributes of the columns (We want to stretch it!)
        self.tree.column('1', minwidth=120, width=145, stretch=False)
        self.tree.column('2', minwidth=120, width=145, stretch=False)
        self.tree.column('3', minwidth=120, width=145, stretch=False)
        self.tree.column('4', minwidth=120, width=145, stretch=False)
        self.tree.column('5', minwidth=120, width=145, stretch=False)
        self.tree.column('6', minwidth=120, width=145, stretch=False)
        self.tree.column('7', minwidth=120, width=145, stretch=False)
        self.tree.column('8', minwidth=120, width=145, stretch=False)
        self.tree.column('9', minwidth=120, width=145, stretch=False)
        self.tree.grid(row=0)
        # self.treeview = self.tree

        # tk.Label(self.root, text=' ').grid(row=1)

        campos = tk.LabelFrame(self.root, text="Packet Parameters")
        campos.grid(row=2, padx=5, pady=15)

        tk.Label(campos, text=' ').grid(row=0, column=0)
        tk.Label(campos, text="Src Host:").grid(row=1, column=0, sticky='w', padx=20, pady=5)
        tk.Label(campos, text="Dst Host:").grid(row=2, column=0, sticky='w', padx=20, pady=5)
        tk.Label(campos, text="Src MAC:").grid(row=1, column=2, sticky='w', padx=20, pady=5)
        tk.Label(campos, text="Dst MAC:").grid(row=2, column=2, sticky='w', padx=20, pady=5)
        tk.Label(campos, text="Src IP:").grid(row=1, column=4, sticky='w', padx=20, pady=5)
        tk.Label(campos, text="Dst IP:").grid(row=2, column=4, sticky='w', padx=20, pady=5)
        tk.Label(campos, text="Src Port:").grid(row=1, column=6, sticky='w', padx=20, pady=5)
        tk.Label(campos, text="Dst Port:").grid(row=2, column=6, sticky='w', padx=20, pady=5)
        tk.Label(campos, text="Pransport protocol:").grid(row=1, column=8, sticky='w', padx=20, pady=5)
        tk.Label(campos, text="No. of packets to add:").grid(row=2, column=8, sticky='w', padx=20, pady=5)

        self.host_src.set(self.host)
        tk.Entry(campos, textvariable=self.host_src, width=10, state='disabled').grid(row=1, column=1, sticky='w')
        tk.Entry(campos, textvariable=self.mac_src, width=16, state='disabled').grid(row=1, column=3, sticky='w')
        tk.Entry(campos, textvariable=self.mac_dst, width=16, state='disabled').grid(row=2, column=3, sticky='w')
        tk.Entry(campos, textvariable=self.ip_src, width=14, state='disabled').grid(row=1, column=5, sticky='w')
        tk.Entry(campos, textvariable=self.ip_dst, width=14, state='disabled').grid(row=2, column=5, sticky='w')

        list_ip = []
        for i in list(self.graph.get_graph().nodes):
            if i[0] == 'h' and i != self.host:
                list_ip.append(i)

        self.showHosts = tk.StringVar(campos)
        self.showHosts.set(list_ip[0])
        self.update_values_hosts('')
        # print('value:',self.showHosts.get())
        self.showHostsOption = tk.OptionMenu(campos, self.showHosts, *list_ip, command=self.update_values_hosts)
        self.showHostsOption.grid(row=2, column=1, sticky='W')
        # must be -column, -columnspan, -in, -ipadx, -ipady, -padx, -pady, -row, -rowspan, or -sticky

        tk.Entry(campos, textvariable=self.port_src, width=7).grid(row=1, column=7, sticky='w')
        tk.Entry(campos, textvariable=self.port_dst, width=7).grid(row=2, column=7, sticky='w')
        # tk.Entry(campos, textvariable=self.protocol, width=10).grid(row=1, column=9, sticky='w')
        self.showProtocols = tk.StringVar(campos)
        self.showProtocols.set('TCP')
        list_protocols = ['TCP', 'UDP']
        self.showProtocolsOption = tk.OptionMenu(campos, self.showProtocols, *list_protocols,
                                                 command=self.update_values_protocols)
        self.showProtocolsOption.grid(row=1, column=9, sticky='W')

        tk.Entry(campos, textvariable=self.number_packets, width=10).grid(row=2, column=9, sticky='w')

        tk.Label(campos, text='     ').grid(row=3, column=13)
        tk.Label(campos, text='     ').grid(row=1, column=13)
        tk.Label(campos, text='     ').grid(row=2, column=13)
        tk.Label(campos, text='     ').grid(row=3, column=13)

        tk.Label(campos, text="       Time Spawn:  ").grid(row=1, column=11, sticky='w')
        tk.Entry(campos, textvariable=self.time_spawn, width=7).grid(row=1, column=12, sticky='w')

        tk.Button(campos, text="Load values", command=self.load_values, height=1, width=15).grid(row=1, column=14,
                                                                                                 sticky='E', padx=5,
                                                                                                 pady=5)
        tk.Button(campos, text="Apply changes", command=self.apply_changes, height=1, width=15).grid(row=2, column=14,
                                                                                                     sticky='E', padx=5,
                                                                                                     pady=5)
        tk.Button(campos, text="Add as new packet", command=self.add_packets, height=1, width=15).grid(row=3,
                                                                                                        column=14,
                                                                                                        sticky='E',
                                                                                                        padx=5, pady=5)
        # tk.Label(campos, text=' ').grid(row=2, column=0)

        # tk.Label(self.root, text=' ').grid(row=3, column=0)

        buttonFrame = tk.Frame(self.root, bd=3)
        buttonFrame.grid(row=4, column=0, sticky='N')

        # botones = tk.LabelFrame(self.root, height=1000)
        # botones.grid(row=4, sticky='N')

        tk.Button(buttonFrame, text="Delete Selected Packet", command=self.delete).grid(row=0, column=0, padx=0, pady=0)
        # tk.Label(botones, text=' ').grid(row=0, column=1)
        tk.Button(buttonFrame, text="Load Packets from...", command=self.load_packets).grid(row=0, column=1, padx=20, pady=0)
        # tk.Label(botones, text=' ').grid(row=0, column=3)
        tk.Button(buttonFrame, text="Save Packets", command=self.return_list_packets).grid(row=0, column=2, padx=0, pady=0)

        # if len(self.tree.selection()) > 0:
        #     mac_src = self.tree.item(self.tree.selection()[0])['values'][1]
        #     print(mac_src)
        # print(len(self.master.info_window_import) > 0 and len(self.master.info_window_import[self.host]) > 0)

        self.ip_src.set(self.graph.get_graph().nodes[self.host]['ip'])
        self.mac_src.set(self.graph.get_graph().nodes[self.host]['mac'])

        if len(self.master.info_window_import) > 0 and self.host in self.master.info_window_import and len(
                self.master.info_window_import[self.host]) > 0:
            # self.list_packets = self.master.info_window_import[self.host]
            # print(len(self.list_packets))
            # list = self.master.info_window_import[self.host]
            # for i in range(1,len(self.master.info_window_import[self.host])):
            #     self.master.info_window_import[self.host][i].show()
            # print(list)
            # print(self.list_packets)
            # print('longitusd:', len(self.master.info_window_import[self.host]))
            for i in range(0, len(self.master.info_window_import[self.host])):
                packet, time_spawn = self.master.info_window_import[self.host][i]
                packet.show()
                # print('MAC' in packet, 'Ethernet' in packet, 'IP' in packet, 'TCP' in packet, 'UDP' in packet)
                if ('MAC' in packet or 'Ethernet' in packet) and 'IP' in packet and (
                        'TCP' in packet or 'UDP' in packet):
                    if 'TCP' in packet:
                        protocol = 'TCP'
                    else:
                        protocol = 'UDP'
                    self.list_packets.append((packet, time_spawn))
                    self.tree.insert('', 'end', iid=self.index, values=(
                        self.index, packet[Ether].src, packet[Ether].dst, packet[IP].src, packet[IP].dst,
                        packet[protocol].sport,
                        packet[protocol].dport, protocol, time_spawn))
                    self.index += 1

    def return_list_packets(self):
        # TODO Estas dos líneas de abajo pueden ser muy útiles
        # self.root.deiconify()
        # self.root.wait_window()
        # print('HELLO')
        self.master.info_window_import[self.host] = self.list_packets
        self.root.destroy()
        # print(self.list_packets)
        # return self.list_packets

# if __name__ == '__main__':
#     app = PacketImportWindow(tk.Tk())
#     app.root.resizable(False, False)
#     app.root.mainloop()
