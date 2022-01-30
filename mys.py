import socket, time

host = socket.gethostbyname(socket.gethostname())
port = 9090

clients = []

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))

quit = False
print("[ Server Started ]")

while not quit:

    data, addr = s.recvfrom(1024)

    itsatime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
    spl = data.decode('utf-8').split(" ")
    if spl[0] == "hello":
        wel = "[SERVER] welcome to server " + spl[1]
        welEncode = wel.encode('utf-8')
        print("[" + spl[1] + "]" + ' connected to server')
        s.sendto(welEncode, addr)
        if addr not in clients:
            clients.append(addr)
    elif spl[0] == 'bye':
        bye = "[SERVER] goodbye " + spl[1]
        byeEncode = bye.encode('utf-8')
        s.sendto(byeEncode, addr)
        disconnectMessage = "[" + spl[1] + "]" + ' disconnected from server'
        print(disconnectMessage)
        for client in clients:
            if addr != client:
                s.sendto(disconnectMessage.encode("utf-8"), client)
        clients.remove(addr)
    else:
        print("[" + addr[0] + "]=[" + str(addr[1]) + "]=[" + itsatime + "]/", end="")
        print(data.decode("utf-8"))
        # print(data.encode("utf-8"))
        for client in clients:
            if addr != client:
                s.sendto(data, client)

s.close()
