import datetime

now = datetime.datetime.now()
past = now + datetime.timedelta(weeks=-52)

print(now)
print(past)
