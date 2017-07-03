import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
while True:
    sock.sendto('broadcast!'.encode(), ('255.255.255.255', 11719))