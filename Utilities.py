from os import path
from pathlib import Path

from scapy.layers.inet import *


class Utilities:

    def mac_address_check(self, mac_address):
        try:
            if re.match("[0-9a-f]{2}([:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac_address.lower()):
                return True
            return False
        except:
            return False

    def ip_address_check(self, ip_address):
        try:
            if len(ip_address.split('.')) == 4:
                for i in ip_address.split('.'):
                    if not int(i) >= 0:
                        return False
                return True
            return False
        except:
            return False

    def port_check(self, port):
        try:
            port_number = int(port)
            if 1 <= port_number <= 65535:
                return True
            return False
        except:
            return False

    def is_number_positive(self, number):
        try:
            number = int(number)
            if number > 0:
                return True
            return False
        except:
            return False

    # https: // es.stackoverflow.com / questions / 281848 / calcular - el - jitter - en - kotlin
    def calculate_jitter(self, list_delays):
        if len(list_delays) < 2:
            return 0.0
        sum = 0.0
        for i in range(0, len(list_delays)):
            # if i > 0:
            sum += abs(list_delays[i - 1] - list_delays[i])
        return sum / (len(list_delays) - 1)

    def create_graph(self, x=[], y=[], color='#526B84', markerfacecolor='#95A5A6', x_range_min=1,
                     x_label='', y_label='', title_graph='', path_image='./GraphsImages', name='', dpi=300,
                     bbox_inches='tight', is_delay=True):

        if is_delay:
            plt.plot(x, y, color=color, linestyle='dashed', linewidth=2,
                     marker='o', markerfacecolor=markerfacecolor, markersize=12)
            y_max = max(y)
            plt.ylim(0, y_max + 0.1 * y_max)
            plt.xlim(1, len(x))
        else:
            plt.figure(figsize=(10, 5))
            plt.step(x, y, where='post', )
        # naming the x axis
        plt.xlabel(x_label)  # 'Packet (number)'
        # naming the y axis
        plt.ylabel(y_label)  # 'Delay (ms)'

        # giving a title to my graph
        plt.title(title_graph)  # 'Delay per Packet'

        # function to show the plot
        if not path.exists(path_image):
            Path("./GraphsImages").mkdir(parents=True, exist_ok=True)

        if is_delay:
            text_pos_x = 0
            text_pos_y = - 0.05

            jitter = self.calculate_jitter(y)
            plt.text(text_pos_x, text_pos_y,
                     'Jitter: ' + str(round(jitter, 2)) + ' mms   Max Delay:' + str(
                         round(max(y), 2)) + ' ms   Min Delay:' + str(round(min(
                         y), 2)) + ' ms   Avg Delay: ' + str(round(sum(y) / len(y), 2)) + ' ms', fontsize=10,
                     transform=plt.gcf().transFigure)
        # plt.rcParams['figure.figsize'] = [10, 10]
        else:
            text_pos_x = 0.25
            text_pos_y = - 0.05

            plt.text(text_pos_x, text_pos_y, 'Max load:' + str(round(max(y), 2)) + ' Bytes   Min Load:' + str(round(min(
                y), 2)) + ' Bytes   Avg Load: ' + str(round(sum(y) / len(y), 2)) + ' Bytes', fontsize=10,
                     transform=plt.gcf().transFigure)

        plt.savefig(path_image + '/' + name, dpi=dpi, bbox_inches=bbox_inches)

        plt.clf()

    def create_graph_multiple(self, list_edges=None, x_label='', y_label='', title_graph='',
                              path_image='./GraphsImages', name='', dpi=300, bbox_inches='tight'):

        if not path.exists(path_image):
            Path("./GraphsImages").mkdir(parents=True, exist_ok=True)
        plt.figure(figsize=(10, 5))
        for link in list_edges:

            if 'load' in link[2]:
                print(link[0], link[1], link[2]['load'])

                lista = (link[2]['load']).copy()
                lista.reverse()
                seen = set()
                Output = [(a, b) for a, b in lista
                          if not (a in seen or seen.add(a))]
                Output.reverse()
                print(Output)

                x = []
                y = []
                for data in Output:
                    x.append(data[0])
                    y.append(data[1])

                if 0 < len(x) == len(y) > 0:
                    plt.step(x, y, where='post', label='[' + link[0] + ',' + link[1] + ']')

        plt.xlabel(x_label)  # 'Packet (number)'
        plt.ylabel(y_label)  # 'Delay (ms)'
        plt.title(title_graph)  # 'Delay per Packet'

        plt.savefig(path_image + '/' + name, dpi=dpi, bbox_inches=bbox_inches)
        plt.clf()
