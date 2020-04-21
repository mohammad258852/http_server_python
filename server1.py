from socket import *
import os
import datetime
import signal
import threading
import time
import httpParsersecond


def makeHeader(code):
    rescodedic = {200: 'OK', 404: 'NotFound'}
    if not(code in rescodedic):
        code = 404
    res = f"""HTTP/1.1 {code} {rescodedic[code]}\r\nDate: {datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")}\r\nServer: Mohammad\r\nConnection: Closed\r\n\r\n"""
    return bytes(res, 'UTF-8')


def sendfile(conn, add):
    try:
        sentfile = open(add, 'rb')
    except:
        print("file not found")
        return
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
    myhttp = httpParsersecond.http(conn)
    print(myhttp)
    if myhttp.method == '':
        return
    req = myhttp.requestPath[1:]
    print(req)
    if req == '':
        req = 'index.html'
    if os.path.isfile(req):
        head = makeHeader(200)
        conn.send(head)
        sendfile(conn, req)
    else:
        head = makeHeader(404)
        conn.send(head)
        sendfile(conn, "NotFound.html")
    print(f'closing conn {add}')
    conn.close()


s = socket(AF_INET, SOCK_STREAM)
ip = ''
port = 80
s.bind((ip, port))
s.listen()
print(f"listening ip {ip} on port {port}")
while True:
    conn, add = s.accept()
    print(f"geting a connetion {add}")
    handle(conn, add)
    #x = threading.Thread(target=handle, args=(conn, add,))
    # x.start()
