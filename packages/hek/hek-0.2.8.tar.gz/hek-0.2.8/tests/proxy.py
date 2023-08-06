import hek

# adding host manually
host = "127.0.0.1:9050"

# request session
session = hek.tor.get_session(host="127.0.0.1:9050")
# request your proxy identity..
identity = session.identity(host=host)
# print proxy identity
print(identity)