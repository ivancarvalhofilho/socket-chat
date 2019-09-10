import socket
import threading

listaDeIPsConectados = []

def recebe_mensagens(s):

    global souServidor

    while True:
        msg, addr = s.recvfrom(1024)
        
        if (souServidor == "1"):
            if not (addr[0] in listaDeIPsConectados):
                listaDeIPsConectados.append(addr[0])

            repassa_mensagens(s, addr[0], msg.decode("utf-8"))

            if not (addr[0] == "127.0.0.1"):
                print(addr[0] + " disse: "+msg.decode("utf-8"))

        if (souServidor == "0"):
            print(msg.decode("utf-8"))

def repassa_mensagens (s, ipCliente, msg):

    msg = ipCliente + " disse: " + msg

    for ip in listaDeIPsConectados:

        if (ipCliente == ip):
            continue

        if (ip == "127.0.0.1"):
            continue

        s.sendto(msg.encode(), (ip, 4004))

def envia_mensagens(s):
    while True:
        msg = input("")

        for ip in listaDeIPsConectados:
            if(souServidor == "1" and ip == "127.0.0.1"):
                s.sendto(msg.encode(), (ip,4004))
            elif(souServidor == "0"):
                s.sendto(msg.encode(), (ip,4004))

def main():

    global souServidor

    souServidor = input("Sou o Servidor? (1 ou 0): ")
    
    ipServidor = "127.0.0.1"
	
    # TODO: metodo de busca de servidores
    if(souServidor == "0"):

	    ipServidor = input("Digite o IP do Servidor:")
	listaDeIPsConectados.append(ipServidor)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.bind(("0.0.0.0", 4004))

    envia = threading.Thread(target=envia_mensagens, args=(s,))

    recebe = threading.Thread(target=recebe_mensagens, args=(s,))
    
    envia.start()

    recebe.start()

main()
