import os
import pickle
import shelve
import math
import subprocess
import re
import urllib
import urllib.request
import bisect
import heapq

# str = "test" if True else "not test"
# bisect.
unsorted = [1,2,8,2,4,9,1,0]
heapq.heapify(unsorted)
print(unsorted)

print(b"\x01\x02")

# re.findall

class TestClass(object):
    def __init__(self, p1, p2):
        self.param1 = p1
        self.param2 = p2
    
    def toStr(self):
        return f'param1: {self.param1}, param2: {self.param2}'

    def __str__(self):
        return self.toStr()
    

class TestClass2(TestClass):
    def toStr(self):
        return f'overridden toStr()'

    def _toStr(self):
        return super().toStr()

c1 = TestClass("p1", "p2")
c2 = TestClass2("adf", "asdf")

print(c1)
print(c2)
print(c2.toStr())
print(c2._toStr())

d = 12.5
print(f"[{d:10}]")
print(f"[{d:<10}]")
# print(f"[{d:10d}]")
print(f"[{d:2.2f}]")
print(f"[{d=}]")

# for x in range(1,11): print(f"[{x:2d}] [{x*x:3d}] [{x**3:4d}] [{x:<4}]")
print("[" + " ".join([f"{k}: " + "{" + k + "};" for k,v in vars().items()]) + "]")
print(" ".join([f"{k}: " + "{" + k + "};" for k,v in vars().items()]).format(**vars().items()))

# with urllib.request.
# --------------------------

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


