import hek

# server ip
ip = "192.168.0.1"
# targeted port
port = 430
# check
result = hek.server.get_banner(address=ip, port=port)
print(result)