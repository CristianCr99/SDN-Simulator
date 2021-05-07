import tkinter as tk
import tkinter.ttk as ttk


class InfoSwitchWindow(tk.Frame):
    def __init__(self, root, switch_data, name):
    #def __init__(self, root):
        self.root = root
        self.switch_data = switch_data
        self.name = name

    def initialize_user_interface(self):

        campos = tk.LabelFrame(self.root, text=' Parameters of Switch ' + self.name + ' ')
        campos.grid(row=0, column=0)

        # tk.Label(campos, text=' ').grid(row=0, column=0)
        tk.Label(campos, text="       MAC Address:  ").grid(row=1, column=0, sticky='w')
        tk.Label(campos, text="       IP Address:  ").grid(row=1, column=2, sticky='w')
        tk.Label(campos, text="       Port:  ").grid(row=1, column=4, sticky='w')
        if 'mac' in self.switch_data:
            tk.Label(campos, text=self.switch_data['mac']).grid(row=1, column=1, sticky='w')
        if 'ip' in self.switch_data:
            tk.Label(campos, text=self.switch_data['ip']).grid(row=1, column=3, sticky='w')
        if 'port' in self.switch_data:
            tk.Label(campos, text=self.switch_data['port']).grid(row=1, column=5, sticky='w')

        # tk.Label(campos, text='     ').grid(row=2, column=0)
        # tk.Label(campos, text='     ').grid(row=4, column=0)

        self.tree = ttk.Treeview(self.root)

        self.scroll = tk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.scroll.grid(column=1, sticky='nsew')
        self.tree.configure(yscrollcommand=self.scroll.set)

        self.tree['show'] = 'headings'
        self.tree["columns"] = ("1", "2", "3", "4", "5", "6", "7", '8', '9', '10', '11')
        # Set the heading (Attribute Names)
        self.tree.heading('1', text='Nº Flow Entry')
        self.tree.heading('2', text='Src MAC')
        self.tree.heading('3', text='Dst MAC')
        self.tree.heading('4', text='Src IP')
        self.tree.heading('5', text='Dst IP')
        self.tree.heading('6', text='Src Port')
        self.tree.heading('7', text='Dst Port')
        self.tree.heading('8', text='Transp. Protocol')
        self.tree.heading('9', text='Nº of Packets')
        self.tree.heading('10', text='Nº of Bytes')
        self.tree.heading('11', text='Action')
        # Specify attributes of the columns (We want to stretch it!)
        self.tree.column('1', minwidth=80, width=80, stretch=False)
        self.tree.column('2', minwidth=120, width=120, stretch=False)
        self.tree.column('3', minwidth=120, width=120, stretch=False)
        self.tree.column('4', minwidth=80, width=80, stretch=False)
        self.tree.column('5', minwidth=80, width=80, stretch=False)
        self.tree.column('6', minwidth=60, width=60, stretch=False)
        self.tree.column('7', minwidth=60, width=60, stretch=False)
        self.tree.column('8', minwidth=100, width=100, stretch=False)
        self.tree.column('9', minwidth=90, width=90, stretch=False)
        self.tree.column('10', minwidth=90, width=90, stretch=False)
        self.tree.column('11', minwidth=70, width=70, stretch=False)
        self.tree.grid(row=1, column=0)

        i = 1
        #self.G.nodes[node]['flow_table']
        # print(self.switch_data.nodes[self.name]['flow_table']['mac_src'])
        for flow_entry in (self.switch_data['flow_table']):
            self.tree.insert('', 'end', iid=i, values=(
                i, flow_entry.get_mac_src(), flow_entry.get_mac_dst(),flow_entry.get_ip_src(),flow_entry.get_ip_dst(),flow_entry.get_port_src(),flow_entry.get_port_dst(),flow_entry.get_transport_protocol(),flow_entry.get_counter_packet_number(),flow_entry.get_counter_packet_byte(), flow_entry.get_action()))
            i += 1


# app = PackageImportWindow(tk.Tk())
# app.root.resizable(False, False)
# app.root.mainloop()
