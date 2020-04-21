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


def getMethod(conn):
    method = ''
    while True:
        data = conn.recv(1)
        if not data:
            break
        if data == b' ':
            break
        method += chr(data[0])
    return method


def getRequestPath(conn):
    requestPath = ''
    while True:
        data = conn.recv(1)
        if not data:
            break
        if data == b' ':
            break
        requestPath += chr(data[0])
    return requestPath


def getHttpVersion(conn):
    httpVersion = ''
    while True:
        data = conn.recv(1)
        if not data:
            break
        if data == b'\r':
            conn.recv(1)
            break
        httpVersion += chr(data[0])
    return httpVersion


def getHeaders(conn):
    headers = {}
    while True:
        curr_head = ''
        while True:
            data = conn.recv(1)
            if not data:
                break
            if data == b'\r':
                conn.recv(1)
                return headers
            tmp = chr(data[0])
            if tmp == ':':
                conn.recv(1)
                break
            curr_head += tmp
        curr_value = ''
        while True:
            data = conn.recv(1)
            if not data:
                break
            tmp = chr(data[0])
            if data[0] == 13:
                conn.recv(1)
                break
            curr_value += tmp
        if not curr_head:
            break
        headers[curr_head] = curr_value
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
