import os
import pickle
import shelve
import math
import subprocess

# str = "test" if True else "not test"

db = shelve.open("test.db", "c")

# out = subprocess.check_output("md5sum \"D:/entertainment/music/Aria\\1986 - С кем ты\\07-Икар.mp3\"")
# out = subprocess.check_output("md5sum \"D:/temp/md5/IP96B-A7T_1121_B.pdf\"")
# out = subprocess.check_output("certutil -hashfile MD5 \"D:/temp/md5/IP96B-A7T_1121_B.pdf\"")
out = subprocess.check_output("certutil -hashfile \"d:/entertainment/music/Aria/Синглы/Дай руку мне.mp3\" MD5")
# "dag".st

print("%-20s|%20s" % ('foo', 'bar'))
print(os.path.splitdrive("d:/entertainment/music/Aria/Синглы/Дай руку мне.mp3"))

print(out.decode("utf-8", errors="replace"))
print(out)
os.path.abspath


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