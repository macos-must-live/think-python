import threading
import queue

q = queue.Queue()

def fib(n):
    if n==1: return 1
    if n==0: return 0
    return fib(n-1)+fib(n-2)

def worker():
    while True:
        item = q.get()
        print(f'[{threading.current_thread().name}] Working on {item}')
        result = fib(item)
        print(f'[{threading.current_thread().name}] Finished {item}, resut: {result}')
        q.task_done()



# Turn-on the worker thread.
threading.Thread(target=worker, daemon=True, name="Thread #1").start()
threading.Thread(target=worker, daemon=True, name="Thread #2").start()
threading.Thread(target=worker, daemon=True, name="Thread #3").start()
threading.Thread(target=worker, daemon=True, name="Thread #4").start()
threading.Thread(target=worker, daemon=True, name="Thread #5").start()

# Send thirty task requests to the worker.
for item in range(40):
    q.put(item)

# Block until all tasks are done.
q.join()
print('All work completed')