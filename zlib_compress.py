import zlib
import zipfile
import os

print(os.getcwd())
# zlib.
# zipfile.

# with open("test.txt", "rb") as input:
#     with open("test.zip", "wb") as out:
#         while True:
#             b = input.read(1024)
#             if len(b)>0:
#                 # compressed = zlib.compress(b)
                
#                 out.write("test.txt", b)
#             else:
#                 break

with zipfile.ZipFile("test.zip", "w", compression=zipfile.ZIP_LZMA) as out:
    out.write("test.txt", "test.txt")
    # out.


print("Done")
