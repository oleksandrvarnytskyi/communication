from threading import Thread
from threading import Lock
import time

LOCK = Lock()


class SleepingThread:
    @staticmethod
    def child(it):
        with LOCK:
            for j in range(5):
                print ("\nHello from thread: %s => %s" % (it, j))

    def parent(self):
        for i in range(10):
            t = Thread(target=self.child, args=(i,))
            t.start()
        time.sleep(2)


sleep = SleepingThread()
sleep.parent()
