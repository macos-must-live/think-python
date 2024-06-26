import os
import pickle
import shelve
import math

# str = "test" if True else "not test"

db = shelve.open("test.db", "c")

try:
    # pickle.dumps/pickle.loads
    print(db["test"])
    print(db["test1"])
    print(db["first"])
    print(db["f"].get(1, "[]"))
    print(db["f"])
    print(db.get("first", "no data"))
except Exception as ex:
    print(f"error: {ex=}")

# "".count
# math.lo
# if True and False:  
# "test"

db["test"] = "new testdb"
db["test1"] = [1,2,3]
db["first"] = (1,2,3)
db["f"] = {1:"2", 2:"3"}
# finally: 
db.close()