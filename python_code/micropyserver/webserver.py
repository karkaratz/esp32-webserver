import network
import machine
from micropyserver import MicroPyServer

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
while sta_if.isconnected() is False:
    sta_if.connect("SSID", "PASSWORD")
sta_if.ifconfig()

machine.freq(240000000)

def hello_world(request):
    ''' request handler '''
    server.send("<HTML><HEAD><TITLE>ESP32</TITLE></HEAD>Success! My Site Is Working!</HTML>")

server = MicroPyServer()
''' add route '''
server.add_route("/", hello_world)
''' start server '''
server.start()
