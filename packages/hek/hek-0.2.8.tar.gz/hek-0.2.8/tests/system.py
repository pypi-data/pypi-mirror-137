from hek import system


res = system.process.getpidbyname(name="top")

print(res)