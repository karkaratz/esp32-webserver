import network
import machine
import socket


def hello_world(server):
    ''' request handler '''
    try:
        server.send("<HTML><HEAD><TITLE>ESP32</TITLE></HEAD>Success! My Site Is Working!</HTML>".encode())
    except:
        print("Error Connection Lost")


sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

while sta_if.isconnected() is False:
    sta_if.connect("SSID", "PASSWORD")

sta_if.ifconfig()

machine.freq(240000000)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("0.0.0.0", 80))
sock.listen(0)

i=0

while True:
    i=i+1
    print (i)
    client_sock, address = sock.accept()
    print (i)
    try:
        a = client_sock.recv(1)
        hello_world(client_sock)
        client_sock.close()
    except:
        print("Error Connection Lost")

    
    
