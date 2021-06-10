# class LoadLink:
#
#     def __init__(self):
#         self.list_loaad = []
#
#     def get_list_loaad(self):
#         return self.list_loaad
#
#     def add_list_load(self, time_change, load):
#         self.list_loaad.append((time_change, load))
#
#     def link_loadevery_moment(self):
#         list_link_loadevery_moment = []
#
#         previous_load = None
#
#         for load in self.list_loaad:
#
#             if previous_load != None:
#
#                 # Si el instante de carga (de la carga actual) es mayor que la anterior (que el momento en el que
#                 # termina la anterior), tenemos que generar otros momentos de carga ya que en algún momento se solapan
#                 # (hay carga del enlace que en un momento se superpone con la carga de otro paquete)
#
#                 if load[0] < previous_load[1]:
#
#                     list_link_loadevery_moment.pop()
#
#                     if load[0] != previous_load[0]:
#                         list_link_loadevery_moment.append((previous_load[0],load[0], previous_load[2]))
#                         list_link_loadevery_moment.append((load[0],previous_load[1], previous_load[2] + load[2]))
#                         list_link_loadevery_moment.append((previous_load[1], load[1], loa))
#
#                 else:
#
#                     list_link_loadevery_moment.append(load)
#
#             previous_load = load
