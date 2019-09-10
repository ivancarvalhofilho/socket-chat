import socket
import threading
import collections

hostIP = "0.0.0.0"
thisMachineIP = "0.0.0.0"
thisMachineDomain = "0.0.0"

hostList = []

COMMANDS = {
    "I_AM_HOST" : "/iamhost",
    "PING" : "/ping",
    "LOOKING_FOR_HOST" : "/lookingForHost",
    "REFRESH" : '/refresh'
}

def getCommandParam (msg):
    code = next((code for code, command in COMMANDS.items() if command in msg), False)
    
    if code is False:
        return (False, False)

    return (COMMANDS[code], msg.split(COMMANDS[code])[1].strip())

def recebe_mensagens(s):
    while True:
        msg, addr = s.recvfrom(1024)

        msg = msg.decode("utf-8")
            
        (command, param) = getCommand()

        if command is False:
            print(msg)

        # elif:
            # if command is ""

def envia_mensagens(s):
    global hostIP    
    global isSeachingHost
    while True:
        msg = input("")

        (command, param) = getCommandParam(msg)

        if command is False:
            s.sendto(msg.encode(), (hostIP, 4004))

        elif command is COMMANDS["REFRESH"]:
            searchForHost (s)

def searchForHost (s):
    print("Buscando servidores...")

    msg = COMMANDS["LOOKING_FOR_HOST"] + " " + thisMachineIP
    
    for lastIpOctet in range(1,255):
        lookingForIP = thisMachineDomain + str(lastIpOctet)
        s.sendto(msg.encode(), (lookingForIP, 4004))

def setIpAndDomain ():
    global thisMachineIP
    global thisMachineDomain
    sq = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sq.connect(("1.0.0.0", 3999))
    thisMachineIP = sq.getsockname()[0]
    sq.close()
    thisMachineDomain = thisMachineIP[:-len(thisMachineIP.split(".")[3])]

def main():
    setIpAndDomain()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("0.0.0.0", 4000))

    searchForHost (s)

    envia = threading.Thread(target=envia_mensagens, args=(s,))
    
    envia.start()
    
    # listaDeIPsConectados.append(ipServidor)

    # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # s.bind(("0.0.0.0", 4004))


    # recebe = threading.Thread(target=recebe_mensagens, args=(s,))
    
    # recebe.start()

main()
