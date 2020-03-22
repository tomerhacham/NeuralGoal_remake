import socket
class Client:
        client=None
        terminate=False
        connected=False
       # def __int__(self):
        #        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #region not relevant
        #hostname, sld, tld, port = 'www', 'integralist', 'co.uk', 80
        #target = (('{}.{}.{}').format(hostname, sld, tld))

        # create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
        #client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # connect the client
        # client.connect((target, port))
        #client.connect(('127.0.0.1', 7777))

        # send some data (in this case a HTTP GET request)
        #client.send(('GET /index.html HTTP/1.1\r\nHost: {}.{}\r\n\r\n').format(sld, tld).encode())

        # receive the response data (4096 is recommended buffer size)
        #response = client.recv(4096)
        #print (response.decode("utf-8"))
        #endregion
        def start(self):
                while self.terminate == False:
                        print('Enter command:')
                        _input = input()
                        if _input=='connect':
                                if self.connected == False:
                                        self.connect()
                                else:
                                        print('You already connected')
                        elif _input=='disconnect':
                                if self.connected==True:
                                        self.logout()
                                else:
                                        print('You already logged out')
                        else:
                                self.send(_input)

        def connect(self):
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client.connect(('176.230.151.201', 443))
                response = self.client.recv(4096)
                print(response.decode("utf-8"))
                if response.decode('utf-8')=='Connected':
                        self.connected=True
                        return
                else:
                        self.terminate=False
        def logout(self):
                self.client.send('disconnect'.encode())
                response = self.client.recv(4096)
                print(response.decode("utf-8"))
                self.client.close()
                self.connected=False
                self.terminate=True
                return
        def send(self,command):
                if self.connected==False:
                        print('You are not connected')
                        return
                else:
                        self.client.send(command.encode())
                        response=self.client.recv(4096)
                        print(response.decode('utf-8'))

def main():
        client=Client()
        client.start()
if __name__ == "__main__":
    main()