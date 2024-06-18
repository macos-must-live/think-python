# from bisect import bisect
import bisect as b
import time 


def binary_search(list, word = "", start=0, end=0):
    
    length = end-start

    if length < 2:
        return list[start] == word

    # partition = int(len(list)/2)
    partition = start+int(length/2)
    if list[partition] < word:
        return binary_search(list, word, partition+1, end)
    else:
        return binary_search(list, word, start, partition)


wordlist = []
for line in open("c:/users/ruzze/source/repos/think-python/words.txt"):
    word = line.strip()
    wordlist.append(word)

start = time.time()
print("test" in wordlist)
print("[in operation] time elapsed %f" %(time.time()-start))

start = time.time()
print(b.bisect(wordlist, "test"))
print("[bisect operation] time elapsed %f" %(time.time()-start))

start = time.time()
print(binary_search(wordlist, "test", 0, len(wordlist)-1))
print("[binary search operation] time elapsed %f" %(time.time()-start))
