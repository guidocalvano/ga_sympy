import asyncio
from threading import Thread, Lock
import ipynbname

from IPython.core.events import EventManager
from IPython import get_ipython


def notebook_hash():
    return ipynbname.path()

notebook_loops = {}
notebook_locks = {}

def asyncio_in_thread():
    global notebook_loops
    global notebook_locks

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError as e:
        loop = asyncio.new_event_loop()

    notebook_loops[notebook_hash()] = loop
    notebook_locks[notebook_hash()] = Lock()

    loop.run_until_complete(cell_execution_loop(notebook_locks[notebook_hash()]))

async def cell_execution_loop(lock: Lock):
    # Lock so you can release in the loop
    lock.acquire()
    while True:
        lock.release()  # let the notebook cell thread execute
        lock.acquire()  # and immediately lock again
        await asyncio.sleep(0)  # Let the event loop execute a scheduled task


def register_thread_safe_cell_execution():
    print("registering cell executiong callbacks")
    ipython = get_ipython()
    ipython.events.register('pre_execute', lock_pre_cell)
    ipython.events.register('post_execute', lock_post_cell)


def lock_pre_cell():
    print("Acquiring cell lock")
    notebook_locks[notebook_hash()].acquire()

def release_post_cell():
    try:
        notebook_locks[notebook_hash()].release()
        print("Releasing cell lock")

    except RuntimeError as e:
        print("Cannot release lock, during registration, because it was never acquired")

        # This is probably because this is the cell that registered the cell execution callbacks
        pass

def get_event_loop():
    global notebook_loops

    return notebook_loops[notebook_hash()]

thread = Thread(target=asyncio_in_thread).start()