import time

memos = {0: 0, 1: 1}

def fibonacci(n):
    if n == 0: 
        return 0
    if n == 1: 
        return 1
    
    return fibonacci(n-1)+fibonacci(n-2)

def fibonacci_with_memos(n):
    # if n == 0: 
    #     return 0
    # if n == 1: 
    #     return 1

    if not n in memos: 
        memos.setdefault(n, fibonacci_with_memos(n-1)+fibonacci_with_memos(n-2))
    print("fib(%d)=%d" %(n,memos[n]))
    return memos[n]

start = time.time()
print(fibonacci_with_memos(40))
print("time elapsed with memos: %f" %(time.time()-start))

start = time.time()
print(fibonacci(40))
print("time elapsed: %f" %(time.time()-start))
