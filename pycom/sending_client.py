import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto("message", ("192.168.43.89", 33033))
