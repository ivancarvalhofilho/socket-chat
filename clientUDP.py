import socket
import threading

# Esta flag indica se a maquina que esta rodando o programa atuará como 
# um cliente ou um servidor.
# -souServidor == "0": Cliente
# -souServidor == "1": Servidor
souServidor = "0"

# Este vetor irá salvar os IPs da máquinas da seguinte forma:
# Se a maquina for Cliente
#    armazenará apenas o IP do servidor (que deve ser informado no inicio do programa)
# Se a maquina for Servidor
#    armazenará todos os IP das maquinas conectadas a ele
listaDeIPsConectados = []

# Metodo responsável por receber as mensagens e imprimi-las na tela
# Recebe como parâmetro o socket configurado no metodo main()
def recebe_mensagens(s):

    # Declaracao necessária para acessar a variavel global souServidor.
    global souServidor

    while True:
        # Escuta alguma resposta de algum socket da rede, salvando a mensagem e o endereço de quem enviou.
        msg, addr = s.recvfrom(1024)
        
        # Verifica se a maquina esta configurada como servidor
        if (souServidor == "1"):
            # Adiciona o IP de quem enviou a mensagem caso ele não esteja na lista ainda
            if not (addr[0] in listaDeIPsConectados):
                listaDeIPsConectados.append(addr[0])

            # Após atualizar a lista de clientes conectados, reenvia a mensagem para todos eles.
            # Esta utilizando o encode utf-8 para permitir o uso de acentos da lingua portuguesa
            repassa_mensagens(s, addr[0], msg.decode("utf-8"))

            # Imprime a mensagem que o servidor recebeu, caso a mensagem não seja dele mesmo.
            if not (addr[0] == "127.0.0.1"):
                print(addr[0] + " disse: "+msg.decode("utf-8"))

        # Caso a maquina esteja configurada como Cliente, apenas imprime a mensagem 
        # que foi repassada do servidor.
        if (souServidor == "0"):
            print(msg.decode("utf-8"))

# Metodo responsavel por repassar uma mensagem de um cliente para os outros
# clientes conectados ao servidor.
# Obs: Somente o servidor chama este metodo
def repassa_mensagens (s, ipCliente, msg):

    # Adiciona na mensagem o IP do cliente que enviou a mensagem
    msg = ipCliente + " disse: " + msg

    # Faz uma iteração para cada usuario conectado ao servidor
    for ip in listaDeIPsConectados:

        # Evita de enviar a mensagem para o próprio Cliente que a enviou
        if (ipCliente == ip):
            continue

        # Evita de reenviar a mensagem novamente para o Servidor
        if (ip == "127.0.0.1"):
            continue

        # Envia a mensagem para o IP atual da iteração
        s.sendto(msg.encode(), (ip, 4004))

# Metodo responsavel por enviar a mensagem para o servidor
def envia_mensagens(s):
    while True:

        # Armazena a mensagem a ser enviada
        msg = input("")

        # Efetua um loop para enviar a mensagem para as maquinas conectadas
        # Obs: 
        #   No caso do Servidor, enviará a mensagem para todos os Clientes de uma vez
        #   No caso do Cliente, enviará a mensagem para o servidor, que em seguida, irá 
        #   repassa-la para os outros Clientes
        for ip in listaDeIPsConectados:
            if(souServidor == "1" and ip == "127.0.0.1"):
                s.sendto(msg.encode(), (ip,4004))
            elif(souServidor == "0"):
                s.sendto(msg.encode(), (ip,4004))


# Metodo principal do programa
def main():

    # Declaracao necessária para acessar a variavel global souServidor.
    global souServidor

    # Armazena o input indicando se é o servidor ou não
    souServidor = input("Sou o Servidor? (1 ou 0): ")
    
    # Caso a maquina seja um Servidor, seta o IP do Servidor como ela mesma 
    ipServidor = "127.0.0.1"

    # Caso a maquina seja um Cliente, pede o IP do Servidor
    if(souServidor == "0"):
        ipServidor = input("Digite o IP do Servidor:")

    # Adiciona o IP a lista de IPs
    listaDeIPsConectados.append(ipServidor)

    # Configura o sokect como UDP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Configura o socket para ouvir mensagens de todos os IP da rede referente a porta 4004
    s.bind(("0.0.0.0", 4004))

    # Configura uma Thread para rodar o metodo de envia_mensagens de forma assincrona
    # enviando como parametro o socket configurado 
    envia = threading.Thread(target=envia_mensagens, args=(s,))

    # Configura uma Thread para rodar o metodo de recebe_mensagens de forma assincrona
    # enviando como parametro o socket configurado 
    recebe = threading.Thread(target=recebe_mensagens, args=(s,))
    
    # Inicia a Thread de envio de mensagens
    envia.start()

    # Inicia a Thread de recebimento de mensagens
    recebe.start()
    
# Ponto de partida para execução do programa
main()
