
class flow_information():

    def __init__(self, packet):

        self.packet = packet
        self.packet_delay_list = []

    def get_packet(self):
        return self.packet

    def get_packet_delay_list(self):
        return self.packet_delay_list


    def set_packet(self, packet):
        self.packet = packet

    def set_packet_delay_list(self, packet_delay_list):
        self.packet_delay_list = packet_delay_list

    def add_delay(self, delay, time_generation):
        j = 0
        for i in self.packet_delay_list:
            if time_generation < i[1]:
                self.packet_delay_list = self.packet_delay_list[:j] + [(delay, time_generation)] + self.packet_delay_list[j:]
                return

            j += 1
        self.packet_delay_list.append((delay, time_generation))

    # # for event in self.list_events:
    #     if event['time_spawn'] > new_event['time_spawn']:
    #         self.list_events = self.list_events[:j] + [new_event] + self.list_events[j:]
    #         print(new_event)
    #         return
    #     j += 1
    # print(new_event)
    # self.list_events.append(new_event)
    #
    # def inser_event(self, new_event):
    #     j = 0
    #
    #     for event in self.list_events:
    #         if event['time_spawn'] > new_event['time_spawn']:
    #             self.list_events = self.list_events[:j] + [new_event] + self.list_events[j:]
    #             print(new_event)
    #             return
    #         j += 1
    #     print(new_event)
    #     self.list_events.append(new_event)

