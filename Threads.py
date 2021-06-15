# import threading
#
#
# class MyPausableThread(threading.Thread):
#
#     def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
#         self._event = threading.Event()
#         if target:
#             args = (self,) + args
#         super(MyPausableThread, self).__init__(group, target, name, args, kwargs)
#
#     def pause(self):
#         self._event.clear()
#
#     def resume(self):
#         self._event.set()
#
#     def _wait_if_paused(self):
#         self._event.wait()

# class ThreadAnimation(Thread):
#     def __init__(self):
#         self.list_thread_animation = []
#         self.__flag = threading.Event()  # The flag used to pause the thread
#         self.__flag.set()  # Set to True
#         self.__running = threading.Event()  # Used to stop the thread identification
#         self.__running.set()  # Set running to True
#     def add_thread(self, thread_add):
#         thread_add.start()
#         self.list_thread_animation.append(thread_add)

import threading
import time

class run_process(threading.Thread):

    def __init__(self,*args, **kwargs):
        super(run_process, self).__init__(*args, **kwargs)
        print(kwargs)
        self.__flag = kwargs['args'][7]  # The flag used to pause the thread
        self.__flag.set()  # Set to True
        self.__running = kwargs['args'][8]  # Used to stop the thread identification
        self.__running.set()  # Set running to True

    # def run_process(self):
    #     while self.__running.isSet():
    #         self.__flag.wait()  # return immediately when it is True, block until the internal flag is True when it is False
    #         print('holaaaa')
    #         time.sleep(1)



    def pause(self):
        self.__flag.clear()  # Set to False to block the thread

    def resume(self):
        self.__flag.set()  # Set to True, let the thread stop blocking

    def stop(self):
        self.__flag.set()  # Resume the thread from the suspended state, if it is already suspended
        self.__running.clear()  # Set to False

#
# a = run_process()
# a.start()
# time.sleep(3)
# a.pause()
# time.sleep(3)
# a.resume()
# time.sleep(3)
# a.pause()
# time.sleep(2)
# a.stop()