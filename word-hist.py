import string

hist = dict()
sortable = []

f = open("C:/Users/ruzze/source/repos/think-python/emma.txt")
replace = string.punctuation+string.whitespace
for line in f:
    #for word in line.strip(string.punctuation+string.whitespace).lower().split():
    for word in line.strip().lower().split():
        word = word.translate(str.maketrans("", "", replace))
        hist[word] = hist.get(word,0)+1

for key,value in hist.items():
    sortable.append((value, key ,))

sortable.sort(reverse=True)

for key, value in sortable[:10]:
    print("[%s] used %d times" % (value, key))