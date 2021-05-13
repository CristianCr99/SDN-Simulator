class DiscreteEvents:

    def __init__(self, initial_event_list=None, initial_packets_list=None, initial_openflow_list=None):
        self.list_events = initial_event_list
        self.list_packets = initial_packets_list
        self.list_packets_openflow = initial_openflow_list

    def get_list_events(self):
        return self.list_events

    def get_list_packets(self):
        return self.list_packets

    def get_list_packets_openflow(self):
        return self.list_packets_openflow

    def queue_list_events(self, x):
        self.list_events.append(x)  # encolamos al final de la lista

    def unqueue_list_events(self):
        """ Elimina el primer elemento de la cola y devuelve su
            valor. Si la cola está vacía, levanta ValueError. """
        try:
            return self.list_events.pop(0)
        except:
            return 0

    def is_empty_list_events(self):
        """ Devuelve True si la cola esta vacía, False si no."""
        return self.list_events == []

    def inser_event(self, new_event):
        j = 0
        for event in self.list_events:
            if event['time_spawn'] > new_event['time_spawn']:
                self.list_events = self.list_events[:j] + [new_event] + self.list_events[j:]
                return
            j += 1
        self.list_events.append(new_event)
