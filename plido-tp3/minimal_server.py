import socket
import binascii

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0', 33033))

values = []

while True:
    data, addr = s.recvfrom(1500)
    print (data, "=>", binascii.hexlify(data))

    new_value = float(data)
    values.append(new_value)
    print(
        f"Average: {sum(values) / len(values) }"
    )
