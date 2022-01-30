import socket, threading, time

key = 8194

shutdown = False
join = False


def decodeMessage(data):
    decrypt = "";
    k = False
    for i in data.decode("utf-8"):
        if i == ":":
            k = True
            decrypt += i
        elif k == False or i == " ":
            decrypt += i
        else:
            decrypt += chr(ord(i) ^ key)
    return decrypt

def cryptMessage(message):
    crypt = ""
    for i in message:
        crypt += chr(ord(i) ^ key)
    return crypt

def receving(name, sock):
    while not shutdown:
        try:
            while True:
                data, addr = sock.recvfrom(1024)
                # Begin
                mes = decodeMessage(data)
                print(mes)
                # End
                time.sleep(0.2)
        except:
            pass


def run(name):
    host = socket.gethostbyname(socket.gethostname())
    port = 0

    server = (socket.gethostbyname(socket.gethostname()), 9090)
    # server = ("192.168.0.101",9090)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    s.setblocking(0)

    print("вы можете отправить любое сообщение всем участникам чата, если хотите отключиться от сервера "
          "введите 'bye'")
    rT = threading.Thread(target=receving, args=("RecvThread", s))
    rT.start()
    global shutdown
    global join
    while shutdown == False:
        if join == False:
            s.sendto(("hello " + name).encode("utf-8"), server)
            join = True
        else:
            try:
                message = input()
                data = message
                if message == 'bye':
                    exitMes = 'bye ' + name
                    s.sendto(exitMes.encode("utf-8"), server)
                    s.shutdown()
                else:
                    # Begin
                    message = cryptMessage(message)
                    # End

                    if message != "":
                        s.sendto(("[" + name + "] :: " + message).encode("utf-8"), server)
                    time.sleep(0.2)
            except:
                print("Connection closed")
                shutdown = True
    rT.join()
    s.close()


print("доступные команды 'connect <имя>'")
res = input()
spl = res.split(" ")
if spl[0] == "connect":
    run(spl[1])
