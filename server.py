from socket import *
import os
import datetime
import threading
import time


def makeHeader(code):
    rescodedic = {200: 'OK', 404: 'NotFound'}
    if not(code in rescodedic):
        code = 404
    res = f"""HTTP/1.1 {code} {rescodedic[code]}\r\nDate: {datetime.datetime.now()}\r\nServer: Mohammad\r\nConnection: Closed\r\n\r\n"""
    return bytes(res, 'UTF-8')


def sendfile(conn, add):
    sentfile = open(add, 'rb')
    partnum = 0
    while True:
        tmp = sentfile.read(1024)
        if not tmp:
            break
        conn.send(tmp)
        print(f"part {partnum} sent")
        partnum += 1

    print("file %s sent" % add)


def handle(conn, add):
    bindata = conn.recv(2048)
    print(bindata)
    if not bindata:
        return
    data = bindata.decode('UTF-8')
    data = data.split('\r\n')
    # print(data)
    req = data[0].split(' ')[1]
    # print(req)
    req = req[1:]
    if req == '':
        req = 'index.html'
    if os.path.isfile(req):
        head = makeHeader(200)
        conn.send(head)
        sendfile(conn, req)
    else:
        head = makeHeader(404)
        conn.send(head)
    print(f'closing conn {add}')
    conn.close()


def KeyHandler(signal, frame):
    exit(0)


signal.signal(signal.SIGINT, KeyHandler)
s = socket(AF_INET, SOCK_STREAM)
ip = ''  # '0.0.0.0'
port = 80
s.bind((ip, port))
s.listen()
print(f"listening ip {ip} on port {port}")
while True:
    conn, add = s.accept()
    print(f"geting a connetion {add}")
    print(conn)
    x = threading.Thread(target=handle, args=(conn, add,))
    x.start()
    # print(data)
    #handle(conn, data)
    # conn.close()
    #print("closing con")
