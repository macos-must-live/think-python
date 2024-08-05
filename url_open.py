from urllib.request import urlopen

with urlopen('http://worldtimeapi.org/api/timezone/etc/UTC.txt') as response:
    # response
    print(response.getcode())
    for line in response:        
        line = line.decode()             # Convert bytes to a str
        if line.startswith('datetime'):
            print(line.rstrip()) 