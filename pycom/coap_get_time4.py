import CoAP
import socket

SERVER = "10.48.172.4" # change to your server's IP address
PORT   = 5683

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

coap = CoAP.Message()
coap.new_header(
	code=CoAP.GET,
	token=0x12345,
	type=CoAP.NON
)
coap.add_option (CoAP.Uri_path, "time")
coap.dump()

s.sendto (coap.to_byte(), (SERVER, PORT))

s.settimeout(10)
resp,addr = s.recvfrom(2000)
answer = CoAP.Message(resp)
answer.dump()

s.settimeout(10)
resp,addr = s.recvfrom(2000)
answer = CoAP.Message(resp)
answer.dump()

mid = answer.get_mid()
ack = CoAP.Message()
ack.new_header(mid=mid, type=CoAP.ACK)
ack.dump()
s.sendto (ack.to_byte(), (SERVER, PORT))
