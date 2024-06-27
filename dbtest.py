import os
import pickle
import shelve
import math

# str = "test" if True else "not test"

db = shelve.open("test.db", "c")

print(hash(u"D:/entertainment/music/Aria\Легенды русского рока\Игра с огнем.mp3"))
print(u"D:/entertainment/music/Aria\Легенды русского рока\Игра с огнем.mp3".encode("utf-16le"))

try:
    # pickle.dumps/pickle.loads
    print(db["test"])
    print(db["test1"])
    print(db["first"])
    print(db["f"].get(1, "[]"))
    print(db["f"])
    
    print(db.get("first", "no data"))
    print(db.get(u"D:/entertainment/music/Aria\Легенды русского рока\Игра с огнем.mp3"))
    # print(db.get((u"D:/entertainment/music/Aria\Легенды русского рока\Игра с огнем.mp3".encode("utf-16le"))))
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
db[u"D:/entertainment/music/Aria\Легенды русского рока\Игра с огнем.mp3"] = "test"
# db[u"D:/entertainment/music/Aria\Легенды русского рока\Игра с огнем.mp3".encode("utf-16le")] = "test1"
# finally: 
db.close()