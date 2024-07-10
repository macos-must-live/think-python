import sys
import os
import shelve
import subprocess
import dbm
from shutil import which
import logging

shelve_db = None 

logger = logging.getLogger(__name__)
logging.basicConfig(filename="md5checksum.log", level=logging.INFO)

def normalize_path(path):
    disk, rel = os.path.splitdrive(path)
    return os.path.join(str(disk).lower(), rel).replace("\\", "/")

def is_md5sum_available():
    return which("md5sum") is not None
def is_certutil_available():
    return which("certutil") is not None

def log(message, verbose=False):
    logger.info(message)
    if verbose: print(message)

def logError(ex):
    logger.error(ex)
    print(f"!!!error: {ex}")

def walk_files(script, dir='.', *rest):
    global shelve_db

    verbose = "--verbose" in rest
    rehash = "--rehash" in rest

    dir = normalize_path(os.path.abspath(dir))
    files_dict,checksums_dict = load_cache()

    if "--check" in rest: 
        print(f"type of the disk database: {dbm.whichdb('cache.db')}")    
        print(f"total files count: {str(len(files_dict.keys()))}")
        print(f"total checksums count: {str(len(checksums_dict.keys()))}")
        print(f"total files in checksums: {sum([len(v) for k,v in checksums_dict.items()])}")
        print(f"total duplicates: {len(files_dict.keys()) - len(checksums_dict.keys())}")
        # for i in sorted(shelve_db["files"].keys()):
        #     print(i)
        # print(shelve_db["files"].get(u"D:/entertainment/music/Aria\Легенды русского рока\Игра с огнем.mp3"))
        # print(shelve_db["files"].get(u"D:/entertainment/music/Aria\Синглы\Дай руку мне.mp3"))
        # print(u"D:/entertainment/music/Aria\Легенды русского рока\Игра с огнем.mp3")
        print("bye!")
        return 

    print(f"processing {dir}", " with rehash" if rehash else "")

    try:
        for root, dirname, files in os.walk(dir,True):
            for f in files:
                file = normalize_path(os.path.join(root,f))
                encoded_file = file

                # if verbose: print(f"{file}", end=" ")
                log(f"{file}", verbose)
                lastmtime = os.path.getmtime(file)
                savedmtime,checksum = files_dict.get(encoded_file, (0, ''))

                # print(f"saved {(savedmtime, checksum)} vs real ({lastmtime})")

                if savedmtime < lastmtime or rehash:
                    checksum = md5(file, "--debug" in rest)
                    print(f"calculated checksum {savedmtime} {lastmtime} {savedmtime < lastmtime} {rehash} {file} {checksum}")
                    
                    # if verbose: print(f" -> {checksum}")
                    log(f" -> {checksum}", verbose)
                    if len(checksum)>0:
                        if checksum in checksums_dict:
                            if encoded_file not in checksums_dict[checksum]:
                                checksums_dict[checksum].append(encoded_file)
                        else:
                            checksums_dict[checksum] = [encoded_file]
                    else:
                        print(f"checksum is invalid {checksum} for {file}")
                        continue
                else:
                    # if verbose: print(f"-> picked saved checksum {(savedmtime,checksum)}")
                    log(f"-> picked saved checksum {(savedmtime,checksum)}", verbose=verbose)

                if len(checksum)>0 and encoded_file not in files_dict: 
                    files_dict[encoded_file] = (lastmtime, checksum)
                    print(f"saving last modif time of {file} to cache")

    finally:
        save_cache(files_dict, checksums_dict)

    duplicates = dict()
    for k,v in checksums_dict.items():
        if len(v) > 1:
            for file in v:
                if file.startswith(dir):
                    if k in duplicates:
                        duplicates[k].append(file)
                    else: 
                        duplicates[k] = [file]

    print("duplicates: ")
    for k,v in duplicates.items():
        print(f"{k}:")
        for file in v:
            # print(f"-{file}".rjust(100))
            print(f"-{file:>120}")

def process_open(command, debug=True):
    if debug: print(command, end=" ")
    try:
        output = subprocess.check_output(command)
        result = output.decode("utf-8", errors="replace")
    except Exception as ex:
        result = ''
        # if debug: print(command)
        # raise
        # if debug: print(f"!error: {command} {ex}", end=" ")
        logError(ex)
    return result 
    
def md5sum(file, debug=True):
    # result = []
    # command = "md5sum" if is_md5sum_available() else "certutil -hashfile" + f" \"{file}\"" + " MD5" if not is_md5sum_available() else ""
    result = process_open(f"md5sum \"{file}\"", debug)
    
    if result.startswith("\\"):
        result = result[1:]

    if debug: print(f"[{result}]", end=" ")
    res = result.strip().split()
    return res[0] if len(res) > 0 else ''

def certutil(file, debug=True):
    result = process_open(f"certutil -hashfile \"{file}\" MD5", debug)
    
    res = result.strip().split("\r")
    if debug: print(f"[{res}]", end=" ")
    return res[1].strip() if len(res) > 1 else ''

def md5(file, debug=True):
    if is_md5sum_available():
        return md5sum(file, debug)
    elif is_certutil_available():
        return certutil(file, debug)
    else:
        raise ValueError("No md5 checksum software supported")

def load_cache(file = "cache.db"):
    with shelve.open(file, "c") as db:
        return db.get("files", dict()), db.get("checksums", dict())    

def save_cache(files, checksums, file = "cache.db"):
    # os.remove(os.path.abspath(file))

    with shelve.open(file, "n") as db:
        db["files"] = files
        db["checksums"] = checksums

if __name__ == "__main__":
    print(f"starting from {sys.path}")
    walk_files(*sys.argv)