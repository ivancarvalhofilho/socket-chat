import socket
import threading
import os

hostIP = "0.0.0.0"
thisMachineDomain = "0.0.0"

hostList = []

class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

class COMMANDS:
    I_AM_HOST = "/iamhost"
    PING = "/ping"
    LOOKING_FOR_HOST = "/lookingForHost"
    REFRESH = "/refresh"

def getCommandParam(msg):
    command = next(
            (
                getattr(COMMANDS, code)
                for code in dir(COMMANDS) 
                if str(getattr(COMMANDS, code)) in msg
            ),
            False
        )

    if command is False:
        return (False, False)

    return (command, msg.split(command)[1].strip())

def getMsgFromHost(s):
    while True:
        (msg, addr) = s.recvfrom(1024)

        msg = msg.decode("utf-8")
            
        (command, param) = getCommand()

        if command is False:
            print(msg)

        else:
            if command is COMMANDS.I_AM_HOST:
                hostList.append({"ID": len(hostList), "IP": addr})
                showHostList()

def setHostIP():
    global hostIP
    selectedID = input("ID:")
    for ip in hostList: 
        if str(ip["ID"]) == str(selectedID): 
            hostIP = ip["IP"]
    print(hostIP)

def showHostList():
    printColored("Selecione um host pelo ID", bcolors.WARNING)
    printColored("ID: IP", bcolors.WARNING)
    
    for ip in hostList:
        printColored(str(ip["ID"]) + ": " + str(ip["IP"]), bcolors.WARNING)
    
    setHostIP()

def sendMsgToHost(s):
    global hostIP    

    while True:
        msg = input("")

        (command, param) = getCommandParam(msg)

        if command is False:
            s.sendto(msg.encode(), (hostIP, 4004))

        elif command is COMMANDS.REFRESH:
            searchForHost(s)

def searchForHost(s):
    hostList = []
    os.system('clear')

    printColored("Buscando servidores...", bcolors.OKBLUE)

    msg = COMMANDS.LOOKING_FOR_HOST
    
    for lastIpOctet in range(1, 255):
        lookingForIP = thisMachineDomain + str(lastIpOctet)
        s.sendto(msg.encode(), (lookingForIP, 4004))

def setIpAndDomain():
    global thisMachineDomain

    sq = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sq.connect(("1.0.0.0", 3999))
    thisMachineIP = sq.getsockname()[0]
    sq.close()
    
    lastIpOctetLenght = len(thisMachineIP.split(".")[3])
    thisMachineDomain = thisMachineIP[:-lastIpOctetLenght]

def printColored(msg, color = None):
    if color is not None:
        print(color + msg + bcolors.ENDC)
    else:
        print(msg)

def main():
    setIpAndDomain()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("0.0.0.0", 4000))

    searchForHost(s)

    sendMsgThread = threading.Thread(target = sendMsgToHost, args = (s,))
    
    sendMsgThread.start()
    
    # getMsgThread = threading.Thread(target=getMsgFromHost, args = (s,))
    
    # getMsgThread.start()

main()
