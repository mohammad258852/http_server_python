class http():
    def __init__(self, conn):
        self.method = getMethod(conn)
        self.requestPath = getRequestPath(conn)
        self.httpVersion = getHttpVersion(conn)
        self.headers = getHeaders(conn)
        if self.method == 'POST':
            self.data = getData(conn)
        else:
            self.data = b''

    def __str__(self):
        return f'{self.method} {self.requestPath} {self.httpVersion} {self.headers} {self.data}'

ENDLINE = b'\r\n'

def getMethod(conn):
    method = readTillGet(conn,b' ')
    return method.decode("utf-8")


def getRequestPath(conn):
    requestPath = readTillGet(conn,b' ').decode("utf-8")
    return requestPath


def getHttpVersion(conn):
    httpVersion = readTillGet(conn,ENDLINE).decode("utf-8")
    return httpVersion


def getHeaders(conn):
    headers = {}
    while True:
        header = readTillGet(conn,ENDLINE).decode("utf-8")
        if not header:
            break
        head = header[:header.find(":")]
        value = header[header.find(":")+2:]
        if not head:
            break
        headers[head] = value
    return headers


def getData(conn):
    data = []
    boundry = readTillGet(conn, b'\r\n')
    while True:
        tmp = readTillGet(conn, boundry)
        data.append(tmp)
        tmp = readTillGet(conn, b'\r\n')
        if tmp == b'--':
            break
    return data


def readTillGet(conn, reach):
    data = b''
    while True:
        tmp = b''
        i = 0
        while i < len(reach):
            tt = conn.recv(1)
            if not tt:
                data+=tmp
                return data
            tmp += tt
            if tt[0] == reach[i]:
                i += 1
            else:
                break
        if i == len(reach):
            break
        else:
            data += tmp
    return data
    