import time
import os

# print(os.getcwd())
file = open("source/repos/think-python/words.txt")
#print(file)

start = time.time()
list1 = []
count = {}
count.get
for line in file:
    word = line.strip()
    list1.append(word)
    # if word in count:
    #     count[word] = count[word]+1
    # else: 
    #     count[word] = 0
    # list1 = list1 + [line]

print("seconds elapsed %f" %(time.time() - start))