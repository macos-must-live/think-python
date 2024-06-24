import os
import pickle
import shelve
import math

# str = "test" if True else "not test"

db = shelve.open("test.db", "c")

try:
    print(pickle.loads(db["test"]))
    print(pickle.loads(db["test3"]))
except Exception as ex:
    print(f"error: {ex=}")

# "".count
# math.lo
# if True and False:  

db["test"] = pickle.dumps("new testdb")
db["test1"] = pickle.dumps([1,2,3])
# finally: 
db.close()