import sys
import os
import shelve
import subprocess
import dbm

shelve_db = None 
def opendb():
    global shelve_db
    shelve_db = shelve.open("checksums.db", "c", writeback=True,)

def walk_files(script, dir, *rest):
    global shelve_db

    verbose = "--verbose" in rest
    rehash = "--rehash" in rest

    if "--check" in sys.argv: 
        print(f"type of the disk database: {dbm.whichdb('checksums.db')}")
        
        print(f"total files count: {str(len(shelve_db['files'].keys()))}")
        print(f"total checksums count: {str(len(shelve_db['checksums'].keys()))}")
        print(f"total files in checksums: {sum([len(v) for k,v in shelve_db['checksums'].items()])}")
        print(f"total duplicates: {len(shelve_db['files'].keys()) - len(shelve_db['checksums'].keys())}")
        # for i in sorted(shelve_db["files"].keys()):
        #     print(i)
        # print(shelve_db["files"].get(u"D:/entertainment/music/Aria\Легенды русского рока\Игра с огнем.mp3"))
        # print(shelve_db["files"].get(u"D:/entertainment/music/Aria\Синглы\Дай руку мне.mp3"))
        # print(u"D:/entertainment/music/Aria\Легенды русского рока\Игра с огнем.mp3")
        print("bye!")
        return 

    print(f"processing {dir}", " with rehash" if rehash else "")
    for root, dirname, files in os.walk(dir,True):
        for f in files:
            file = os.path.join(root,f)
            # encoded_file = file.encode("utf-16le")
            encoded_file = file

            if verbose: print(f"{file}", end=" ")
            lastmtime = os.path.getmtime(file)
            savedmtime,checksum = shelve_db["files"].get(encoded_file, (0, ''))

            # print(f"saved {(savedmtime, checksum)} vs real ({lastmtime})")

            if savedmtime < lastmtime or rehash:
                checksum = md5(file, "--debug" in rest)
                print(f"calculated checksum {savedmtime} {lastmtime} {savedmtime < lastmtime} {rehash} {file} {checksum}")
                
                if verbose: print(f" -> {checksum}")
                if len(checksum)>0:
                    if checksum in shelve_db["checksums"]:
                        shelve_db["checksums"][checksum].append(encoded_file)
                    else:
                        shelve_db["checksums"][checksum] = [encoded_file]
                else:
                    print(f"checksum is invalid {checksum} for {file}")
                    continue
            else:
                if verbose: print(f"-> picked saved checksum {(savedmtime,checksum)}")

            if len(checksum)>0 and encoded_file not in shelve_db["files"]: 
                shelve_db["files"][encoded_file] = (lastmtime, checksum)
                print(f"saving last modif time of {file} to cache")

            shelve_db.sync()

    print("duplicates: ")
    for k,v in shelve_db["checksums"].items():
        if len(v) > 1:
            print(f"{k}:")
            for file in v:
                print(f"-{file}".rjust(100))


def md5(file, debug=True):
    # result = []
    command = f"md5sum \"{file}\""
    if debug: print(command, end=" ")
    # with os.popen(command) as md5:
    try:
        output = subprocess.check_output(command)
        # result = md5.read()
        result = output.decode("utf-8")
    except Exception as ex:
        result = ''
        # if debug: print(command)
        # raise
        if debug: print(f"!error: {command} {ex}", end=" ")

    if result.startswith("\\"):
        result = result[1:]

    if debug: print(f"[{result}]", end=" ")
    res = result.strip().split()
    return res[0] if len(res) > 0 else ''

if __name__ == "__main__":
    # opendb()
    print(f"starting from {sys.path}")
    shelve_db = shelve.open("checksums.db", "c", writeback=True)
    shelve_db["files"] = shelve_db.get("files", dict())
    shelve_db["checksums"] = shelve_db.get("checksums", dict())
        
    # shelve_db["files"][3] = "test"
    # print(shelve_db["files"] )
    try:
        walk_files(*sys.argv)
    finally:
        shelve_db.close()