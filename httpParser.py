class http():
    def __init__(self, data):
        self.method = ''
        self.requestPath = ''
        self.httpVersion = ''
        self.headers = {}
        i = 0
        length = len(data)
        while i < length:
            tmp = chr(data[i])
            if tmp == ' ':
                i += 1
                break
            self.method += tmp
            i += 1
        while i < length:
            tmp = chr(data[i])
            if tmp == ' ':
                i += 1
                break
            self.requestPath += tmp
            i += 1
        while i < length:
            tmp = chr(data[i])
            if data[i] == 13:
                i += 2
                break
            self.httpVersion += tmp
            i += 1
        while i < length:
            curr_head = ''
            while i < length:
                tmp = chr(data[i])
                if tmp == ':':
                    i += 2
                    break
                curr_head += tmp
                i += 1
            curr_value = ''
            while i < length:
                tmp = chr(data[i])
                if data[i] == 13:
                    i += 2
                    break
                curr_value += tmp
                i += 1
            self.headers[curr_head] = curr_value
            print(f"{curr_head}:{curr_value}")
            if data[i] == 13:
                break
