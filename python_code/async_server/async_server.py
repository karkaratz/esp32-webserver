import network
import machine
import socket
import uasyncio
from queue import Queue
import select
import random



async def run_thread(q, i):
    print ("WORKER", i)
    while True:
        x=None
        if q.qsize()>0:
            #print ("WORKER", i)
            x = await q.get()
            
        else:
            pass
        if x is not None:
            try:
                a = x.recv(1)
                x.send("<HTML><HEAD><TITLE>ESP32</TITLE></HEAD>Success! My Site Is Working!</HTML>".encode())
                x.close()
            except:
                print ("Broken Connection")
        else:
            pass
        await uasyncio.sleep_ms(1)

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

while sta_if.isconnected() is False:
    sta_if.connect("SSID", "PASSWORD")

sta_if.ifconfig()

machine.freq(240000000)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("0.0.0.0", 80))
#sock.setblocking(0)
sock.listen(1)


q=Queue()


poll=select.poll()
poll.register(sock)

async def main(q, p):
    uasyncio.create_task(run_thread(q, 0))


    j=0
    while True:
        j=j+1
        print (j)
        events = p.poll()
        for i in events:
            try:
                client_sock, address = sock.accept()
                #client_sock.setblocking(0)
            except:
                print ("Broken main")
            await q.put(client_sock)
        await uasyncio.sleep_ms(1)


uasyncio.run(main(q, poll))

