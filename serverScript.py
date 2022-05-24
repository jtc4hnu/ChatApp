import socket
import threading
import select

def IsInList(ls, tst):
    out = False
    for i in range(len(ls)):
        if ls[i] == tst:
            out = True
    return out


hostname = socket.gethostname()
print("Hostname: " + hostname)
print("Outmost IP: " + socket.gethostbyname(socket.gethostname()))
host = input("Enter Host IP: ")


socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((host, 1051))
socket.listen(5)
print("Host Established")
clients = []
addresses = []


def Accept():
    global thread
    (clientsocket, address) = socket.accept()
    if not IsInList(clients, clientsocket):
        print("NEW CLIENT", clientsocket, address)
        clients.append(clientsocket)
        addresses.append(address)
    thread = threading.Thread(target = Accept)
    thread.start()
    
thread = threading.Thread(target = Accept)
thread.start()
  
active = True
while active:
    if len(clients) > 0:
        ready = select.select(clients, [], [], 0.1)
        for i in range(len(ready[0])):
            data = ready[0][i].recv(1024).decode("ASCII")
            print(data)
            if data == "rm_me":
                clients.remove(clientsocket)
            elif data == "cl_sk":
                active = false
            for i in range(len(clients)):
                clients[i].send(data.encode("ASCII"))

socket.close()
