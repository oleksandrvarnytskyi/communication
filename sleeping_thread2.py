import thread
import time

MUTEX = thread.allocate_lock()


def child(my_id, num):
    with MUTEX:
        for n in range(num):
            print ("\nHello from thread: %s => %s" % (my_id, n))


def parent():
    for i in range(5):
        thread.start_new_thread(child, (i, 5))

parent()
time.sleep(3)
print ('Main thread exiting.')
